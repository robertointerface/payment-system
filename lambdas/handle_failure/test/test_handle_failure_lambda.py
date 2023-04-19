from handle_failure_lambda.lambda_handler import lambda_handler
from handle_failure_lambda.database_connection import (
    get_database_connection,
    ERRORS_DATABASE_NAME)


def test_passed_error_is_saved_in_database():
    event = {
        "error_details": {
            "error_type": "ValueError",
            "error_cause": "Payment Could not be processed"
        }
    }
    lambda_handler(event, {})
    mongo_client = get_database_connection()
    db = mongo_client[ERRORS_DATABASE_NAME]
    saved_error = db['payment-errors'].find_one({"error_type": "ValueError"})
    assert saved_error is not None
