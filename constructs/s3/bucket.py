from constructs import Construct
from imports.s3_module import S3Module

class S3BucketConstruct(Construct):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        self.bucket = self._create_bucket()
    
    def _create_bucket(self):
        return S3Module(self, "bucket",
            bucket_prefix="lab-account-bucket-",
            versioning={"enabled": "True"},
            force_destroy=True,
            server_side_encryption_configuration={
                "rule": {
                    "bucket_key_enabled": True,
                    "apply_server_side_encryption_by_default": {
                        "sse_algorithm": "AES256"
                    }
                }
            }
        )
    
    @property
    def arn(self):
        return self.bucket.s3_bucket_arn_output

    @property
    def bucket_id(self):
        return self.bucket.s3_bucket_id_output
    
    @property
    def regional_domain_name(self):
        return self.bucket.s3_bucket_bucket_regional_domain_name_output
    