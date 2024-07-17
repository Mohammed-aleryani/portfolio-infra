from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_ecs as ecs,
    aws_ecr as ecr,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct
import os
from dotenv import load_dotenv

load_dotenv()


class ServicesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        cluster = ecs.Cluster(self, "EcsCluster",
                              vpc=vpc,
                              enable_fargate_capacity_providers=True
                              )

        task_definition = ecs.FargateTaskDefinition(
            self, "TaskDef", cpu=256, memory_limit_mib=512)

        ecr_repository = ecr.Repository.from_repository_name(
            self, "ECRRepository", os.getenv("ECR_REPO_NAME"))

        task_definition.add_container(
            "image",
            image=ecs.ContainerImage.from_ecr_repository(ecr_repository),
            port_mappings=[ecs.PortMapping(container_port=80)]
        ),

        service = ecs.FargateService(self, "FargateService",
                                     cluster=cluster,
                                     task_definition=task_definition,
                                     assign_public_ip=False,
                                     desired_count=2,
                                     capacity_provider_strategies=[ecs.CapacityProviderStrategy(
                                         capacity_provider="FARGATE_SPOT",
                                         weight=1
                                     ), ecs.CapacityProviderStrategy(
                                         capacity_provider="FARGATE",
                                         weight=1
                                     )
                                     ]
                                     )
        lb = elbv2.ApplicationLoadBalancer(self, "portfolio-alb",
                                           vpc=vpc,
                                           internet_facing=True,
                                           load_balancer_name="portfolio-lb"
                                           )

        listener = lb.add_listener("Listener",
                                   port=80,
                                   open=True
                                   )
        listener.add_targets("portfolio-TG",
                             port=8080,
                             targets=[service.load_balancer_target(
                                 container_name='image', container_port=80
                             )]
                             )
        lb.connections.allow_to(service, ec2.Port.tcp(80), "Allow HTTP")
