import os
from typing import Type
from pay_order_lambda.data_handlers.data_strategies import MakePaymentByCreditStrategy

ALLOWED_PAYMENT_DATA_GETTERS = ('REST_API', "Credit")


def payment_method_factory() -> Type[MakePaymentByCreditStrategy]:
    """
    Factory to choose the class that takes care of payment.

    Order data could be retrieved from any type of database, rest api,
        graphql... In order to have modularity we implement this factory that
        returns a class that MUST follow protocols stablished on class
        OrderDataGetter.

    Returns:
        Class that follows protocol 'OrderDataGetter' to extract order data.
    Raises:
        ValueError if the methodology was not specified or specified incorrect.
    """
    payment_methodology = os.environ.get('PAYMENT_DATA_HANDLER')
    if (payment_methodology is None
        or
        payment_methodology not in ALLOWED_PAYMENT_DATA_GETTERS):
        raise ValueError(f'Specified payment methodology not defined or the'
                         f' specified methodology "{payment_methodology}" '
                         f'is not implemented.')
    if payment_methodology == "Credit":
        return MakePaymentByCreditStrategy