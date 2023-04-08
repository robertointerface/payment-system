import os
from typing import Type
from check_product_availability_lambda.data_getters import MongoOrderDataGetter
ALLOWED_ORDER_DATA_GETTERS = ('REST_API', "MongoDb")


def order_data_getter_factory() -> Type[MongoOrderDataGetter]:
    """
    Factory to choose the class that retrieves order data.

    Order data could be retrieved from any type of database, rest api,
        graphql... In order to have modularity we implement this factory that
        returns a class that MUST follow protocols stablished on class
        OrderDataGetter.

    Returns:
        Class that follows protocol 'OrderDataGetter' to extract order data.
    Raises:
        ValueError if the methodology was not specified or specified incorrect.
    """
    data_getter_methodology = os.environ.get('ORDER_DATA_GETTER')
    if (data_getter_methodology is None
        or
        data_getter_methodology not in ALLOWED_ORDER_DATA_GETTERS):
        raise ValueError(f'Specified order data getter was not defined or the'
                         f' specified methodology "{data_getter_methodology}" '
                         f'is not implemented.')
    if data_getter_methodology == "MongoDb":
        return MongoOrderDataGetter
