import pytest
import pathlib
import json
from arrange_delivery_lambda.database_connection import (
    get_database_connection,
    PAYMENT_SYSTEM_DATABASE_NAME)
from arrange_delivery_lambda.lambda_handler import lambda_handler

TEST_DATA_PATH = pathlib.Path(__file__).parent / 'test_data'


@pytest.fixture
def insert_order_in_database():
    order_file = TEST_DATA_PATH / "order_data.json"
    order_data = json.loads(order_file.read_text())
    mongo_client = get_database_connection()
    db = mongo_client[PAYMENT_SYSTEM_DATABASE_NAME]
    db['orders'].insert_one(order_data)
    return order_data


def test_lambda_handler_saves_deliveries(insert_order_in_database):
    event = {
        "order_id": insert_order_in_database['order_id']
    }
    lambda_handler(event, {})
    mongo_client = get_database_connection()
    db = mongo_client[PAYMENT_SYSTEM_DATABASE_NAME]
    for product in insert_order_in_database['products']:
        related_delivery = db['deliveries'].find_one({'product_id': product['product_id']})
        assert related_delivery is not None