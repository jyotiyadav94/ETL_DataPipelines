<a name="readme-top"></a>

# **Building ETL Pipeline**

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#project-background">Project Background</a></li>
    <li><a href="#How-to-Run">How to Run</a></li>
    <li><a href="#Dataset">Dataset</a></li>
    <li><a href="#Implementation">Implementation</a></li>
    <li><a href="#ETL-Pipeline">ETL Pipeline</a></li>
    <li><a href="#Environment-Variables-.env">Environment Variables (.env)</a></li>
    <li><a href="#Requirements.txt">Requirements.txt</a></li>
    <li><a href="#MongoDB">MongoDB</a></li>
    <li><a href="#Dockerfile-&-Docker-compose">Dockerfile & Docker-compose</a></li>
    <li><a href="#FastAPI-Web-Application">FastAPI Web Application</a></li>
    <li><a href="#Google-Cloud-Platform-(Deployment)">Google Cloud Platform (Deployment)</a></li>
    <li><a href="#Pytests">Pytests</a></li>
    <li><a href="#Feedback">Feedback</a></li>
  </ol>
</details>




<!-- PROJECT BACKGROUND -->
# **Project Background**
The ETL Pipeline Project is designed to process data from three CSV files, extract, transform, and validate, and ultimately load the transformed data into a JSON object. Leveraging Test-Driven Development principles, the project ensures the accuracy and reliability of data cleansing and transformation processes. Utilizing Docker and MongoDB, the application is Dockerized for scalability and efficiency, while FastAPI facilitates web application development. Deployment on Google Cloud Platform through Google Cloud Run showcases effective data management operations.

### **Project Structure**

``` bash

ETL_pipeline/
│
├── app/
│ ├── __init__.py
│ ├── extract.py
│ ├── load.py
│ ├── main.py
│ ├── transform.py
│ └── .env
│
├── dataset/
│ ├── __init__.py
│ ├── data engineer 2023 - input - assets.csv
│ ├── data engineer 2023 - input - assets_entities_join.csv
│ ├── data engineer 2023 - input - entities.csv
│ └── data.csv
│
├── tests/
│ ├── __init__.py
│ ├── test_extract.py
│ ├── test_load.py
│ ├── test_main.py
│ └── test_transform.py
│
├── Dockerfile
├── README.md
├── docker-compose.yaml
└── requirements.txt
└── .gitignore

```

# **How to Run**

1. **Download or Clone Repository:**
   - Download or clone the repository branch using the method of your choice. For example, if you have git installed on your machine, run the following command:
     ```bash
     https://github.com/jyotiyadav94/ETL_pipeline.git
     ```
     This will download the files into the ETL_pipeline folder.

2. **Ensure Python and Docker Installed:**
   - Ensure that both Python and Docker are installed on your machine.

3. **Navigate to the ETL_pipeline folder:**
   - Open a terminal and navigate to the ETL_pipeline folder:
     ```bash
     cd ETL_pipeline
     ```
   - Create a file named `.env` in the app folder and add the following credentials:
     ```plaintext
     ```

4. **Run Docker Images:**
   - Run the following command to start the Docker containers:
     ```bash
     docker-compose up
     ```

5. **Stop Docker Containers:**
   - Open a new terminal and run the following command to stop the Docker containers:
     ```bash
     docker-compose down
     ```

6. **Ensure Port Mapping:**
   - Ensure that the port mapping for the web application inside docker-compose.yml is set to port 8000, which is the default port.

