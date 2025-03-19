import unittest
from unittest.mock import patch
from src.parser import HH
from src.user_interaction import interact


class TestInteract(unittest.TestCase):

    @patch('builtins.input', return_value='5')
    # Патчим input и имитируем ввод '5'
    def test_interact_incorrect_selection(self, mock_input):
        with patch('builtins.print') as mock_print:
        # Патчим print, чтобы перехватить вывод
            interact()
            mock_print.assert_called_with('Неверный выбор. Программа завершает работу.')