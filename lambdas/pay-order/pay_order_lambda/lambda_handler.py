
from pay_order_lambda.factories import payment_method_factory
from pay_order_lambda.make_payment import UserCreditPaymentDetails


def lambda_handler(event, context):
    order_id = event.get('order_id')
    if order_id is None:
        raise ValueError(f'Order Id was not provided to the lambda Event')
    data_handler = payment_method_factory()
    order_data_getter = data_handler.order_data_getter()
    order_data_getter.get_order_data(order_id)
    order_data = order_data_getter.order_data
    payment_methodology = data_handler.payment_methodology()
    payment_details = UserCreditPaymentDetails(user_id=order_data.user_id,
                                               amount_to_charge=order_data.total_payment)
    payment_methodology.set_payment_details(payment_details)
    payment_methodology.make_payment()
