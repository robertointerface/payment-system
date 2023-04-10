import pytest
import os
from check_product_availability_lambda.database_connection import \
    get_database_connection, PAYMENT_SYSTEM_DATABASE_NAME
from check_product_availability_lambda.exceptions import \
    ProductsNotAvailableException
from check_product_availability_lambda.lambda_handler import lambda_handler


def test_lambda_handler_updates_database_correctly(products_data,
                                                   order_id,
                                                   set_environ_variables):
    """Assert the lambda handler updates the field available_count on the product
        document correctly, that is the
        available count = current available count - number of products requested by the user.
        I.E if there are 5 books available and the user wants to buy 3, after the
        lambda the products database should reflect only 2 available."""

    event = {"order_id": order_id}
    # First calculate the expected products available count, load the product
    # data from database before we call the lambda handler and calculate the
    # expected available count = current available count - number of items that will be requested.
    # this needs to be done before calling the lambda as in the lambda we update
    # the products collection.
    expected_products_available_count = {}
    mongo_connection = get_database_connection()
    db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
    order_data = db.orders.find_one({"order_id": order_id})
    for requested_product in order_data["products"]:
        product_id = requested_product["product_id"]
        product_data = db.products.find_one(
            {"product_id": product_id})
        expected_products_available_count[product_id] = product_data['available_count'] - requested_product["requested_count"]
    # call the lambda and assert the products available count has been updated
    # accordingly
    lambda_handler(event, {})
    order_data = db.orders.find_one({"order_id": order_id})
    for requested_product in order_data["products"]:
        product_id = requested_product["product_id"]
        product_data = db.products.find_one({"product_id": product_id})
        assert product_data["available_count"] == expected_products_available_count[product_id], \
            f"""Product with id = {product_id} is expected to have field 'available_count' = {expected_products_available_count[product_id]}
             after labmda is called"""


def test_lambda_handler_raises_ProductsNotAvailableException_when_products_are_not_available(
        products_data_non_available,
        order_id,
        set_environ_variables):
    os.environ['ORDER_DATA_GETTER'] = 'MongoDb'
    event = {"order_id": order_id}
    with pytest.raises(ProductsNotAvailableException):
        lambda_handler(event, {})
