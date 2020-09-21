#!/usr/bin/env python3

from aws_cdk import core

from cdk.vpc_stack import VpcStack
from cdk.fargate_stack import FargateStack
from cdk.cdn_stack import CdnStack
from cdk.rds_stack import RdsStack
from cdk.ec_stack import EcStack

app = core.App()


vpc_stack = VpcStack(app, "cdk-vpc")
ec_stack = EcStack(app, "cdk-ec", vpc=vpc_stack.vpc)
fargate_stack = FargateStack(app, "cdk-fargate", vpc=vpc_stack.vpc, redis=ec_stack.ec)
cdn_stack = CdnStack(app, "cdk-cdn", vpc=vpc_stack.vpc, alb=fargate_stack.lb)
rds_stack = RdsStack(app, "cdk-rds", vpc=vpc_stack.vpc)


app.synth()
