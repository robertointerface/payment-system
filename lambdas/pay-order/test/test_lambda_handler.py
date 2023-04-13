# ASSERT SOME METHODS ARE CALLED
from pay_order_lambda.lambda_handler import lambda_handler
from pay_order_lambda.database_connection import get_database_connection, \
    PAYMENT_SYSTEM_DATABASE_NAME

def test_lambda_reduces_user_credit_when_available_credit(order_id,
                                                          insert_users,
                                                          set_environ_variables):
    mongo_connection = get_database_connection()
    db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
    order_data = db.orders.find_one({'order_id': order_id})
    user_data_before_lambda = db.users.find_one({'user_id': order_data['user_id']})
    event_input = {
        "order_id": order_id
    }
    lambda_handler(event_input, {})
    updated_user_data = db.users.find_one({'user_id': order_data['user_id']})
    assert updated_user_data['credit'] < user_data_before_lambda['credit']

