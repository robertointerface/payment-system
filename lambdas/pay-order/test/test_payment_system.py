import random

import pytest

from pay_order_lambda.exceptions import NotEnoughCredictError
from pay_order_lambda.make_payment import (
    MakePaymentUserCredit,
    UserCreditPaymentDetails)
from pay_order_lambda.database_connection import (
    get_database_connection,
    PAYMENT_SYSTEM_DATABASE_NAME)


class TestMakePaymentUserCredit:

    def database_connection(self):
        mongo_connection = get_database_connection()
        return mongo_connection[PAYMENT_SYSTEM_DATABASE_NAME]

    def test_make_payment_method_updates_users_credit(self,
                                                      insert_users):
        dummy_user_id = insert_users[random.randint(0, len(insert_users) - 1)]
        database = self.database_connection()
        user_to_use = database.users.find_one({"_id": dummy_user_id})
        amount_to_charge = round(user_to_use['credit'] / 2, 2)
        expected_user_result = user_to_use['credit'] - amount_to_charge
        user_payment_details = UserCreditPaymentDetails(
            user_id=user_to_use['user_id'],
            amount_to_charge=amount_to_charge
        )
        payment_instance = MakePaymentUserCredit()
        payment_instance.set_payment_details(user_payment_details)
        payment_instance.make_payment()
        updated_user = database.users.find_one({"_id": dummy_user_id})
        assert updated_user['credit'] == expected_user_result

    def test_make_payment_method_raises_NotEnoughCredictError(self,
                                                              insert_users):
        dummy_user_id = insert_users[random.randint(0, len(insert_users) - 1)]
        database = self.database_connection()
        user_to_use = database.users.find_one({"_id": dummy_user_id})
        amount_to_charge = user_to_use['credit'] + 1000000
        user_payment_details = UserCreditPaymentDetails(
            user_id=user_to_use['user_id'],
            amount_to_charge=amount_to_charge
        )
        payment_instance = MakePaymentUserCredit()
        payment_instance.set_payment_details(user_payment_details)
        with pytest.raises(NotEnoughCredictError):
            payment_instance.make_payment()