from aws_cdk import (
    Stack,
    aws_ec2 as ec2,
)
from constructs import Construct


class NetworkStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        self.vpc = ec2.Vpc(self, "PortfolioVpc", max_azs=2, create_internet_gateway=True, nat_gateways=1,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name="public", subnet_type=ec2.SubnetType.PUBLIC),
                               ec2.SubnetConfiguration(
                                   name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
                           ],
                           )

    def ref_vpc(self):
        return self.vpc
