"""
Unit tests for the data processing script
"""

import unittest
import os
import sys
import pandas as pd
import json

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from process_data import load_bls_data, process_bls_data


class TestProcessData(unittest.TestCase):
    
    def setUp(self):
        """Set up test data"""
        self.sample_bls_data = {
            'status': 'REQUEST_SUCCEEDED',
            'Results': {
                'series': [{
                    'data': [
                        {
                            'year': '2023',
                            'period': 'M01',
                            'periodName': 'January',
                            'value': '157000',
                            'footnotes': []
                        },
                        {
                            'year': '2023',
                            'period': 'M02',
                            'periodName': 'February',
                            'value': '157200',
                            'footnotes': [{'text': 'Preliminary'}]
                        }
                    ]
                }]
            }
        }
    
    def test_process_bls_data_returns_dataframe(self):
        """Test that process_bls_data returns a DataFrame"""
        result = process_bls_data(self.sample_bls_data)
        self.assertIsInstance(result, pd.DataFrame)
    
    def test_process_bls_data_correct_columns(self):
        """Test that the DataFrame has correct columns"""
        result = process_bls_data(self.sample_bls_data)
        expected_columns = ['year', 'period', 'periodName', 'value', 'footnotes']
        self.assertListEqual(list(result.columns), expected_columns)
    
    def test_process_bls_data_correct_row_count(self):
        """Test that the DataFrame has correct number of rows"""
        result = process_bls_data(self.sample_bls_data)
        self.assertEqual(len(result), 2)
    
    def test_process_bls_data_value_is_numeric(self):
        """Test that value column is converted to numeric"""
        result = process_bls_data(self.sample_bls_data)
        self.assertTrue(pd.api.types.is_numeric_dtype(result['value']))


if __name__ == '__main__':
    unittest.main()
