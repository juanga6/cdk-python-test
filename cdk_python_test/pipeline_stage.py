from aws_cdk import Stage
from constructs import Construct

from .cdk_python_test_stack import CdkPythonTestStack


class WorkshopPipelineStage(Stage):
    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        CdkPythonTestStack(self, "WebService")
