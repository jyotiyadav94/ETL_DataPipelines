import pandas as pd
from tabulate import tabulate
import csv

def load_csv(file_path):
    """
    Load a CSV file into a DataFrame.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    pd.DataFrame or FileNotFoundError or pd.errors.EmptyDataError:
        Returns a DataFrame containing the data from the CSV file if successful.
        Returns FileNotFoundError if the file specified by 'file_path' does not exist.
        Returns pd.errors.EmptyDataError if the CSV file specified by 'file_path' is empty.
    """
    try:
        df = pd.read_csv(file_path)
        print("File Successfully turned into a DF")
        return df 
    except FileNotFoundError as error:
        print(f"There is No file at {file_path}")
        return error
    except pd.errors.EmptyDataError as empty_data_error:
        print(f"There is No data in {file_path}")
        return empty_data_error

def print_tabulated_data(data_frame):
    """
    Print tabulated data from a DataFrame.

    Args:
    data_frame (pd.DataFrame): The DataFrame containing the data to be tabulated.

    Returns:
    This function prints the tabulated data from the provided DataFrame in a visually appealing format.
    """
    print(tabulate(data_frame, headers='keys', tablefmt='psql'))

def extract_data(file_path):
    """
    Extract asset records from a CSV file.

    Args:
    file_path (str): The path to the CSV file containing asset records.

    Returns:
    pd.DataFrame or FileNotFoundError or pd.errors.EmptyDataError:
        Returns a DataFrame containing the asset records from the CSV file if successful.
        Returns FileNotFoundError if the file specified by 'file_path' does not exist.
        Returns pd.errors.EmptyDataError if the CSV file specified by 'file_path' is empty.
    """
    return load_csv(file_path)

