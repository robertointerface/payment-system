import os
from abc import ABC, abstractmethod
import pymongo
import urllib
# from boto3 import Session
# from botocore.credentials import ReadOnlyCredentials

MONGO_CONNECTION = None
MONGO_CONNECTION_PORT = 27017
PAYMENT_SYSTEM_DATABASE_NAME = os.environ['PAYMENT_SYSTEM_DATABASE_NAME']


class MongoDbConnection(ABC):

    @abstractmethod
    def get_connection_string(self):
        pass


class MongoDbLocalConnection(MongoDbConnection):

    def get_connection_string(self):
        return f'mongodb://localhost:{MONGO_CONNECTION_PORT}'


def connect_to_mongo():
    connection_string = f"mongodb+srv://User_name:Password$@Cluster_Name.mmdvvxm.mongodb.net/?retryWrites=true&w=majority"
    client = pymongo.MongoClient(connection_string)
    return client


def get_database_connection():
    global MONGO_CONNECTION
    if MONGO_CONNECTION is None:
        MONGO_CONNECTION = connect_to_mongo()
    return MONGO_CONNECTION