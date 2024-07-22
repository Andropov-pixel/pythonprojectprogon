import pytest

from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date


@pytest.mark.parametrize("string, expected_result", [
    ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ("Счет 12345678901234567890", "Счет **7890"),
])
def test_mask_account_card(string, expected_result):
    assert mask_account_card(string) == expected_result


def test_get_date(date):
    assert get_date(date) == "2018-07-11T02:26:18.671407"


@pytest.mark.parametrize("string, expected_result", [
    ("7158300734726758", "7158 30** **** 6758"),
    ("7158300734726759", "7158 30** **** 6759"),
])
def test_get_mask_card_number(string, expected_result):
    assert get_mask_card_number(string) == expected_result


@pytest.mark.parametrize("string, expected_result", [
    ("12345678901234567340", "**7340"),
    ("12345678901234567890", "**7890"),
])
def test_get_mask_account(string, expected_result):
    assert get_mask_account(string) == expected_result
