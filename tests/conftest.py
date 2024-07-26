import pytest

from src.generators import transactions
from src.processing import initial_list


@pytest.fixture
def test_initial_list():
    return "EXECUTED"


@pytest.fixture
def test_initial_list_1():
    return initial_list


@pytest.fixture
def date():
    return "2018-07-11T02:26:18.671407"


@pytest.fixture
def test_transactions():
    return transactions
