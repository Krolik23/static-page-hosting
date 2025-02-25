from cdktf import Fn, TerraformAsset
from constructs import Construct
import os
from datetime import datetime
from imports.s3_object_module import S3ObjectModule

class StaticPageContentConstruct(Construct):
    def __init__(self, scope: Construct, id: str, s3_bucket: Construct):
        super().__init__(scope, id)
        self.asset = self._create_asset()
        self._upload_content(s3_bucket)
    
    def _create_asset(self):
        return TerraformAsset(self, "html-asset",
            path=os.path.join(os.path.dirname(__file__), "../resources/static/index.html.tmpl")
        )
    
    def _upload_content(self, s3_bucket):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        S3ObjectModule(self, "static-page",
            key="static/index.html",
            bucket=s3_bucket.bucket.s3_bucket_id_output,
            content=Fn.templatefile(self.asset.path, {"timestamp": timestamp}),
            content_type="text/html",
            source_hash=Fn.filemd5(self.asset.path)
        )