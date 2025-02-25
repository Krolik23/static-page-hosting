from cdktf import App
from stacks.page_hosting_stack import PageHostingStack

# Main CDKTF application entry point
# Defines the infrastructure stack for static site hosting
app = App()
PageHostingStack(app, "static-site-hosting")
app.synth()