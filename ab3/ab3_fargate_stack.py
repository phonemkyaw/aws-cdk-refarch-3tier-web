from aws_cdk import core
from aws_cdk import aws_ecr as _ecr
from aws_cdk import aws_ecr_assets as _ecr_assets
from aws_cdk import aws_ecs as _ecs
from aws_cdk import aws_ec2 as _ec2
from aws_cdk import aws_elasticloadbalancingv2 as _elbv2

class Ab3FargateStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, redis,**kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        

        self.ecr = _ecr.Repository(
            self,
            "ecrRepo"
        )

        self.ecs_cluster = _ecs.Cluster(
            self,
            "ecsCluster",
            container_insights=True,
            vpc=vpc
        )

        self.task_definition = _ecs.FargateTaskDefinition(
            self,
            "taskDefinition",
            memory_limit_mib=512,
            cpu=256
        )


        self.docker_image = _ecr_assets.DockerImageAsset(
            self,
            "dockerImage",
            directory="./code"
        )

        self.container = self.task_definition.add_container(
            "testContainer",
            image=_ecs.ContainerImage.from_docker_image_asset(self.docker_image),
            logging=_ecs.LogDriver.aws_logs(stream_prefix="containerlogs"),
            environment={
                "STAGE": "dev",
                "REDIS_ENDPOINT": redis.attr_configuration_end_point_address
            },
        )

        self.container.add_port_mappings(_ecs.PortMapping(container_port=5000, protocol=_ecs.Protocol.TCP))

        self.service = _ecs.FargateService(
            self,
            "fargateService",
            cluster=self.ecs_cluster,
            task_definition=self.task_definition,
            desired_count=3,
            vpc_subnets=_ec2.SubnetSelection(subnets=vpc.private_subnets),
            security_groups=[vpc.sg]
        )

        self.lb = _elbv2.ApplicationLoadBalancer(
            self,
            "alb",
            vpc=vpc,
            security_group=vpc.sg,
            internet_facing=True
        )

        listener = self.lb.add_listener("listener", port=80)

        self.target_group = listener.add_targets(
            "fargateTarget",
            port=80,
            targets=[self.service]
        )

        core.CfnOutput(self, "albDnsName", value=self.lb.load_balancer_dns_name)