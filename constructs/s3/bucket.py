from constructs import Construct
from imports.s3_module import S3Module

# Construct for secure S3 bucket configuration with encryption and versioning enabled
class S3BucketConstruct(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        self.bucket = self._create_bucket()
    
    def _create_bucket(self):
        return S3Module(self, "bucket",
            bucket_prefix="lab-account-bucket-", # Avoid bucket name collisions
            versioning={"enabled": "True"}, # Enable versioning for rollbacks
            force_destroy=True, # Allow bucket deletion with contents during destroy
            server_side_encryption_configuration={
                "rule": {
                    "bucket_key_enabled": True, # Reduce encryption costs
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256" # AWS-managed encryption
                    }
                }
            }
        )
    
    # S3 bucket ARN for policy references
    @property
    def arn(self):
        return self.bucket.s3_bucket_arn_output

    # Physical bucket name for resource references
    @property
    def bucket_id(self):
        return self.bucket.s3_bucket_id_output
    
    # Regional domain name for CloudFront origin configuration
    @property
    def regional_domain_name(self):
        return self.bucket.s3_bucket_bucket_regional_domain_name_output
    