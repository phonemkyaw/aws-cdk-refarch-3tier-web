from aws_cdk import core
from aws_cdk import aws_rds as _rds
from aws_cdk import aws_ec2 as _ec2


class Ab3RdsStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        master_user = _rds.Login(
            username="user",
            password=core.SecretValue.plain_text("password")
        )

        rds = _rds.DatabaseCluster(
            self,
            "rds",
            engine=_rds.DatabaseClusterEngine.aurora_mysql(version=_rds.AuroraMysqlEngineVersion.VER_5_7_12),
            master_user=master_user,
            instance_props=_rds.InstanceProps(
                vpc=vpc,
                instance_type=_ec2.InstanceType("t3.medium"),
                security_groups=[vpc.sg],
                vpc_subnets=_ec2.SubnetSelection(subnets=vpc.isolated_subnets)
            ),
            instances=2
        )


        # core.CfnOutput(self, "outputSg", value=self.vpc_sg.security_group_id)
