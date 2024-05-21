import os
import json
import logging
import wikipedia
import pandas as pd
from dotenv import load_dotenv, find_dotenv
from etl_pipeline.etl_pipeline.extract import load_csv,print_tabulated_data
from etl_pipeline.etl_pipeline.transform import processs_menu_data,create_text_column,transform_dataframe,translate_text_column_to_english
from etl_pipeline.etl_pipeline.load import delete_collection_data,insert_dataframe_to_collection,query_collection_to_dataframe,save_df_to_csv

# Load environment variables
config = find_dotenv(".env")
load_dotenv()

cluster_uri = os.getenv("CLUSTER_URI")
database = os.getenv("MONGODB_DATABASE")
collection=os.getenv("MONGODB_COLLECTION")


### define the prompts
MENU_PROMPT = """
<s>[INST]    As a restaurant menu manager, your role is to gather below informations based on input data (Name of the dish).
generate the output 
    
### information to be extracted :
<Ingredients>: Only Ingredients included in the dish.
<Description>: Briefly describe the dish.
<Allergens>: Only Choose relevant options from this list - [Cereals, Crustaceans, Egg, Fish, Peanuts, SOYBEAN, Latte, Nuts, Celery, Mustard, Sesame seeds, Sulfur dioxide and sulphites, Shell, Clams].
<Additional Information>: Only Choose relevant options from this list - [Spicy, Vegan, Gluten free, Vegetarian].

### Output Format 
"ingredients": All Ingredients in a List,
"description": Description in a string,
"allergen": All allergen in a List,
"Additional_information": All Additional_information in a List
"""


def run_etl_pipeline():
    source_folder = 'datasets/'
    
    asset_file = os.path.join(source_folder, 'gz_recipe.csv')
    asset_records = load_csv(asset_file)
    processed_df = processs_menu_data(asset_records)
    df=create_text_column(processed_df)
    df=transform_dataframe(df,MENU_PROMPT)
    #print_tabulated_data(df)
    translated_df=translate_text_column_to_english(df)
    save_df_to_csv(translated_df)
    
    ## dataset to be stored in the Mongo Database
    dataframe_dict = {'MenuDataset': translated_df}
    delete_collection_data(database, collection, cluster_uri)
    insert_dataframe_to_collection(database, collection, cluster_uri,dataframe_dict)
    df=query_collection_to_dataframe(database, collection, cluster_uri)
    print_tabulated_data(df)



