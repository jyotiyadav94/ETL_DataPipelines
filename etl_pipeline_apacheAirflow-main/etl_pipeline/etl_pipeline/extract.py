import pandas as pd
from tabulate import tabulate
import csv

def load_csv(file_path):
    """
    Load a CSV file into a DataFrame.
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
    """
    print(tabulate(data_frame.head(5), headers='keys', tablefmt='psql'))



    

