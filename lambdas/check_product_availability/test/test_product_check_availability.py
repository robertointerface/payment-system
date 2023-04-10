import uuid

import random

from check_product_availability_lambda.data_handlers.data_getters import ProductData
from check_product_availability_lambda.data_handlers.product_availability_checker import \
    check_product_availability

random.seed()


def test_check_product_availability_returns_true_when_product_available(products_data):
    test_product = products_data[random.randint(0, len(products_data) - 1)]
    product_data = ProductData(
        product_id=test_product["product_id"],
        name=test_product["name"],
        price=test_product["price"],
        requested_count=test_product["available_count"] if test_product["available_count"] <= 1 else test_product["available_count"] - 1,
        delivery_address=str(uuid.uuid4()),
        type=test_product["type"]
    )
    is_product_available = check_product_availability(product_data)
    assert is_product_available, f"Product should be available, product available " \
                                 f"count = {test_product['available_count']} product requested buying count = {product_data.requested_count}"


def test_check_product_availability_returns_false_when_product_available(products_data):
    test_product = products_data[random.randint(0, len(products_data) - 1)]
    product_data = ProductData(
        product_id=test_product["product_id"],
        name=test_product["name"],
        price=test_product["price"],
        requested_count=test_product["available_count"] + 1,
        delivery_address=str(uuid.uuid4()),
        type=test_product["type"]
    )
    is_product_available = check_product_availability(product_data)
    assert not is_product_available,\
        f"Product should NOT be available, product available count = {test_product['available_count']} " \
        f"product requested buying count  = {product_data.requested_count}"

