from aws_cdk import Stack
from aws_cdk import (
    pipelines as pipelines,
)
from constructs import Construct

from .pipeline_stage import WorkshopPipelineStage


class WorkshopPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        git_input = pipelines.CodePipelineSource.connection(
            repo_string="juanga6/cdk-python-test",
            branch="main",
            connection_arn="arn:aws:codeconnections:eu-north-1:724772078988:connection/124f0516-1e00-4f7c-a97b-f3e2b5651142",
        )

        pipeline = pipelines.CodePipeline(
            self,
            "Pipeline",
            synth=pipelines.ShellStep(
                "Synth",
                input=git_input,
                commands=[
                    "npm install -g aws-cdk",  # Installs the cdk cli on Codebuild
                    "pip install -r requirements.txt",  # Instructs Codebuild to install required packages
                    "cdk synth",
                ],
            ),
        )

        deploy = WorkshopPipelineStage(self, "Deploy")
        pipeline.add_stage(deploy)
