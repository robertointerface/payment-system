from arrange_delivery_lambda.database_connection import (
    get_database_connection,
    PAYMENT_SYSTEM_DATABASE_NAME)


def lambda_handler(event, context):
    order_id = event.get('order_id')
    if order_id is None:
        raise ValueError(f'order Id was not provided in event')
    mongo_client = get_database_connection()
    db = mongo_client[PAYMENT_SYSTEM_DATABASE_NAME]
    order_info = db['orders'].find_one({"order_id": order_id})
    deliveries = []
    for product in order_info["products"]:
        deliveries.append({
            "order_id": order_id,
            "product_id": product["product_id"],
            "delivery_address": product["delivery_address"]
        })
    db["deliveries"].insert_many(deliveries)