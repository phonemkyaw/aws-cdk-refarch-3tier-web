from aws_cdk import core
from aws_cdk import aws_s3 as _s3
from aws_cdk import aws_cloudfront as _cf

class CdnStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, alb, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        self.website_bucket = _s3.Bucket(
            self,
            "websiteBucket",
            website_index_document="index.html",
            website_error_document="error.html",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        self.static_bucket = _s3.Bucket(
            self,
            "staticBucket",
            removal_policy=core.RemovalPolicy.DESTROY
        )

        # Website
        web_behavior = _cf.Behavior(
            is_default_behavior=True,
            default_ttl=core.Duration.minutes(0)
        )
        web_source_config = _cf.SourceConfiguration(
            behaviors=[web_behavior],
            s3_origin_source=_cf.S3OriginConfig(s3_bucket_source=self.website_bucket)
        )

        # Static Content
        static_behavior = _cf.Behavior(
            path_pattern="images/*",
            default_ttl=core.Duration.minutes(0)
        )
        static_source_config = _cf.SourceConfiguration(
            behaviors=[static_behavior],
            s3_origin_source=_cf.S3OriginConfig(s3_bucket_source=self.static_bucket)
        )

        # ALB
        alb_behavior = _cf.Behavior(
            path_pattern="api/*",
            allowed_methods=_cf.CloudFrontAllowedMethods.ALL,
            default_ttl=core.Duration.minutes(0)
        )
        alb_source_config = _cf.SourceConfiguration(
            behaviors=[alb_behavior],
            custom_origin_source=_cf.CustomOriginConfig(
                domain_name=alb.load_balancer_dns_name,
                origin_protocol_policy=_cf.OriginProtocolPolicy.HTTP_ONLY)
        )

        self.cf = _cf.CloudFrontWebDistribution(
            self,
            "cfDistribution",
            price_class=_cf.PriceClass.PRICE_CLASS_100,
            origin_configs=[web_source_config, static_source_config, alb_source_config]
        )

        # self.cf.add_behaviour(
        #     path_pattern="/static",
        #     origin=static_origin
        # )
        # core.CfnOutput(self, "outputSg", value=self.vpc_sg.security_group_id)
