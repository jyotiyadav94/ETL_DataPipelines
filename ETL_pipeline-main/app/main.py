import os
import json
import logging
import pandas as pd
from typing import List
from pymongo import MongoClient
from fastapi import FastAPI, Response
from app.extract import extract_data
from dotenv import load_dotenv, find_dotenv
from app.load import convert_df_to_json, delete_records, insert_records
from app.transform import validate_assets, validate_entities, validate_join, transform_data

# Load environment variables
config = find_dotenv(".env")
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# MongoDB connection parameters
cluster_uri = os.getenv("CLUSTER_URI")
collection_name = os.getenv("MONGODB_COLLECTION")
database_name = os.getenv("MONGODB_DATABASE")

# Create a FastAPI app
app = FastAPI()

# Connect to MongoDB
client = MongoClient(cluster_uri)
db = client[database_name]
collection = db[collection_name]

def etl_pipeline():
    """
    Main entry point of the data pipeline.
    
    This function orchestrates the Extract, Transform, Load (ETL) process.
    It extracts, validates, and transforms the data, then saves it to a MongoDB collection.
    """
    data_folder = '/dataset'
    asset_file = os.path.join(data_folder, 'data engineer 2023 - input - assets.csv')
    logger.info('data engineer 2023 - input - assets.csv File Successfully turned into a DF')
    entity_file = os.path.join(data_folder, 'data engineer 2023 - input - entities.csv')
    logger.info('data engineer 2023 - input - entities.csv File Successfully turned into a DF')
    join_file = os.path.join(data_folder, 'data engineer 2023 - input - assets_entities_join.csv')
    logger.info('data engineer 2023 - input - assets.csv File Successfully turned into a DF')

    try:
        # Extract data
        asset_records = extract_data(asset_file)
        entity_records = extract_data(entity_file)
        join_records = extract_data(join_file)
        logger.info('Data extraction successful.')

        # Validate data
        asset_records = validate_assets(asset_records)
        entity_records = validate_entities(entity_records)
        join_records = validate_join(join_records)
        logger.info('Data validation successful.')

        # Transform data
        transformed_data = transform_data(asset_records, entity_records, join_records)
        logger.info('Data transformation successful.')

        # Convert DataFrame to JSON
        df_records = convert_df_to_json(transformed_data)
        logger.info('DataFrame conversion to JSON successful.')

        # Delete existing collection content
        delete_records(collection)
        logger.info('Existing collection content deleted.')

        # Insert new records into the collection
        insert_records(collection, df_records)
        logger.info('Records inserted into MongoDB collection.')

        logger.info("All data has been ingested.")
    except Exception as e:
        logger.exception("An error occurred during the data pipeline.")


@app.get("/data")
def read_data():
    """
    Retrieve all data from a specific MongoDB collection.

    This endpoint triggers the ETL process, retrieves all records from the MongoDB collection,
    and returns them in JSON format.

    Returns:
        Response: JSON response containing all records from the MongoDB collection.
    """
    try:
        # Trigger the ETL process
        etl_pipeline()

        # Query the database to retrieve all records
        records = list(collection.find({}))

        # Convert ObjectId to string for serialization
        for record in records:
            record["_id"] = str(record["_id"])

        # Serialize the records to JSON with proper formatting
        json_str = json.dumps(records, indent=4, default=str)

        # Return the formatted JSON response
        return Response(content=json_str, media_type="application/json")
    except Exception as e:
        logger.exception("An error occurred while fetching all data from MongoDB.")
        return Response(content=json.dumps({"error": "An error occurred."}), status_code=500, media_type="application/json")

@app.get("/data/{citycode}")
def get_record_by_city_code(citycode: str):
    """
    Get details of a record from MongoDB based on the cityCode.

    Args:
        citycode (str): The city code to search for in the MongoDB collection.

    Returns:
        Response: JSON response containing the details of the record.
    """
    try:
        # Query the database to retrieve the record based on citycode
        record = collection.find_one({"cityCode": citycode})

        # If no record found, return a 404 Not Found response
        if not record:
            return Response(content=json.dumps({"message": "Record not found"}), status_code=404, media_type="application/json")

        # Convert ObjectId to string for serialization
        record["_id"] = str(record["_id"])

        # Serialize the record to JSON with proper formatting
        json_str = json.dumps(record, indent=4, default=str)

        # Return the formatted JSON response
        return Response(content=json_str, media_type="application/json")
    except Exception as e:
        logger.exception(f"An error occurred while fetching data for city code: {citycode}.")
        return Response(content=json.dumps({"error": "An error occurred."}), status_code=500, media_type="application/json")
