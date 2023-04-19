from typing import Union
from abc import ABC, abstractmethod
from pydantic import BaseModel

from pay_order_lambda.database_connection import get_database_connection, \
    PAYMENT_SYSTEM_DATABASE_NAME
from pay_order_lambda.exceptions import NotEnoughCredictError


class UserCreditPaymentDetails(BaseModel):
    user_id: str
    amount_to_charge: float


class MakePayment(ABC):
    """Abstract class to define protocols/interface for make payments"""
    @abstractmethod
    def make_payment(self):
        pass

    @abstractmethod
    def set_payment_details(self,
                            payment_details: Union[UserCreditPaymentDetails]):
        pass


class MakePaymentUserCredit(MakePayment):
    """Take order payment by deducting from his credit saved on database.
    __payment_details attribute needs to be set first.
    """
    def make_payment(self):
        """Process Payment for a given order.

        Get the user credit details.
            If credit is less than amount to charge raise error.
            If credit is enough reduce from the account and save back to
            Database.

        Raises:
            NotEnoughCredictError: If user does  not have enough credit.
        """
        mongo_connection = get_database_connection()
        db = mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]
        user = db.users.find_one({'user_id': self.user_id})
        if user['credit'] < self.amount_to_charge:
            msg = f"Not enough credit on the user.\n" \
                  f"user credit = {user['credit']} \n" \
                  f"order cost = {self.amount_to_charge}"
            raise NotEnoughCredictError(msg)
        pipeline = [
            {
                "$set": {
                    "credit": {
                        '$subtract': ['$credit',
                                      self.amount_to_charge]
                    }
                }
            }
        ]
        _ = db.users.update_one({'user_id': self.user_id},
                                           pipeline)

    def set_payment_details(self, payment_details: UserCreditPaymentDetails):
        """Set payment details that will be used to process payment"""
        self.__payment_details = payment_details

    @property
    def user_id(self):
        return self.__payment_details.user_id

    @property
    def amount_to_charge(self):
        return self.__payment_details.amount_to_charge
