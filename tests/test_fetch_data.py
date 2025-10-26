"""
Unit tests for the data retrieval script
"""

import unittest
import os
import sys
import json
from unittest.mock import patch, Mock

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from fetch_data import fetch_bls_data, save_data


class TestFetchData(unittest.TestCase):
    
    def test_save_data_creates_directory(self):
        """Test that save_data creates the output directory if it doesn't exist"""
        test_dir = 'test_data_output'
        test_data = {'test': 'data'}
        
        # Clean up if exists
        if os.path.exists(test_dir):
            import shutil
            shutil.rmtree(test_dir)
        
        try:
            save_data(test_data, test_dir)
            self.assertTrue(os.path.exists(test_dir))
        finally:
            # Clean up
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir)
    
    def test_save_data_creates_json_file(self):
        """Test that save_data creates a JSON file"""
        test_dir = 'test_data_output'
        test_data = {'status': 'REQUEST_SUCCEEDED', 'data': [1, 2, 3]}
        
        try:
            filename = save_data(test_data, test_dir)
            self.assertTrue(os.path.exists(filename))
            self.assertTrue(filename.endswith('.json'))
            
            # Verify content
            with open(filename, 'r') as f:
                loaded_data = json.load(f)
            self.assertEqual(loaded_data, test_data)
        finally:
            # Clean up
            if os.path.exists(test_dir):
                import shutil
                shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
