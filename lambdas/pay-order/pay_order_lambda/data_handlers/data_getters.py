from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel

from pay_order_lambda.database_connection import get_database_connection, \
    PAYMENT_SYSTEM_DATABASE_NAME


class ProductData(BaseModel):
    product_id: str
    price: float
    requested_count: int


# LOOK at discount on the fluent python recipe we had
class OrderData(BaseModel):
    order_id: str
    user_id: str
    products: List[ProductData]

    def total_payment(self):
        pass


class OrderDataGetter(ABC):
    """Abstract class for order data getter, class dictates the interface/protocols
    of the classes which purpose is to get order data."""
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
    """
    Get order data from mongodb.
    """
    def __init__(self):
        self.__raw_order_data = None

    def get_order_data(self, order_id: str):
        """Get the order data from mongodb with the specified database
            configurations. The order information is saved inside attribute
            __raw_order_data so later it can be converted to any specified format.

        Args:
            order_id: The order id
        """
        mongo_connection = get_database_connection()
        db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
        order_data = db.orders.find_one(
            {'order_id': order_id},
            {"order_id": 1, 'user_id': 1, 'products': 1})
        if order_data is None:
            msg = f"""order with id {order_id} could not be found on 
            Mongo database {PAYMENT_SYSTEM_DATABASE_NAME} on collection orders"""
            raise OrderNotFoundException(msg)
        self.__raw_order_data = order_data

    @property
    def order_data(self) -> OrderData:
        """Convert extracted data into dataclass OrderData"""
        return OrderData(**self.__raw_order_data)
