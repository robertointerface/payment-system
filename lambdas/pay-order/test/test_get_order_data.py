from pay_order_lambda.data_handlers.data_getters import (
    MongoOrderDataGetter,
    OrderData)

EXTRACTED_ORDER_FIELDS = ['order_id', 'user_id', 'products']


def test_order_getter_returns_expected_fields(order_id):
    data_getter = MongoOrderDataGetter()
    data_getter.get_order_data(order_id)
    extracted_order_data = data_getter.__dict__['_MongoOrderDataGetter__raw_order_data']
    assert list(extracted_order_data.keys()).sort() == EXTRACTED_ORDER_FIELDS.sort()


def test_property_order_data_returns_correct_type(order_id):
    data_getter = MongoOrderDataGetter()
    data_getter.get_order_data(order_id)
    order_data = data_getter.order_data
    assert isinstance(order_data, OrderData)
