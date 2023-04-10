from typing import List
from pymongo import UpdateOne
from check_product_availability_lambda.data_getters import ProductData
from check_product_availability_lambda.database_connection import \
    get_database_connection, PAYMENT_SYSTEM_DATABASE_NAME


class UpdateProductsMongo:

    def __init__(self, products: List[ProductData]):
        self.products = products

    def create_mongodb_update_operation(self, product: ProductData):
        pipeline = [
            {
                "$set": {
                    "available_count": {
                        '$subtract': ['$available_count',
                                      product.requested_count]
                    }
                }
            }
        ]
        return UpdateOne({"product_id": product.product_id},
                         pipeline)

    def update(self):
        mongo_connection = get_database_connection()
        db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
        update_operations = [self.create_mongodb_update_operation(product)
                             for product in self.products]
        db.products.bulk_write(update_operations)