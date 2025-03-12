import unittest
from unittest.mock import patch, Mock
from utils import get_transaction_amount_rub, load_transactions
import os
import json

class TestUtils(unittest.TestCase):

    def test_get_transaction_amount_rub_rub(self):
        transaction = {'operationAmount': {'amount': '100.0', 'currency': 'RUB'}}
        self.assertEqual(get_transaction_amount_rub(transaction), 100.0)

    @patch('utils.convert_to_rub')
    def test_get_transaction_amount_rub_foreign(self, mock_convert_to_rub):
        transaction = {'operationAmount': {'amount': '50.0', 'currency': 'USD'}}
        mock_convert_to_rub.return_value = 4500.0
        self.assertEqual(get_transaction_amount_rub(transaction), 4500.0)
        mock_convert_to_rub.assert_called_once_with(50.0, 'USD')

        transaction = {'operationAmount': {'amount': '25.0', 'currency': 'EUR'}}
        mock_convert_to_rub.return_value = 2250.0
        self.assertEqual(get_transaction_amount_rub(transaction), 2250.0)
        mock_convert_to_rub.assert_called_with(25.0, 'EUR')

    def test_get_transaction_amount_rub_invalid_input(self):
        with self.assertRaises(TypeError):
            get_transaction_amount_rub("not a dict")
        with self.assertRaises(ValueError):
            get_transaction_amount_rub({})
        with self.assertRaises(ValueError):
            get_transaction_amount_rub({'operationAmount': {'currency': 'RUB'}}) # Missing amount
        with self.assertRaises(ValueError):
            get_transaction_amount_rub({'operationAmount': {'amount': 'abc', 'currency': 'RUB'}}) # Invalid amount

    def test_load_transactions_file_handling(self):
        def run_load_test(file_content, expected_result):
            with open("test_file.json", "w") as f:
                f.write(file_content)
            result = load_transactions("test_file.json")
            self.assertEqual(result, expected_result)
            os.remove("test_file.json")

        run_load_test("", [])
        run_load_test("not json", [])
        run_load_test(json.dumps([{"test": "data"}]), [{"test": "data"}])
        self.assertEqual(load_transactions("non_existent_file.json"), [])