import os
import pathlib
import json
import pytest
import pymongo
from arrange_delivery_lambda import database_connection as mongo_init

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

