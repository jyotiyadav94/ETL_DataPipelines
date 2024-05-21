'''
import pandas as pd
import unittest
from app.load import convert_df_to_json, delete_records, insert_records

class TestInsertRecords(unittest.TestCase):
    """Unit tests for the insert_records function."""

    def test_convert_df_to_json(self):
        """
        Test the conversion of a DataFrame to a list of dictionaries in JSON format.
        """
        df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        result = convert_df_to_json(df)
        expected = [{'col1': '1', 'col2': 'a'}, {'col1': '2', 'col2': 'b'}, {'col1': '3', 'col2': 'c'}]
        assert result == expected


if __name__ == '__main__':
    unittest.main()
'''