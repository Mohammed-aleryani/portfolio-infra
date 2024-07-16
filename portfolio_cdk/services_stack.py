from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
    aws_elasticloadbalancingv2 as elbv2
)
from constructs import Construct


class ServicesStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.IVpc, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lb = elbv2.ApplicationLoadBalancer(self, "portfolio",
                                           vpc=vpc,
                                           internet_facing=True,
                                           load_balancer_name="portfolio-lb"
                                           )

        # Add a listener and open up the load balancer's security group
        # to the world.
        listener = lb.add_listener("Listener",
                                port=80,

                                # 'open: true' is the default, you can leave it out if you want. Set it
                                # to 'false' and use `listener.connections` if you want to be selective
                                # about who can access the load balancer.
                                open=True
                                )

        # Create an AutoScaling group and add it as a load balancing
        # target to the listener.
        listener.add_targets("portfolio-TG",
                            port=8080,
                            targets=[]
                            )
