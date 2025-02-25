from cdktf import TerraformStack, TerraformOutput
from constructs import Construct
from constructs.s3.bucket import S3BucketConstruct
from constructs.cloudfront.distribution import CloudFrontDistributionConstruct
from constructs.static_page_content import StaticPageContentConstruct
from constructs.s3.policy import S3BucketPolicyConstruct

# Main CDKTF stack defining the complete static site hosting infrastructure.
class PageHostingStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)
        
        # Initialize AWS provider with specified region
        self._configure_provider()
        
        # Infrastructure components (order matters for dependencies)
        # 1. Create S3 bucket for hosting static content
        self.s3_bucket = S3BucketConstruct(self, "s3-hosting")

        # 2. Upload HTML content to S3 (depends on bucket creation)
        self.static_content = StaticPageContentConstruct(
            self, "static-content", 
            self.s3_bucket
        )

        # 3. Create CloudFront distribution (depends on S3 bucket)
        self.cloudfront = CloudFrontDistributionConstruct(
            self, "cloudfront-distro",
            self.s3_bucket
        )

        # 4. Attach security policy to S3 bucket (depends on CloudFront ARN)
        S3BucketPolicyConstruct(
            self, "s3-bucket-policy",
            s3_bucket=self.s3_bucket,
            cloudfront_arn=self.cloudfront.arn
        )

        ### Outputs for easy access to deployed resources
        # Public URL for accessing the hosted static site
        TerraformOutput(self, "static_page_url",
            value = f"https://{self.cloudfront.cloudfront_url}"
        )

        # Name of the created S3 bucket for reference
        TerraformOutput(self, "s3_bucket_name",
            value = self.s3_bucket.bucket_id
        )

    # Configures the AWS provider with default Frankfurt (eu-central-1) region
    def _configure_provider(self):
        from imports.aws.provider import AwsProvider
        AwsProvider(self, "aws", region="eu-central-1")