from pydantic import BaseModel

from check_product_availability_lambda.exceptions import \
    ProductsNotAvailableException
from check_product_availability_lambda.factories import order_data_getter_factory


class UpdateProductData(BaseModel):
    product_id: str
    available_count: int


def lambda_handler(event, context):
    order_id = event.get("order_id")
    if order_id is None:
        raise ValueError(f"order id was not provided in event, Lambda can not "
                         f"be executed without an Order id.")
    data_handler = order_data_getter_factory()
    order_data_getter = data_handler.order_data_getters()
    order_data_getter.get_order_data(order_id)
    order_data = order_data_getter.order_data
    products_available = map(data_handler.check_product_availability,
                             order_data.products)
    if not all(products_available):
        raise ProductsNotAvailableException(
            "some or all of the products are not available")
    products_updater_method = data_handler.product_updater
    products_updater = products_updater_method(order_data.products)
    products_updater.update()
    return {"available": True}
