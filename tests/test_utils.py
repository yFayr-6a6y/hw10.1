import unittest
from unittest.mock import patch, Mock
import os
import json

class TestUtils(unittest.TestCase):

    def test_get_transaction_amount_rub_rub(self):
        transaction = {
            'operationAmount': {
                'amount': '100.0',
                'currency': {'code': 'RUB'}
            }
        }
        self.assertEqual(get_transaction_amount_rub(transaction), 100.0)

    @patch('external_api.convert_to_rub')
    def test_get_transaction_amount_rub_foreign(self, mock_convert_to_rub):
        mock_convert_to_rub.return_value = 4500.0
        transaction = {
            'operationAmount': {
                'amount': '50.0',
                'currency': {'code': 'USD'}
            }
        }
        self.assertEqual(get_transaction_amount_rub(transaction), 4500.0)
        mock_convert_to_rub.assert_called_once_with(50.0, 'USD')

        mock_convert_to_rub.return_value = 2250.0
        transaction = {
            'operationAmount': {
                'amount': '25.0',
                'currency': {'code': 'EUR'}
            }
        }
        self.assertEqual(get_transaction_amount_rub(transaction), 2250.0)
        mock_convert_to_rub.assert_called_with(25.0, 'EUR')

    @patch('external_api.convert_to_rub')
    def test_get_transaction_amount_rub_conversion_failure(self, mock_convert_to_rub):
        mock_convert_to_rub.return_value = None
        transaction = {
            'operationAmount': {
                'amount': '50.0',
                'currency': {'code': 'USD'}
            }
        }
        with self.assertRaises(ValueError):
            get_transaction_amount_rub(transaction)

    def test_get_transaction_amount_rub_invalid_input(self):
        with self.assertRaises(TypeError):
            get_transaction_amount_rub("not a dict")
        with self.assertRaises(ValueError):
            get_transaction_amount_rub({})
        with self.assertRaises(ValueError):
            get_transaction_amount_rub({'operationAmount': {'currency': {'code': 'RUB'}}})  # Нет amount

    def test_load_transactions_file_handling(self):
        def run_load_test(file_content, expected_result):
            with open("test_file.json", "w", encoding='utf-8') as f:
                f.write(file_content)
            result = load_transactions("test_file.json")
            self.assertEqual(result, expected_result)
            os.remove("test_file.json")

        run_load_test("", [])
        run_load_test("not json", [])
        run_load_test(json.dumps([{"test": "data"}]), [{"test": "data"}])
        self.assertEqual(load_transactions("non_existent_file.json"), [])