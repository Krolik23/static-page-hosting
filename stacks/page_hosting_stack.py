from cdktf import TerraformStack, TerraformOutput
from constructs import Construct
from constructs.s3.bucket import S3BucketConstruct
from constructs.cloudfront.distribution import CloudFrontDistributionConstruct
from constructs.static_page_content import StaticPageContentConstruct
from constructs.s3.policy import S3BucketPolicyConstruct

class PageHostingStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        
        # Initialize AWS provider
        self._configure_provider()
        
        # Create infrastructure components
        self.s3_bucket = S3BucketConstruct(self, "s3-hosting")
        self.static_content = StaticPageContentConstruct(
            self, "static-content", 
            self.s3_bucket
        )
        self.cloudfront = CloudFrontDistributionConstruct(
            self, "cloudfront-distro",
            self.s3_bucket
        )

        # Add policy for CloudFornt OAC access
        S3BucketPolicyConstruct(
            self, "s3-bucket-policy",
            s3_bucket=self.s3_bucket,
            cloudfront_arn=self.cloudfront.arn
        )

        ### Output
        # URL for accessing hosted static page
        TerraformOutput(self, "static_page_url",
            value = f"https://{self.cloudfront.cloudfront_url}"
        )

        # S3 bucket where files are hosted
        TerraformOutput(self, "s3_bucket_name",
            value = self.s3_bucket.bucket_id
        )

    def _configure_provider(self):
        from imports.aws.provider import AwsProvider
        AwsProvider(self, "aws", region="eu-central-1")