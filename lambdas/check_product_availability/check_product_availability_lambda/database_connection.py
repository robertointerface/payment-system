import json
import os
from abc import ABC, abstractmethod
import pymongo
from check_product_availability_lambda.utils import get_string_secret

MONGO_CONNECTION = None
MONGO_CONNECTION_PORT = 27017
PAYMENT_SYSTEM_DATABASE_NAME = os.environ['PAYMENT_SYSTEM_DATABASE_NAME']
DATABASE_USERNAME_SECRET = os.environ['DATABASE_USERNAME_SECRET']
DATABASE_PASSWORD_SECRET = os.environ['DATABASE_PASSWORD_SECRET']
DATABASE_CLUSTER_SECRET = os.environ['DATABASE_CLUSTER_SECRET']


class MongoDbConnection(ABC):

    @abstractmethod
    def get_connection_string(self):
        pass


class MongoDbLocalConnection(MongoDbConnection):

    def get_connection_string(self):
        return f'mongodb://localhost:{MONGO_CONNECTION_PORT}'


def connect_to_mongo():
    user_name = json.loads(get_string_secret(secret_name=DATABASE_USERNAME_SECRET,
                                             region_name="eu-west-2"))['DATABASE_USERNAME_SECRET']
    password = json.loads(get_string_secret(secret_name=DATABASE_PASSWORD_SECRET,
                                 region_name="eu-west-2"))['DATABASE_PASSWORD_SECRET']
    cluster_name = json.loads(get_string_secret(secret_name=DATABASE_CLUSTER_SECRET,
                                     region_name="eu-west-2"))['DATABASE_CLUSTER_SECRET']
    connection_string = f"mongodb+srv://{user_name}:{password}" \
                        f"@{cluster_name}.mmdvvxm.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    return client


def get_database_connection():
    global MONGO_CONNECTION
    if MONGO_CONNECTION is None:
        MONGO_CONNECTION = connect_to_mongo()
    return MONGO_CONNECTION
