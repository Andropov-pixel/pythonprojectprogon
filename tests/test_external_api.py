from unittest.mock import patch

from src.external_api import convert_to_rub


@patch('requests.get')
def test_convert_to_rub(mock_get):
    mock_response = mock_get.return_value
    mock_response.json.return_value = {"result": 75.0}

    transaction = {
        "operationAmount": {
            "amount": 1,
            "currency": {"code": "USD"}
        }
    }
    result = convert_to_rub(transaction)
    assert result == 75.0
