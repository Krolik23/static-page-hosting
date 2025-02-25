from cdktf import App
from stacks.page_hosting_stack import PageHostingStack

app = App()
PageHostingStack(app, "static-site-hosting")
app.synth()