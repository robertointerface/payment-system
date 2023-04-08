import os
import pytest
from data_getters import MongoOrderDataGetter
from factories import order_data_getter_factory


@pytest.mark.parametrize('data_getter_variable,expected_result',
                         [
                             ('MongoDb', MongoOrderDataGetter)
                         ]
                         )
def test_factory_method_order_data_getter_factory_returns_correct_method(
        data_getter_variable, expected_result):
    """Test method order_data_getter_factory returns correct values

    Args:
        data_getter_variable: value to set on environment variable ORDER_DATA_GETTER
            to test the method since the method result depends on that value.
        expected_result: expected type of class that is returned from the method.
    """
    os.environ['ORDER_DATA_GETTER'] = data_getter_variable
    order_data_getter = order_data_getter_factory()
    assert type(order_data_getter) is type(expected_result)


def test_factory_method_order_data_getter_factory_raises_error_when_incorrect_environ_variable_defined():
    """
    Test factory method order_data_getter_factory raises valuerror when incorrect
    environment variable is set.
    """
    os.environ['ORDER_DATA_GETTER'] = "Non-existing-data-getter"
    with pytest.raises(ValueError) as exc_info:
        _ = order_data_getter_factory()
    expected_key_phrases = ["Specified order data getter was not defined",
                          "is not implemented"]
    for phrase in expected_key_phrases:
        assert phrase in str(exc_info.value), \
            f"expected phrase '{phrase}' should be on error message when order data getter is wrongly defined"
