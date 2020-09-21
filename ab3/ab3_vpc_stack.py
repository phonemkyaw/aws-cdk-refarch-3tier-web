from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_s3 as _s3

class Ab3VpcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        public_subnet = _ec2.SubnetConfiguration(
            name="publicSubnet",
            cidr_mask=24,
            subnet_type=_ec2.SubnetType.PUBLIC
        )

        private_subnet = _ec2.SubnetConfiguration(
            name="privateSubnet",
            cidr_mask=24,
            subnet_type=_ec2.SubnetType.PRIVATE
        )

        db_subnet = _ec2.SubnetConfiguration(
            name="dbSubnet",
            cidr_mask=24,
            subnet_type=_ec2.SubnetType.ISOLATED
        )


        self.vpc = _ec2.Vpc(
            self,
            "Vpc",
            cidr="10.0.0.0/16",
            subnet_configuration=[public_subnet, private_subnet, db_subnet],
            max_azs=3,
            nat_gateways=1
        )


        self.vpc.sg = _ec2.SecurityGroup(
            self,
            "vpcSg",
            vpc=self.vpc
        )
        self.vpc.sg.add_ingress_rule(self.vpc.sg, _ec2.Port.tcp(6379))  #Redis
        self.vpc.sg.add_ingress_rule(self.vpc.sg, _ec2.Port.tcp(3306))  #Aurora MySQL

        core.CfnOutput(self, "outputVpc", value=self.vpc.vpc_id)
        # core.CfnOutput(self, "outputSg", value=self.vpc_sg.security_group_id)
