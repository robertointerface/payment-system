from pydantic import BaseModel
from check_product_availability_lambda.exceptions import \
    ProductsNotAvailableException
from check_product_availability_lambda.factories import order_data_getter_factory


class UpdateProductData(BaseModel):
    product_id: str
    available_count: int


def lambda_handler(event, context):
    """Handle lambda request.

    Take the purchase order id and do the following steps.
        - load the products information for the related order id.
        - Assert the requested quantity of products are available on warehouse.
        - Update warehouse to reduce the number of available products.
        i.e available products in warehouse =  available products in warehouse - order requesetd products
        that way the warehouse data is up to date.
    Args:
        event: contains the order id.
        context: Empty in this case

    Returns:
        Dict: As this will be used on State Machine we return necessary
            information for the next step, that is if all products are available
            and propagate the order_id.
    Raises:
        OrderNotFoundException: If order can not be found.
        ProductNotFoundException: if any of the requested products can not be
            found.
        ProductsNotAvailableException: If any of the requested product is not
        available in the desire quantity.
    """
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
    return {"available": True,
            "order": order_id}
