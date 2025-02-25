from constructs import Construct
from imports.aws.data_aws_iam_policy_document import DataAwsIamPolicyDocument
from imports.aws.s3_bucket_policy import S3BucketPolicy

class S3BucketPolicyConstruct(Construct):
    def __init__(self, scope: Construct, id: str, s3_bucket: Construct, cloudfront_arn: str):
        super().__init__(scope, id)
        
        self.policy_document = DataAwsIamPolicyDocument(self, "s3-policy-doc",
            statement=[{
                "actions": ["s3:GetObject"],
                "resources": [f"{s3_bucket.arn}/static/*"],
                "principals": [{
                    "type": "Service",
                    "identifiers": ["cloudfront.amazonaws.com"]
                }],
                "condition": [{
                    "test": "StringEquals",
                    "variable": "aws:SourceArn",
                    "values": [cloudfront_arn]
                }]
            }]
        )

        S3BucketPolicy(self, "s3-bucket-policy",
            # bucket=bucket_arn.split(':::')[-1],  # Extract bucket name from ARN
            bucket=s3_bucket.bucket_id,
            policy=self.policy_document.json
        )