import os
from abc import ABC, abstractmethod
import pymongo
from arrange_delivery_lambda.utils import get_current_user_or_role_credentials
import urllib
MONGO_CONNECTION = None
MONGO_CONNECTION_PORT = 27017
PAYMENT_SYSTEM_DATABASE_NAME = os.environ['PAYMENT_SYSTEM_DATABASE_NAME']
DATABASE_CLUSTER_DOMAIN = os.environ['DATABASE_CLUSTER_DOMAIN']


class MongoDbConnection(ABC):

    @abstractmethod
    def get_connection_string(self) -> str:
        pass


class MongoDbLocalConnection(MongoDbConnection):
    """
    Connect to mongodb to local mongodb, mostly for testing.
    """
    def get_connection_string(self) -> str:
        return f'mongodb://localhost:{MONGO_CONNECTION_PORT}'


class MongoDbConnectByAwsRoleCredentials(MongoDbConnection):
    """
    Connect to Mongodb using AWS Role Credentials.
    """
    def get_connection_string(self) -> str:
        current_credentials = get_current_user_or_role_credentials()
        access_key = urllib.parse.quote_plus(current_credentials.access_key)
        secret_key = urllib.parse.quote_plus(current_credentials.secret_key)
        session_token = urllib.parse.quote_plus(current_credentials.token)
        return f"mongodb+srv://{access_key}:{secret_key}@practice.mmdvvxm.mongodb.net/?authSource=%24external&authMechanism=MONGODB-AWS&retryWrites=true" \
                            f"&w=majority&authMechanismProperties=AWS_SESSION_TOKEN:{session_token}"


def connect_to_mongo() -> pymongo.mongo_client:
    """Connect to mongodb with one of the given options.

    Returns:
        pymongo client
    """
    if DATABASE_CLUSTER_DOMAIN == 'localhost':
        connection_string = MongoDbLocalConnection().get_connection_string()
    else:
        connection_string = MongoDbConnectByAwsRoleCredentials().get_connection_string()
    client = pymongo.MongoClient(connection_string)
    return client


def get_database_connection() -> pymongo.mongo_client:
    """Get the mongodb connection by Pymongo or initialise and return if it
    has NOT been initialised."""
    global MONGO_CONNECTION
    if MONGO_CONNECTION is None:
        MONGO_CONNECTION = connect_to_mongo()
    return MONGO_CONNECTION
