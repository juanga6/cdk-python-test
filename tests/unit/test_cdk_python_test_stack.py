import pytest
from aws_cdk import Stack, assertions
from aws_cdk import aws_lambda as _lambda

from cdk_python_test.hitcounter import HitCounter


def test_dynamodb_table_created():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
        ),
    )
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 1)


def test_lambda_has_env_vars():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
        ),
    )

    template = assertions.Template.from_stack(stack)
    envCapture = assertions.Capture()

    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "hitcount.handler",
            "Environment": envCapture,
        },
    )

    assert envCapture.as_object() == {
        "Variables": {
            "DOWNSTREAM_FUNCTION_NAME": {"Ref": "TestFunction22AD90FC"},
            "HITS_TABLE_NAME": {"Ref": "HitCounterHits079767E5"},
        },
    }


def test_dynamodb_with_encryption():
    stack = Stack()
    HitCounter(
        stack,
        "HitCounter",
        downstream=_lambda.Function(
            stack,
            "TestFunction",
            runtime=_lambda.Runtime.PYTHON_3_7,
            handler="hello.handler",
            code=_lambda.Code.from_asset("lambda"),
        ),
    )

    template = assertions.Template.from_stack(stack)
    template.has_resource_properties(
        "AWS::DynamoDB::Table",
        {
            "SSESpecification": {
                "SSEEnabled": True,
            },
        },
    )


def test_dynamodb_raises():
    stack = Stack()
    with pytest.raises(Exception):
        HitCounter(
            stack,
            "HitCounter",
            downstream=_lambda.Function(
                stack,
                "TestFunction",
                runtime=_lambda.Runtime.PYTHON_3_7,
                handler="hello.handler",
                code=_lambda.Code.from_asset("lambda"),
            ),
            read_capacity=1,
        )
