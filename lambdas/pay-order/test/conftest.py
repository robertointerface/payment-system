import os
import pathlib
import json
import pytest
import pymongo
from check_product_availability_lambda import database_connection as mongo_init

TEST_DATA_PATH = pathlib.Path(__file__).parent / "test_data"


@pytest.fixture(autouse=True)
def replace_mongodb_with_mockdb():
    if mongo_init.MONGO_CONNECTION is None:
        mongo_connection = mongo_init.MongoDbLocalConnection()
        connection_string = mongo_connection.get_connection_string()
        mongo_init.MONGO_CONNECTION = pymongo.MongoClient(connection_string)
    # here we don't delete/stop the connection to mongoengine, what we do
    # is delete the data inside the database but we still keep the connection
    # IS IMPORTANT THAT YOU AWAIT FOR THE drop_database OTHERWISE TESTS MIGHT
    # FAIL AS THEY ARE NOT SYNCHRONIZE AND THE DATABASE CAN BE DROPING THE
    # DATA WHILE TESTS ARE BEING DONE AND THAT RAISES UNEXPECTED ERRORS
    mongo_init.MONGO_CONNECTION.drop_database(mongo_init.PAYMENT_SYSTEM_DATABASE_NAME)


@pytest.fixture(name='products_data')
def load_product_data_in_database():
    products_data_file = TEST_DATA_PATH / "products_data.json"
    products = json.loads(products_data_file.read_text())
    db = mongo_init.MONGO_CONNECTION[mongo_init.PAYMENT_SYSTEM_DATABASE_NAME]
    _ = db.products.insert_many(products)
    return products


@pytest.fixture(name='products_data_non_available')
def load_product_data_with_non_available_products_in_database():
    products_data_file = TEST_DATA_PATH / "products_data_not_available.json"
    products = json.loads(products_data_file.read_text())
    db = mongo_init.MONGO_CONNECTION[mongo_init.PAYMENT_SYSTEM_DATABASE_NAME]
    _ = db.products.insert_many(products)
    return products


@pytest.fixture(name="order_id")
def load_order_data_in_database():
    orders_data_file = TEST_DATA_PATH / "order_data.json"
    order = json.loads(orders_data_file.read_text())
    db = mongo_init.MONGO_CONNECTION[mongo_init.PAYMENT_SYSTEM_DATABASE_NAME]
    _ = db.orders.insert_one(order)
    return order['order_id']


@pytest.fixture
def set_environ_variables():
    os.environ['ORDER_DATA_GETTER'] = 'MongoDb'
