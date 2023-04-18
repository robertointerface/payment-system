import os
from dataclasses import dataclass
from typing import Dict, Any

from stepfunctions.steps import (
    Pass,
    Retry,
    Chain,
    Catch,

    Choice,
    ChoiceRule,
    Task,
    Fail,
    LambdaStep)
from stepfunctions.steps.states import Parallel
from stepfunctions.workflow import Workflow


def create_main_state_machine() -> Dict[str, Any]:
    wrapped = wrap_pipeline_in_workflow()
    return wrapped.definition.to_dict()

ERROR_LAMBDA_TIMEOUT = 30
STANDARD_LAMBDA_TIMEOUT_SECONDS = 30

@dataclass()
class StateMachineTags:
    START_STATE_MACHINE = "Start State Machine"
    ORDER_PRODUCTS_AVAILABLE = "Check order products are available"
    PAYMENT_ORDER = "Process order payment"
    HANDLE_LAMBDA_FAILURE = "Handle failure"
    FINISHED_STATE_MACHINE = "Order placed"
    FAILED_STATUS = "Payment Failed"

@dataclass
class ArnReferences:
    CHECK_ORDER_PRODUCTS_ARE_AVAILABLE_ARN = "${OrderProductsAvailableLambdaArn}"
    PAYMENT_ORDER_ARN = "${PaymentOrderLambdaArn}"
    HANDLE_LAMBDA_FAILURE_ARN = "${HandleFailureLambdaArn}"

initialise_step = Pass(
    state_id=StateMachineTags.START_STATE_MACHINE
)
finish_payment_state_machine = Pass(
    state_id=StateMachineTags.FINISHED_STATE_MACHINE
)
failed_status = Fail(state_id=StateMachineTags.FAILED_STATUS)


def create_error_lambda_handler():
    error_lambda = LambdaStep(
        state_id=StateMachineTags.HANDLE_LAMBDA_FAILURE,
        parameters={
            "FunctionName": ArnReferences.HANDLE_LAMBDA_FAILURE_ARN,
            "Payload": {
                "order_id.$": "$.order_id",
                "error_details": {
                    "error_type.$": "$.error.Error",
                    "error_cause.$": "$.error.Cause"
                }
            }
        },
        timeout_seconds=ERROR_LAMBDA_TIMEOUT,
        input_path='$'
    )
    retry = Retry(interval_seconds=10,
                  max_attempts=1,
                  error_equals=["States.ALL"])
    error_lambda.add_retry(retry)
    error_lambda.next_step = failed_status
    return error_lambda


def create_check_products_availability_lambda():
    check_products_lambda = LambdaStep(
        state_id=StateMachineTags.ORDER_PRODUCTS_AVAILABLE,
        parameters={
            "FunctionName": ArnReferences.CHECK_ORDER_PRODUCTS_ARE_AVAILABLE_ARN,
            "Payload.$": "$"
        },
        timeout_seconds=STANDARD_LAMBDA_TIMEOUT_SECONDS,
        input_path="$"
    )
    retry = Retry(
        interval_seconds=10,
        max_attempts=1,
        error_equals=['States.ALL']
    )
    check_products_lambda.add_retry(retry)
    return check_products_lambda


def create_payment_order_lambda():
    payment_lambda = LambdaStep(
        state_id=StateMachineTags.PAYMENT_ORDER,
        parameters={
            "FunctionName": ArnReferences.CHECK_ORDER_PRODUCTS_ARE_AVAILABLE_ARN,
            "Payload.$": "$"
        },
        timeout_seconds=STANDARD_LAMBDA_TIMEOUT_SECONDS,
        input_path="$"
    )
    retry = Retry(
        interval_seconds=10,
        max_attempts=1,
        error_equals=['States.ALL']
    )
    payment_lambda.add_retry(retry)
    return payment_lambda



def create_payment_state_machine_definition():
    check_product_availability_lambda = create_check_products_availability_lambda()
    payment_order_lambda = create_payment_order_lambda()
    catch = Catch(
        error_equals=["States.ALL"],
        next_step=create_error_lambda_handler(),
        result_path="$.error"
    )
    check_product_availability_lambda.add_catch(catch)
    payment_order_lambda.add_catch(catch)
    return Chain([check_product_availability_lambda,
                  payment_order_lambda,
                  finish_payment_state_machine])


def create_payment_state_machine() -> Workflow:

    workflow = Workflow(
        name=f'payment-statemachine',
        definition=create_payment_state_machine_definition(),
        role="arn:aws:iam::858290205983:role/step-functions-control-role"
    )
    return workflow


# if __name__ == "__main__":
#     import boto3
#     import json
#     st_input = {
#         "order_id": "311b559c-2dde-4a95-b7a3-30fbf60a2d9c"
#     }
#     client = boto3.client('stepfunctions')
#     execution = client.start_execution(
#         stateMachineArn="arn:aws:states:eu-west-2:858290205983:stateMachine:process-payment",
#         input=json.dumps(st_input))