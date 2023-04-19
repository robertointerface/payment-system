import pytest
import pymongo
from handle_failure_lambda import database_connection as mongo_init


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
    mongo_init.MONGO_CONNECTION.drop_database(mongo_init.ERRORS_DATABASE_NAME)


