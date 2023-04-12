"""Describe the data handler strategies, data handles are in charge of fectching
and updating data to third parties like SQL or Rest Apis..."""
from check_product_availability_lambda.data_handlers.data_getters import  MongoOrderDataGetter
from check_product_availability_lambda.data_handlers.data_updater import \
    UpdateProductsMongo
from check_product_availability_lambda.data_handlers.product_availability_checker import check_product_availability


class MongoDbDataHandlers:
    """Defines Mongodb Data handlers"""
    order_data_getters = MongoOrderDataGetter
    check_product_availability = check_product_availability
    product_updater = UpdateProductsMongo
