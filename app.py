#!/usr/bin/env python3

from aws_cdk import core

from ab3.ab3_vpc_stack import Ab3VpcStack
from ab3.ab3_fargate_stack import Ab3FargateStack
from ab3.ab3_cdn_stack import Ab3CdnStack
from ab3.ab3_rds_stack import Ab3RdsStack
from ab3.ab3_ec_stack import Ab3EcStack

app = core.App()


vpc_stack = Ab3VpcStack(app, "ab3-vpc")
ec_stack = Ab3EcStack(app, "ab3-ec", vpc=vpc_stack.vpc)
fargate_stack = Ab3FargateStack(app, "ab3-fargate", vpc=vpc_stack.vpc, redis=ec_stack.ec)
cdn_stack = Ab3CdnStack(app, "ab3-cdn", vpc=vpc_stack.vpc, alb=fargate_stack.lb)
rds_stack = Ab3RdsStack(app, "ab3-rds", vpc=vpc_stack.vpc)


app.synth()
