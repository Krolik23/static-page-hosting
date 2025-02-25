from constructs import Construct
from imports.cf_module import CfModule

# Construct defining a CloudFront distribution for S3 static site hosting
class CloudFrontDistributionConstruct(Construct):
    def __init__(self, scope: Construct, id: str, s3_bucket: Construct):
        super().__init__(scope, id)
        self.distribution = self._create_distribution(s3_bucket)
    
    def _create_distribution(self, s3_bucket):
        return CfModule(self, "distribution",
            comment="Secure S3 hosting distribution",
            enabled=True,
            price_class="PriceClass_100", # Cost-optimized for US/EU regions
            wait_for_deployment=True, # Ensure deployment completes before proceeding
            create_origin_access_control=True,
            origin_access_control=self._oac_config(),
            origin=self._origin_config(s3_bucket),
            default_cache_behavior=self._cache_behavior(),
            default_root_object="static/index.html" # Entry point for the static site
        )
    
    # Configures Origin Access Control (OAC) for secure S3 access
    def _oac_config(self):
        return {
            "s3_oac": {
                "description": "Origin Access Control for S3",
                "origin_type": "s3",
                "signing_behavior": "always",
                "signing_protocol": "sigv4" # AWS recommended signing protocol
            }
        }
    
    # Defines S3 origin configuration with regional domain name
    def _origin_config(self, s3_bucket):
        return {
            "s3_oac": {
                "domain_name": s3_bucket.regional_domain_name,
                "origin_access_control": "s3_oac" # Reference to OAC config
            }
        }
    
    # Sets optimized caching and security headers policies
    def _cache_behavior(self):
        return {
            "target_origin_id": "s3_oac",
            "viewer_protocol_policy": "redirect-to-https", # Enforce HTTPS
            "allowed_methods": ["GET", "HEAD", "OPTIONS"], # Static site methods
            "cached_methods": ["GET", "HEAD"],
            "use_forwarded_values": "false", # Use managed cache policies instead
            "cache_policy_name": "Managed-CachingOptimized",
            "origin_request_policy_name": "Managed-UserAgentRefererHeaders",
            "response_headers_policy_name": "Managed-SimpleCORS"
        }
    
    # Returns CloudFront distribution ARN for policy attachments
    @property
    def arn(self):
        return self.distribution.cloudfront_distribution_arn_output

    # Returns CloudFront distribution domain name for output
    @property
    def cloudfront_url(self):
        return self.distribution.cloudfront_distribution_domain_name_output