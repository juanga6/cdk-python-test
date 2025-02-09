from aws_cdk import Stack
from aws_cdk import aws_codebuild as codebuild
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
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
        deploy_stage = pipeline.add_stage(deploy)

        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestViewerEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": deploy.hc_viewer_url},
                commands=["curl -Ssf $ENDPOINT_URL"],
            )
        )
        deploy_stage.add_post(
            pipelines.ShellStep(
                "TestAPIGatewayEndpoint",
                env_from_cfn_outputs={"ENDPOINT_URL": deploy.hc_endpoint},
                commands=[
                    "curl -Ssf $ENDPOINT_URL",
                    "curl -Ssf $ENDPOINT_URL/hello",
                    "curl -Ssf $ENDPOINT_URL/test",
                ],
            )
        )

        # Test stage
        test_stage = codebuild.PipelineProject(
            self,
            "TestStage",
            build_spec=codebuild.BuildSpec.from_object(
                {
                    "version": "0.2",
                    "phases": {
                        "install": {
                            "commands": [
                                "echo Installing dependencies...",
                                "pip install -r requirements-dev.txt",  # Instala las dependencias
                                "pip install pytest",  # Instala pytest
                            ],
                        },
                        "build": {
                            "commands": [
                                "echo Running tests...",
                                "pytest",  # Ejecuta pytest
                            ],
                        },
                    },
                    "artifacts": {
                        "files": ["**/*"],
                    },
                }
            ),
        )

        # Fase de la pipeline: Ejecutar pruebas con pytest
        pipeline.add_stage(
            stage_name="Test",
            actions=[
                codepipeline_actions.CodeBuildAction(
                    action_name="RunTests",
                    project=test_stage,
                    input=git_input,
                )
            ],
        )
