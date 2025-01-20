#!/usr/bin/env python3

import aws_cdk as cdk

from cdk_python_test.pipeline_stack import WorkshopPipelineStack

app = cdk.App()
WorkshopPipelineStack(app, "WorkshopPipelineStack")

app.synth()
