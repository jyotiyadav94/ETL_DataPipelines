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

