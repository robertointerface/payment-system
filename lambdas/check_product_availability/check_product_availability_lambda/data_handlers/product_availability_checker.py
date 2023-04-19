from check_product_availability_lambda.data_handlers.data_getters import ProductData
from check_product_availability_lambda.database_connection import(
    get_database_connection,
    PAYMENT_SYSTEM_DATABASE_NAME)
from check_product_availability_lambda.exceptions import ProductNotFoundException


"""This could be implemented with a Rest API or graphql, the database should
not be accessed directly, database operations should be implemented in an 
isolated/microservice way."""
def check_product_availability(product: ProductData) -> bool:
    """Check if a product is available in the warehouse for a given quantity.

    i.e if the user requests 2 monitors and there is only 1 in the warehouse
        this will return False, if the user requests 1 monitor and there are
        5 monitors on the warehouse, this will return True

    Args:
        product: Product information of type ProductData

    Returns:
        True: product is available
        False: product is not Available
    Raises:
        ProductNotFoundException: if product can not be found on warehouse
    """
    mongo_connection = get_database_connection()
    db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
    product_data = db.products.find_one({"product_id": product.product_id})
    if product_data is None:
        raise ProductNotFoundException(f"Product with id {product.product_id} "
                                       f"could not be found.")
    return product_data["available_count"] >= product.requested_count

