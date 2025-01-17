#!/usr/bin/env python3
import os

import aws_cdk as cdk

from portfolio_cdk.network_stack import NetworkStack
from portfolio_cdk.services_stack import ServicesStack
from dotenv import load_dotenv

load_dotenv()

app = cdk.App()
network_stack = NetworkStack(app, "PortfolioCdkStack",
                             # If you don't specify 'env', this stack will be environment-agnostic.
                             # Account/Region-dependent features and context lookups will not work,
                             # but a single synthesized template can be deployed anywhere.

                             # Uncomment the next line to specialize this stack for the AWS Account
                             # and Region that are implied by the current CLI configuration.

                             # env=cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'), region=os.getenv('CDK_DEFAULT_REGION')),

                             # Uncomment the next line if you know exactly what Account and Region you
                             # want to deploy the stack to. */

                             env=cdk.Environment(region=os.getenv('REGION')),

                             # For more information, see https://docs.aws.amazon.com/cdk/latest/guide/environments.html
                             )

service_stack = ServicesStack(app, "PortfolioServicesStack", vpc=network_stack.ref_vpc(
), env=cdk.Environment(region=os.getenv('REGION')))

app.synth()
