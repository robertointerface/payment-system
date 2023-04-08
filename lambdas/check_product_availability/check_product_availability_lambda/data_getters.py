from abc import ABC, abstractmethod


class OrderDataGetter(ABC):

    @abstractmethod
    def get_order_data(self, order_id: str):
        pass


class MongoOrderDataGetter(OrderDataGetter):

    @abstractmethod
    def get_order_data(self, order_id: str):
        pass


