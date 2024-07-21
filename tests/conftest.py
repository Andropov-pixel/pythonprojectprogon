import pytest

from src.processing import initial_list


@pytest.fixture
def test_initial_list():
    return 'EXECUTED'

@pytest.fixture
def test_initial_list_1():
    return initial_list