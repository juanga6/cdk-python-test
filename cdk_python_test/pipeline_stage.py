from aws_cdk import Stage
from constructs import Construct

from .cdk_python_test_stack import CdkPythonTestStack


class WorkshopPipelineStage(Stage):
    @property
    def hc_endpoint(self):
        return self._hc_endpoint

    @property
    def hc_viewer_url(self):
        return self._hc_viewer_url

    def __init__(self, scope: Construct, id: str, **kwargs):
        super().__init__(scope, id, **kwargs)

        service = CdkPythonTestStack(self, "WebService")

        self._hc_endpoint = service.hc_endpoint
        self._hc_viewer_url = service.hc_viewer_url
