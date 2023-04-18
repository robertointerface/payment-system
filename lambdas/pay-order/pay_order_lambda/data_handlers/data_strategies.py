from pay_order_lambda.data_handlers.data_getters import MongoOrderDataGetter
from pay_order_lambda.make_payment import MakePaymentUserCredit


class MakePaymentByCreditStrategy:
    order_data_getter = MongoOrderDataGetter
    payment_methodology = MakePaymentUserCredit

