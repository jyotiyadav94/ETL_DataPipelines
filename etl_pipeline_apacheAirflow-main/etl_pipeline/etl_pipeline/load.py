import pandas as pd
from pymongo import MongoClient
from typing import List
import os


def delete_collection_data(my_database, my_collection, cluster_uri):
    """
    Delete all records from the specified collection in the specified database.
    """
    # Connect to MongoDB
    client = MongoClient(cluster_uri)

    # Access the database and collection
    db = client[str(my_database)]
    collection = db[str(my_collection)]

    # Delete all records from the collection
    collection.delete_many({})

    # Close the MongoDB connection
    client.close()


def insert_dataframe_to_collection(my_database, my_collection, cluster_uri, dataframe_dict):
    """
    Insert the DataFrame records into the specified collection in the specified database.
    """
    # Connect to MongoDB
    client = MongoClient(cluster_uri)

    # Access the database and collection
    db = client[my_database]

    # Iterate over each collection and DataFrame in the dictionary
    for collection_name, dataframe in dataframe_dict.items():
        # Access the collection
        collection = db[collection_name]

        # Delete all records from the collection
        collection.delete_many({})

        # Convert DataFrame to dictionary
        data = dataframe.to_dict(orient='records')

        # Insert data into MongoDB collection
        collection.insert_many(data)

    # Close the MongoDB connection
    client.close()



def query_collection_to_dataframe(my_database, my_collection, cluster_uri):
    """
    Query all records from the specified collection in the specified database,
    and load the data into a DataFrame.
    """
    # Connect to MongoDB
    client = MongoClient(cluster_uri)

    # Access the database and collection
    db = client[my_database]
    collection = db[my_collection]

    # Query all records from the collection
    cursor = collection.find({})

    # Convert cursor to DataFrame
    dataframe = pd.DataFrame(list(cursor))

    # Close the MongoDB connection
    client.close()

    return dataframe


def save_df_to_csv(df):
    """
    Save a DataFrame to a CSV file.

    Args:
    - df (pd.DataFrame): The DataFrame to be saved.
    - file_path (str): The file path where the CSV file will be saved.
    """
    df.to_csv("/Users/wenda/airflow/dags/etl_pipeline/target/menu.csv", index=False)