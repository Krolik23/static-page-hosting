from constructs import Construct
from imports.cf_module import CfModule

class CloudFrontDistributionConstruct(Construct):
    def __init__(self, scope: Construct, id: str, s3_bucket: Construct):
        super().__init__(scope, id)
        self.distribution = self._create_distribution(s3_bucket)
    
    def _create_distribution(self, s3_bucket):
        return CfModule(self, "distribution",
            comment="Secure S3 hosting distribution",
            enabled=True,
            price_class="PriceClass_100",
            wait_for_deployment=True,
            create_origin_access_control=True,
            origin_access_control=self._oac_config(),
            origin=self._origin_config(s3_bucket),
            default_cache_behavior=self._cache_behavior(),
            default_root_object="static/index.html"
        )
    
    def _oac_config(self):
        return {
            "s3_oac": {
                "description": "Origin Access Control for S3",
                "origin_type": "s3",
                "signing_behavior": "always",
                "signing_protocol": "sigv4"
            }
        }
    
    def _origin_config(self, s3_bucket):
        return {
            "s3_oac": {
                "domain_name": s3_bucket.regional_domain_name,
                "origin_access_control": "s3_oac"
            }
        }
    
    def _cache_behavior(self):
        return {
            "target_origin_id": "s3_oac",
            "viewer_protocol_policy": "redirect-to-https",
            "allowed_methods": ["GET", "HEAD", "OPTIONS"],
            "cached_methods": ["GET", "HEAD"],
            "use_forwarded_values": "false",
            "cache_policy_name": "Managed-CachingOptimized",
            "origin_request_policy_name": "Managed-UserAgentRefererHeaders",
            "response_headers_policy_name": "Managed-SimpleCORS"
        }
    
    @property
    def arn(self):
        return self.distribution.cloudfront_distribution_arn_output

    @property
    def cloudfront_url(self):
        return self.distribution.cloudfront_distribution_domain_name_output