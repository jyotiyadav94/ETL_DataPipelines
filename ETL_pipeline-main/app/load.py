import pandas as pd
from pymongo import MongoClient
from typing import List

def convert_df_to_json(df: pd.DataFrame) -> List[dict]:
    """
    Convert DataFrame to a list of dictionaries in JSON format.

    Args:
        df (pd.DataFrame): The input DataFrame.

    Returns:
        List[dict]: List of dictionaries representing the DataFrame in JSON format.

    This function selects specific columns from the input DataFrame and converts them into a list of dictionaries,
    with each dictionary representing a row of data in JSON format.
    """
    df_json = df[['cherry_asset_id', 'cityCode', 'catasto', 'sezione', 'foglio', 'particella', 'subalterno', 'ownerships']]
    json_data = df_json.to_dict(orient='records')
    return json_data


def delete_records(collection: str):
    """
    Delete all documents from a MongoDB collection.

    Args:
        collection (str): The name of the MongoDB collection to delete documents from.
    """
    collection.delete_many({})


def insert_records(collection: str, records: list):
    """
    Insert records into a MongoDB collection.

    Args:
        collection (str): The name of the MongoDB collection to insert records into.
        records (list): List of dictionaries representing the records to be inserted.
    """
    records = [dict(record) for record in records]
    collection.insert_many(records)
