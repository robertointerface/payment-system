import json
from typing import Union, Dict, MutableMapping
from pydantic import BaseModel
from handle_failure_lambda.database_connection import (
    get_database_connection,
    ERRORS_DATABASE_NAME)


class ErrorData(BaseModel):
    error_type: str
    error_cause: Union[str, MutableMapping]

    def format_mongodb(self):
        error_cause = self.error_cause
        if isinstance(error_cause, MutableMapping):
            error_cause = json.dumps(error_cause)
        return {
            "error_type": self.error_type,
            "error_cause": error_cause
        }


def lambda_handler(event, context):
    """Handle state machine errors.

    Errors are saved into the specified error database.

    Args:
        event: lambda event (Dictionary) containing passed error from previous
            state machine steps.
        context:
    """
    error_details = event.get('error_details')
    if error_details is None:
        raise ValueError(f'Error detail was not provided in Handle Failure Lambda')
    error_data = ErrorData(**error_details)
    mongo_client = get_database_connection()
    db = mongo_client[ERRORS_DATABASE_NAME]
    db['payment-errors'].insert_one(error_data.format_mongodb())
