import unittest
import pandas as pd
from app.transform import drop_columns, remove_duplicates, validate_assets, validate_entities, validate_join
from app.transform import remove_invalid_characters, remove_invalid_records, fill_missing_values, delete_nan_rows,create_cherry_asset_id

class TestTransformFunctions(unittest.TestCase):
    """Unit tests for the Transform class."""

    def test_fill_missing_values(self):
        """Test filling missing values with empty strings."""
        df = pd.DataFrame({'A': [1, None, 3], 'B': ['NaN', 'nan', None]})
        result = fill_missing_values(df)
        expected = pd.DataFrame({'A': [1, '', 3], 'B': ['', '', '']})
        pd.testing.assert_frame_equal(result, expected)

    def test_drop_columns(self):
        """Test dropping specified columns."""
        df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        to_drop = ['A', 'B']
        result = drop_columns(df, to_drop)
        expected = pd.DataFrame({'C': [7, 8, 9]})
        pd.testing.assert_frame_equal(result, expected)

    def test_remove_duplicates(self):
        """Test removing duplicate entries."""
        df = pd.DataFrame({'A': [1, 2, 3, 3], 'B': [4, 5, 6, 6], 'C': [7, 8, 9, 9]})
        result = remove_duplicates(df)
        expected = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6], 'C': [7, 8, 9]})
        pd.testing.assert_frame_equal(result, expected)

    def test_validate_assets(self):
        """Test validating asset records."""
        asset_data = pd.DataFrame({'particella': ['1', '2', '3', '4'], 'subalterno': ['5', '6', '7', '8']})
        result = validate_assets(asset_data)
        expected = pd.DataFrame({'particella': ['1', '2', '3', '4'], 'subalterno': ['5', '6', '7', '8']})
        pd.testing.assert_frame_equal(result, expected)

    def test_validate_entities(self):
        """Test validating entity records."""
        entity_data = pd.DataFrame({'entity_id': [1, 2, 3, 3], 'vatCode': ['4', '5', '6', '6'], 'taxCode': ['7', '8', '9', '9']})
        result = validate_entities(entity_data)
        expected = pd.DataFrame({'entity_id': [1, 2, 3], 'vatCode': ['4', '5', '6'], 'taxCode': ['7', '8', '9']})
        pd.testing.assert_frame_equal(result, expected)

    def test_validate_join(self):
        """Test validating join records."""
        join_data = pd.DataFrame({'entity_id': [1, 2, 3, 3], 'asset_id': [4, 5, 6, 6]})
        result = validate_join(join_data)
        expected = pd.DataFrame({'entity_id': [1, 2, 3], 'asset_id': [4, 5, 6]})
        pd.testing.assert_frame_equal(result, expected)

    def test_remove_invalid_characters(self):
        """Test removing invalid characters from specified columns."""
        df = pd.DataFrame({'A': ['123abc', '456def', '789!@#'], 'B': ['abc', 'def456', '789xyz']})
        columns = ['A', 'B']
        result = remove_invalid_characters(df, columns)
        expected = pd.DataFrame({'A': ['123abc', '456def'], 'B': ['abc', 'def456']})
        pd.testing.assert_frame_equal(result, expected)

if __name__ == '__main__':
    unittest.main()
