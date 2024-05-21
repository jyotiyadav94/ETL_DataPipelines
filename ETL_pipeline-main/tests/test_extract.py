import unittest
import pandas as pd
from unittest.mock import patch
from app.extract import print_tabulated_data, load_csv
from pandas.testing import assert_frame_equal


class TestLoadCsv(unittest.TestCase):
    """Unit tests for the load_csv function."""

    def test_load_csv_with_valid_file(self):
        """
        Test that load_csv returns a pandas DataFrame when given a valid file path.
        """
        file_path = "dataset/data engineer 2023 - input - assets_entities_join.csv"
        df = load_csv(file_path)
        self.assertIsInstance(df, pd.DataFrame)

    def test_load_csv_with_non_existent_file(self):
        """
        Test that load_csv returns a FileNotFoundError when given an invalid file path.
        """
        file_path = "dataset/data enginee.csv"
        error = load_csv(file_path)
        self.assertIsInstance(error, FileNotFoundError)

    def test_load_csv_with_empty_file(self):
        """
        Test that load_csv returns a pd.errors.EmptyDataError when given an empty file path.
        """
        file_path = "dataset/data.csv"
        error = load_csv(file_path)
        self.assertIsInstance(error, pd.errors.EmptyDataError)


if __name__ == '__main__':
    unittest.main()
