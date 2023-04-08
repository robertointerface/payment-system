from abc import ABC, abstractmethod
from dataclasses import dataclass
from check_product_availability_lambda.database_connection import (
    get_database_connection,
    PAYMENT_SYSTEM_DATABASE_NAME)
from check_product_availability_lambda.exceptions import OrderNotFoundException


@dataclass
class OrderData:
    product_id: str
    name: str
    price: float
    requested_count: int
    delivery_address: str
    type: str = None


class OrderDataGetter(ABC):

    @abstractmethod
    def __init__(self):
        self.__order_data = None

    @abstractmethod
    def get_order_data(self, order_id: str):
        pass

    @property
    @abstractmethod
    def order_data(self) -> OrderData:
        pass


class MongoOrderDataGetter(OrderDataGetter):

    def __init__(self):
        self.__raw_order_data = None

    def get_order_data(self, order_id: str):
        # call mongodb and query by order id
        mongo_connection = get_database_connection()
        db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
        order_data = db.orders.find_one({'order_id': order_id})
        if order_data is None:
            msg = f"""order with id {order_id} could not be found on 
            Mongo database {PAYMENT_SYSTEM_DATABASE_NAME} on collection orders"""
            raise OrderNotFoundException(msg)
        self.__raw_order_data = order_data

    @property
    def order_data(self) -> OrderData:
        pass
