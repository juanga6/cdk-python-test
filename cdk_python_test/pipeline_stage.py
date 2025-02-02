from aws_cdk import Stage
from cdk_python_test_stack import CdkPythonTestStack
from constructs import Construct


class WorkshopPipelineStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        CdkPythonTestStack(self, "WebService")
