from aws_cdk import core
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_elasticache as _ec


class EcStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.sng = _ec.CfnSubnetGroup(
            self,
            "ecSubnetGroup",
            description="redisSubnetGroup",
            subnet_ids=vpc.select_subnets(subnet_type=_ec2.SubnetType.ISOLATED).subnet_ids,
            cache_subnet_group_name=f"{core.Aws.STACK_NAME}-ecSng"
        )

        self.ec = _ec.CfnReplicationGroup(
            self,
            "redisCluster",
            replication_group_description="redisReplicationGroup",
            engine="redis",
            engine_version="5.0.6",
            cache_node_type="cache.t3.micro",
            automatic_failover_enabled=True,
            auto_minor_version_upgrade=True,
            cache_subnet_group_name=self.sng.cache_subnet_group_name,
            num_node_groups=3,
            security_group_ids=[vpc.sg.security_group_id]
        )
        # core.CfnOutput(self, "outputSg", value=self.vpc_sg.security_group_id)