7. **Test the Installation:**
   - Once the containers are running, you can test if the installation was successful by visiting the endpoints [http://127.0.0.1:8000/data](http://127.0.0.1:8000/data) or [http://127.0.0.1:8000/data/L263](http://127.0.0.1:8000/data/L263). If the installation was successful, you should receive a 200 OK response from the server.You should see the minimal interface displaying all the datasets present in the MongoDB or the designed endpoint with the specific cityCode. If you wish to see the documentation for your API, navigate to the [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) endpoint. This navigable API comes pre-packaged with FastAPI.

8. **Run Test Cases:**
   - Open a new terminal and run the following command to run all the test cases:
     ```bash
     pytest tests
     ```
     Note: Test cases related to pymongo are commented to run them. Ensure you have pymongo installed on VS code.

9. **Access Deployed Endpoint on Google Cloud Platform:**
   - To access the deployed endpoint on Google Cloud Platform, use the following URL:<br>
     [https://project-n5ni4ipgma-uc.a.run.app/data](https://project-n5ni4ipgma-uc.a.run.app/data)
    
   - To retrieve data for a specific city, replace "A024" with the desired city code in the URL:
     <br>
    [https://project-n5ni4ipgma-uc.a.run.app/data/A024](https://project-n5ni4ipgma-uc.a.run.app/data/A024)


# **Dataset**

### assets.csv

- The dataset consists of information about different assets (properties or parcels of land) identified by unique asset IDs.
- Each property is uniquely identified by the following fields: asset_id, cityCode, catasto, sezione, foglio, particella, and subalterno.
- Fields particella and subalterno can only accept digits and letters ([a-zA-Z0-9]).
<br>
<br>

| asset_id  | cityCode | catasto | sezione? | foglio | particella | subalterno? |
|-----------|----------|---------|----------|--------|------------|-------------|
| string    | string   | string  | string   | string | string     | string      |

- **asset_id**: Unique identifier for each asset.
- **cityCode**: Code identifying the city or municipality where the asset is located.
- **catasto**: This represent a category or classification related to cadastral or land registry information. It might indicate the type of land or property.
- **sezione**: It refers to the specific section or zone within a municipality
- **foglio**: Represents the sheet number within the cadastral map or registry where it has a detailed information about land plots/parcel, boundaries, and other cadastral data is recorded.
- **particella**: Denotes the parcel number within the section and sheet identified above.
- **subalterno**: Possibly refers to a subordinate or related entity or attribute of the asset.



### entities.csv
- This dataset contains information about different entities or individuals, each identified by a unique `entity_id`.
- Each record must have at least one of vatCode and taxCode fields filled.
- Field vatCode must be a valid Italian “partita iva” and field taxCode must be a valid Italian “codice fiscale”.
<br>
<br>

| entity_id | vatCode?   | taxCode?   |
|-----------|------------|------------|
| string    | string     | string     |

- **entity_id**: Unique identifier for each entity or individual.
- **taxCode**: Tax code or fiscal code associated with the entity. In Italy, this is known as "codice fiscale," a unique identifier used for tax purposes.
- **vatCode**: Value-added tax (VAT) code associated with the entity. In Italy, this is known as "partita IVA," a unique identifier used for VAT purposes.
  

### assets_entities_join.csv
- This dataset links the assets to the entities and contains the ownership share of each entity for their properties. It also has information related to the ownership shares of different assets, where each asset is identified by a unique `asset_id`. 
- Fields marked with “‘?“ are optional.
- The asset_id and entity_id fields are used to establish the relationship between assets and entities

| entity_id | asset_id | ownershipShare |
|-----------|----------|----------------|
| string    | string   | string         |

- **asset_id**: Unique identifier for each asset.
- **entity_id**: Unique identifier for the entity or individual associated with the ownership share.
- **ownershipShare**: Indicates the ownership share or percentage of ownership that the entity identified by `entity_id` holds in the asset identified by `asset_id`.

### Schema 
```json
{
  "cherry_asset_id": "string",
  "cityCode": "string",
  "catasto": "string",
  "sezione?": "string",
  "foglio": "string",
  "particella": "string",
  "subalterno?": "string",
  "ownerships": {
    "entity_id": "string",
    "vatCode?": "string",
    "taxCode?": "string",
    "ownershipShare": "float"
  }
}
```

### Target Validation 
- The minimum data validation required includes:
  - Removing all the non-valid records from the three files.
  - Managing duplicate entries.
  - Managing all other errors encountered while joining the files.


### Observations from the Dataset:

1. When encountering invalid or incomplete data we had two approaches:
    *  Remove the entire row. ( This approach has been used in the project)
    *  Remove the particular value in the particella column.

2. After merging the three dataset vat code and tax code fields, some records have NaN (Not a Number) values.
3. Regarding the ownershipShare field:
    - Upon examining the merged data, it appears that a single entity can have shared ownership with multiple individuals.
    - For example, we observed instances where ownership was divided as 50% between two individuals and 33% among three individuals for the same entity.
4. When considering the cherry_asset_id, include only mandatory data representing the asset, such as:
    - asset_id
    - cityCode
    - catasto
    - foglio
    - particella

5. For More on Observations Refer to EDA folder.

# **Implementation**

## **ETL Pipeline**

### extract.py

#### Class Summary: Extract Operations

This class contains functions designed to work with CSV files using the pandas library in Python.

- `load_csv(file_path)`: 
  - This function loads a CSV file into a pandas DataFrame. It handles potential errors such as FileNotFoundError and pd.errors.EmptyDataError.

- `print_tabulated_data(data_frame)`:
  - This function prints tabulated data from a DataFrame in a visually appealing format using the tabulate library.

- `extract_data(file_path)`:
  - This function extracts asset records from a CSV file by calling the `load_csv` function and returns a DataFrame containing the asset records. It also handles potential errors such as FileNotFoundError and pd.errors.EmptyDataError.


```python
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
```



### transform.py 

#### Class Summary: Transform Operations

This class contains functions related to data transformation and validation using the pandas and numpy libraries in Python.

#### Functions:

1. `remove_invalid_records(df, required_fields)`:
   - This function removes records from a DataFrame with missing required fields specified by `required_fields`.

2. `remove_invalid_characters(df, columns)`:
   - This function removes records with non-alphanumeric characters from specified columns in a DataFrame.

3. `fill_missing_values(data)`:
   - This function fills missing values with empty strings and replaces 'NaN' and 'nan' with blanks in a DataFrame.

4. `delete_nan_rows(df, columns)`:
   - This function deletes rows with NaN values in specified columns from a DataFrame.

5. `drop_columns(df, to_drop)`:
   - This function drops specified columns from a DataFrame.

6. `remove_duplicates(df)`:
   - This function removes duplicate rows from a DataFrame.

7. `validate_assets(asset_data)`:
   - This function performs data validation for asset records by removing records with invalid characters and duplicate entries.

8. `validate_entities(entity_data)`:
   - This function performs data validation for entity records by removing records with missing fields and duplicate entries.

9. `validate_join(join_data)`:
   - This function performs data validation for join records by removing records with missing fields and duplicate entries.

10. `create_cherry_asset_id(row)`:
    - This function creates a unique identifier ('cherry_asset_id') for a property based on its attributes.

11. `create_ownerships(row)`:
    - This function creates a list of ownership details for a property based on the provided row of data.

12. `merge_data(asset_data, entity_data, join_data)`:
    - This function merges asset, entity, and join data into a single DataFrame.

13. `convert_ownership_share_to_float(ownership_share)`:
    - This function converts the ownership share value to a floating-point number.

14. `transform_data(asset_data, entity_data, join_data)`:
    - This function transforms the input data to meet specified requirements including converting ownership share to float, merging dataframes, removing duplicates, filling missing values, creating new fields, and more.



```python
import pandas as pd
import numpy as np
import re
import ast
import json

def remove_invalid_records(df, required_fields):
    """
    Remove records from a DataFrame with missing required fields.

    Args:
    df (pd.DataFrame): The input DataFrame.
    required_fields (list): A list of column names representing the required fields.

    Returns:
    pd.DataFrame: DataFrame with invalid records removed.

    This function removes records from the input DataFrame where any of the required fields specified by 'required_fields' have missing values (NaN).
    """
    return df.dropna(subset=required_fields)


def remove_invalid_characters(df, columns):
    """
    Remove records with non-alphanumeric characters from specified columns in a DataFrame.

    Args:
    df (pd.DataFrame): The input DataFrame.
    columns (list): A list of column names to check for non-alphanumeric characters.

    Returns:
    pd.DataFrame: DataFrame with records removed where specified columns contain non-alphanumeric characters.
    """
    for column in columns:
        df[column] = df[column].astype(str)
        df = df[df[column].str.match(r'^[a-zA-Z0-9]+$')]
    return df


def fill_missing_values(data):
    """
    Fill missing values with empty strings and replace 'NaN' and 'nan' with blank in a DataFrame.

    Args:
    data (pd.DataFrame): The DataFrame to be processed.

    Returns:
    pd.DataFrame: The DataFrame with missing values filled with empty strings and 'NaN' and 'nan' replaced with blank.
    """
    processed_data = data.fillna('').replace(['NaN', 'nan'], '')
    return processed_data


def delete_nan_rows(df, columns):
    """
    Delete rows with NaN values in specified columns from a DataFrame.

    Args:
    df (pd.DataFrame): The input DataFrame.
    columns (list): A list of column names to check for NaN values.

    Returns:
    pd.DataFrame: DataFrame with rows removed where all specified columns have NaN values.
    """
    cleaned_df = df.dropna(subset=columns, how='all')
    return cleaned_df


def drop_columns(df, to_drop):
    """
    Drop specified columns from a DataFrame.

    Args:
    df (pd.DataFrame): The input DataFrame.
    to_drop (list): A list of column names to be dropped from the DataFrame.

    Returns:
    pd.DataFrame: DataFrame with specified columns removed.

    This function removes the specified columns from the input DataFrame.
    """
    return df.drop(columns=to_drop, errors='ignore')



def remove_duplicates(df):
    """
    Remove duplicate rows from a DataFrame.

    Args:
    df (pd.DataFrame): The input DataFrame.

    Returns:
    pd.DataFrame: DataFrame with duplicate rows removed.

    This function removes duplicate entries (rows) from the input DataFrame.
    """
    return df.drop_duplicates()


def validate_assets(asset_data):
    """
    Perform data validation for asset records.

    Args:
    asset_data (pd.DataFrame): DataFrame containing asset records.

    Returns:
    pd.DataFrame: DataFrame with validated asset records.

    This function performs data validation for asset records by removing records 
    with invalid characters in 'particella' and 'subalterno' fields and removing duplicate entries.
    """
    # Remove records where particella and subalterno fields contain characters other than digits and letters
    asset_data = remove_invalid_characters(asset_data, ['particella', 'subalterno'])

    # Remove duplicate entries
    asset_data = remove_duplicates(asset_data)

    return asset_data


def validate_entities(entity_data):
    """
    Perform data validation for entity records.

    Args:
    entity_data (pd.DataFrame): DataFrame containing entity records.

    Returns:
    pd.DataFrame: DataFrame with validated entity records.

    This function performs data validation for entity records by removing records with missing 'entity_id',
    'vatCode', or 'taxCode', removing duplicate entries, and returning the cleaned DataFrame.
    """
    entity_data = remove_invalid_records(entity_data, ['entity_id'])
    entity_data = delete_nan_rows(entity_data, ['vatCode', 'taxCode'])
    entity_data = remove_duplicates(entity_data)

    return entity_data


def validate_join(join_data):
    """
    Perform data validation for join records.

    Args:
    join_data (pd.DataFrame): DataFrame containing join records.

    Returns:
    pd.DataFrame: DataFrame with validated join records.

    This function performs data validation for join records by removing records
    with missing 'entity_id' or 'asset_id', removing duplicate entries, and returning the cleaned DataFrame.
    """
    required_fields = ['entity_id', 'asset_id']
    join_data = remove_invalid_records(join_data, required_fields)
    join_data = remove_duplicates(join_data)

    return join_data



def create_cherry_asset_id(row):
    """
    Create a unique identifier (cherry_asset_id) for a property based on its attributes.

    Args:
    row (pd.Series): Series containing the attributes of the property.

    Returns:
    str: Unique identifier (cherry_asset_id) for the property.
    """
    cherry_asset_id = f"{row['asset_id']}-{row['cityCode']}-{row['catasto']}-{row['foglio']}-{row['particella']}"
    return cherry_asset_id



def create_ownerships(row):
    """
    Create a list of ownership details for a property based on the provided row of data.

    Args:
        row (pd.Series): A row of data containing ownership information.

    Returns:
        list: List of ownership details as dictionaries.
    """
    ownerships = {
        'entity_id': row['entity_id'],
        'vatCode': row['vatCode'],
        'taxCode': row['taxCode'],
        'ownershipShare': row['ownershipShare']
    }
    return ownerships


def merge_data(asset_data, entity_data, join_data):
    """
    Merge asset, entity, and join data into a single DataFrame.

    Args:
        asset_data (pd.DataFrame): DataFrame containing asset records.
        entity_data (pd.DataFrame): DataFrame containing entity records.
        join_data (pd.DataFrame): DataFrame containing join information.

    Returns:
        pd.DataFrame: Merged DataFrame containing all data.
    """
    # Merge asset, entity, and join data based on common columns
    merged_data = pd.merge(join_data, entity_data, on='entity_id', how='outer')
    merged_data = pd.merge(merged_data, asset_data, on='asset_id', how='outer')
    return merged_data


def convert_ownership_share_to_float(ownership_share):
    """
    Convert the ownership share value to a floating-point number, rounding to 2 decimal places if applicable.

    Args:
        ownership_share (str): The ownership share value to be converted.

    Returns:
        float or None: The ownership share value as a floating-point number, rounded to 2 decimal places if applicable.
                       Returns None if the input cannot be converted to a valid floating-point number.
    """
    if ownership_share is None:
        return None
    elif '/' in ownership_share:
        numerator, denominator = ownership_share.split('/')
        try:
            float_value = float(numerator) / float(denominator)
            return round(float_value, 2)  # Round to 2 decimal places
        except ValueError:
            return None  # Return None if conversion fails
    else:
        try:
            return float(ownership_share)
        except ValueError:
            return None  # Return None if conversion fails




def transform_data(asset_data, entity_data, join_data):
    """
    Transform the input data to meet specified requirements.

    Args:
        asset_data (pd.DataFrame): DataFrame containing asset data.
        entity_data (pd.DataFrame): DataFrame containing entity data.
        join_data (pd.DataFrame): DataFrame containing join data.

    Returns:
        pd.DataFrame: Transformed DataFrame.

    This function performs several transformations on the input data:
    1. Converts the 'ownershipShare' column in 'join_data' to float values.
    2. Merges 'asset_data', 'entity_data', and 'join_data' DataFrames.
    3. Deletes rows with NaN values in 'vatCode' and 'taxCode' columns.
    4. Removes duplicate entries.
    5. Fills missing values with empty strings.
    6. Converts the 'foglio' column to string data type.
    7. Creates a new field 'cherry_asset_id' based on certain columns.
    8. Creates a new field 'ownerships' based on certain columns.
    """
    join_data['ownershipShare'] = join_data['ownershipShare'].apply(convert_ownership_share_to_float)

    merged_data = merge_data(asset_data, entity_data, join_data)
    merged_data = delete_nan_rows(merged_data, ['vatCode', 'taxCode'])
    merged_data = remove_duplicates(merged_data)
    merged_data = fill_missing_values(merged_data)
    merged_data['foglio'] = merged_data['foglio'].astype(str)
    merged_data['cherry_asset_id'] = merged_data.apply(create_cherry_asset_id, axis=1)
    merged_data['ownerships'] = merged_data.apply(create_ownerships, axis=1)
    merged_data['ownerships'] = merged_data['ownerships'].apply(lambda x: eval(x) if isinstance(x, str) else x)
    
    return merged_data
```

### load.py 

#### Class Summary: MongoDB Operations

This class contains functions related to performing operations with MongoDB using the pymongo library in Python.

#### Functions:

1. `convert_df_to_json(df: pd.DataFrame) -> List[dict]`:
   - This function converts a DataFrame to a list of dictionaries in JSON format. It selects specific columns from the input DataFrame and converts them into a list of dictionaries, with each dictionary representing a row of data in JSON format.

2. `delete_records(collection: str)`:
   - This function deletes all documents from a MongoDB collection specified by the collection name.

3. `insert_records(collection: str, records: list)`:
   - This function inserts records into a MongoDB collection specified by the collection name. The records parameter should be a list of dictionaries representing the records to be inserted into the collection.

```python
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

```

### main.py 

#### Class Summary: ETL Pipeline with FastAPI and MongoDB

This class contains functions related to orchestrating an Extract, Transform, Load (ETL) pipeline using FastAPI and MongoDB for data ingestion and retrieval.

#### Functions:

1. `etl_pipeline()`:
   - This function serves as the main entry point of the data pipeline. It orchestrates the ETL process by extracting, validating, transforming, and loading the data into a MongoDB collection.

2. `read_data()`:
   - This function retrieves all data from a specific MongoDB collection. It triggers the ETL process, retrieves all records from the MongoDB collection, and returns them in JSON format.

3. `get_record_by_city_code(citycode: str)`:
   - This function retrieves details of a record from MongoDB based on the cityCode. It searches for the specified cityCode in the MongoDB collection and returns the details of the record in JSON format if found.

```python
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
username = os.getenv("MONGODB_USERNAME")
password = os.getenv("MONGODB_PASSWORD")
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

```

# **Environment Variables (.env)**

####  Usage of .env File and python-dotenv Library

- **Secure Management:**
  - `.env` file securely manages sensitive environment variables, such as database credentials.
  - `python-dotenv` library and `load_dotenv()` function ensure sensitive information remains private and not exposed in the codebase.
  - Environment-specific configurations, like MongoDB cluster URI and database details, are stored in `.env`, isolating them from the application code.
  - Separating configurations in `.env` promotes flexibility and maintainability, allowing easy updates without modifying the application code.
  - Utilizing `.env` and `python-dotenv` aligns with best practices for managing environment-specific configurations, ensuring security and maintainability.

The following environment variables are used to configure the MongoDB connection:

- `CLUSTER_URI`: URI of the MongoDB cluster.
  - Example: `mongodb+srv://jojoyadav255:CbS1zFtduhiTwQB4@cluster0.912iw8i.mongodb.net/?retryWrites=true&w=majority`
  - This URI specifies the username (`jojoyadav255`), password (`CbS1zFtduhiTwQB4`), and MongoDB cluster details (`cluster0.912iw8i.mongodb.net`) required to connect to the MongoDB Atlas cluster.

- `MONGODB_DATABASE`: Name of the MongoDB database.
  - Example: `database`
  - This variable specifies the name of the MongoDB database to connect to.

- `MONGODB_COLLECTION`: Name of the MongoDB collection.
  - Example: `collection`
  - This variable specifies the name of the MongoDB collection within the specified database where data will be stored or retrieved.


```dotenv
```

# **Requirements.txt**

#### Brief Overview of Python Libraries Used

  - **numpy:**
    - `numpy` is a powerful library for numerical computing in Python, providing support for arrays, matrices, and mathematical functions.
  
  - **pandas:**
    - `pandas` is a versatile library for data manipulation and analysis, offering data structures like DataFrame and tools for reading and writing data in various formats.
  
  - **tabulate:**
    - `tabulate` is a convenient library for formatting and displaying tabular data in Python, providing functions to create visually appealing tables.
  
  - **fastapi:**
    - `fastapi` is a modern web framework for building APIs with Python, known for its high performance, automatic validation, and easy-to-use asynchronous capabilities.
  
  - **pymongo:**
    - `pymongo` is the official Python driver for MongoDB, allowing Python applications to interact with MongoDB databases by providing a simple API for CRUD operations.
  
  - **uvicorn:**
    - `uvicorn` is a lightning-fast ASGI server for running Python web applications, enabling the deployment of ASGI applications with minimal configuration.
  
  - **python-dotenv:**
    - `python-dotenv` is a library for managing environment variables in Python applications, facilitating the loading of environment variables from a `.env` file into the application's environment.


```plaintext
numpy
pandas
tabulate
fastapi
pymongo
uvicorn
python-dotenv
```

# MongoDB

MongoDB is a popular NoSQL database management system known for its flexibility, scalability, and ease of use. In the project, MongoDB was utilized via MongoDB Atlas, the cloud-based database service offered by MongoDB. MongoDB Atlas provides a fully managed and scalable database solution, enabling efficient storage, retrieval, and management of data without the need for infrastructure management.

![Alt text](<images/Screenshot 2024-02-11 at 19.20.18.png>)


# **Dockerfile & Docker-compose**


#### Dockerfile

The Dockerfile defines the steps required to build a Docker image for the application. It starts with a base Python image, sets the working directory, defines a volume for data persistence, installs dependencies, copies the application code, and specifies the default command to run the application.

```Dockerfile
FROM python:3.9

# Set the working directory inside the container
WORKDIR /code
 
# Define a volume for the /dataset directory
VOLUME /dataset 

# Copy the requirements.txt file into the container at /code/requirements.txt
COPY ./requirements.txt /code/requirements.txt
 
# Install the required Python packages
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
# Copy the contents of the app directory into the container at /code/app
COPY ./app /code/app
 
# Set the default command to run when the container starts
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

###  Docker-compose

The docker-compose.yml file orchestrates the deployment of multiple containers using Docker Compose. It specifies the services required for the application, including the web service for the application container and the mongo service for the MongoDB container. It defines the build context, port mappings, service dependencies, and data volume mappings for each service, allowing for easy management and deployment of the application environment.

```yaml
version: '3.8'

services:
  web:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    depends_on:
      - mongo
    volumes:
      - ./dataset:/dataset

  mongo:
    image: mongo
    ports:
      - "27017:27017"
```


# **FastAPI Web Application**

#### `/data` Endpoint:
- Retrieves all data from a specific MongoDB collection.
- Returns data in JSON format.
- Triggers the ETL process to ensure data integrity.
- Uses `collection.find({})` to retrieve all records from the MongoDB collection.
- Converts ObjectId to string for serialization.
- Returns a JSON response containing all records.

![Alt text](<images/Screenshot 2024-02-11 at 19.35.31.png>)

![Alt text](<images/Screenshot 2024-02-11 at 19.36.36.png>)

![Alt text](<images/Screenshot 2024-02-11 at 19.37.10.png>)

![Alt text](<images/Screenshot 2024-02-11 at 19.37.30.png>)


#### `/data/{citycode}` Endpoint:
- Retrieves details of a record from MongoDB based on the provided city code.
- Returns data in JSON format.
- Queries the database using `collection.find_one({"cityCode": citycode})`.
- Converts ObjectId to string for serialization.
- Returns a JSON response containing the record details.
- Returns a 404 Not Found response if no record is found.

![Alt text](<images/Screenshot 2024-02-11 at 19.37.54.png>)

![Alt text](<images/Screenshot 2024-02-11 at 19.38.25.png>)

![Alt text](<images/Screenshot 2024-02-11 at 19.38.43.png>)



# **Google Cloud Platform (Deployment)**

### Benefits of Deploying on Google Cloud Run

- **Scalability**:
  - Managed Autoscaling: Automatically scales based on incoming traffic.
  - Horizontal Scaling: Can handle increased traffic by spinning up additional container instances.

- **Durability**:
  - High Availability: Runs in a fault-tolerant environment distributed across multiple Google Cloud regions.
  - Automated Load Balancing: Distributes incoming traffic across multiple instances for continuous availability.

- **Security**:
  - VPC Service Controls: Integrates with Google Cloud's security perimeters for data access control.
  - Built-in IAM: Defines fine-grained access controls and permissions for managing resources.

- **Environment Variables**:
  - Secret Manager Integration: Securely stores sensitive configuration data.
  - Secure Handling: References secrets as environment variables for secure application configuration.


![Alt text](<images/Screenshot 2024-02-11 at 19.52.00.png>)


```bash
docker buildx build --platform linux/amd64 -t jyotiyadav79811/etl_pipeline:1.0.9 .
```
![Alt text](<images/Screenshot 2024-02-11 at 19.59.23.png>)

```bash
docker push jyotiyadav79811/etl_pipeline:1.0.9
```
![Alt text](<images/Screenshot 2024-02-11 at 20.00.35.png>)

![Alt text](<images/Screenshot 2024-02-11 at 20.01.53.png>)

![Alt text](<images/Screenshot 2024-02-11 at 20.17.50.png>)

![Alt text](<images/Screenshot 2024-02-11 at 20.18.57.png>)

![Alt text](<images/Screenshot 2024-02-11 at 20.19.22.png>)


# **Pytests**

### Test Run successfully

![Alt text](<images/Screenshot 2024-02-11 at 20.35.14.png>)


 ### test_extract.py

#### **TestLoadCsv**
  - Test that `load_csv` returns a pandas DataFrame when given a valid file path.
  - Test that `load_csv` returns a FileNotFoundError when given an invalid file path.
  - Test that `load_csv` returns a pd.errors.EmptyDataError when given an empty file path.
 
```python
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

```

### test_transform.py

#### **TestTransformFunctions**
- Test filling missing values with empty strings.
- Test dropping specified columns.
- Test removing duplicate entries.
- Test validating asset records.
- Test validating entity records.
- Test validating join records.
- Test removing invalid characters from specified columns.

```python
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
```

### test_load.py

#### **TestInsertRecords**
- Test the conversion of a DataFrame to a list of dictionaries in JSON format.

```python

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

```

# **gitignore **

### Git Ignore Rules

1. **Python Bytecode Files:**
   - Bytecode files generated by the Python interpreter are ignored.
   - These files are stored in the `__pycache__` directory.

2. **Jupyter Notebook Checkpoints:**
   - Checkpoint files created by Jupyter Notebooks are ignored.
   - These files are stored in the `.ipynb_checkpoints` directory.

3. **Pytest Cache and History Files:**
   - Cache and history files generated by pytest are ignored.
   - These files are typically stored in directories named `.history` and `.pytest_cache`.

These rules help maintain a cleaner repository by excluding unnecessary or autogenerated files and directories from version control.

```plaintext
# Ignore Python bytecode files
__pycache__/

# Ignore Jupyter Notebook checkpoints
.ipynb_checkpoints/

# Ignore pytest cache and history files
.history/
.pytest_cache/
**.pytest_cache/

```

# **Feedback**
* Feedback on this project would be greatly appreciated. I value your insights and suggestions to improve its effectiveness and quality. Thank you for providing this opportunity


# Author
-------------------------------
[Jyoti Yadav](https://www.linkedin.com/in/jyoti-yadav-64916b160/)

