from langchain_core.prompts import ChatPromptTemplate
from deep_translator import GoogleTranslator
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain_groq import ChatGroq
from langchain.agents import Tool
from dotenv import load_dotenv, find_dotenv
from etl_pipeline.etl_pipeline.load import save_df_to_csv
import warnings
import pandas as pd
warnings.filterwarnings('ignore')
from dotenv import find_dotenv
from groq import Groq
import pandas as pd
import wikipedia
import ast
import os

# Load environment variables
config = find_dotenv(".env")
load_dotenv()

## load the env
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
TEMPERATURE = os.getenv("TEMPERATURE")
MAX_TOKENS=os.getenv("MAX_TOKENS")
MODEL=os.getenv("MODEL")

client = Groq(api_key=GROQ_API_KEY,)
llm = ChatGroq(temperature=TEMPERATURE, 
               groq_api_key=GROQ_API_KEY,
               model_name=MODEL,
               max_tokens=MAX_TOKENS) 

def get_llm_output(prompt):
    print("get_llm_output started")
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model=MODEL,
    )
    print("get_llm_output ended")
    return (chat_completion.choices[0].message.content)


def collect_recipe(df, i):
    """
    collects name and ingredients from the df and rows collects the number of rows upon which operation has to be performed
    df: df containing the name and ingredients "Nome" and "ingredienti"
    rows: number of rows to be collected (default 1)
    """
    print("collect_recipe started")
    name = df["Nome"].iloc[i]
    ingredients = ast.literal_eval(df["Ingredienti"].iloc[i])
    # drop the second value in list
    for i in range(len(ingredients)):
        ingredients[i] = ingredients[i][0]
    wiki_data = wikipedia.search(name)
    print("collect_recipe ended")
    return [name, ingredients, wiki_data]


def set_prompt(dish_list):
    print("set_prompt started")
    name, ingredients, description = dish_list[0], dish_list[1], dish_list[2]
    # Define prompt
    prompt_template = f"""Write a concise summary based on the dish name
    "{name}" and ingredients "{ingredients}". Do not mention the ingredients in final output.
    FINAL CONCISE SUMMARY:"""
    print("set_prompt ended")
    return prompt_template

def set_prompt_allergen(dish_list):
    print("set_prompt_allergen started")
    name, ingredients, description = dish_list[0], dish_list[1], dish_list[2]
    # Define prompt
    prompt_template = f"""Given the name
    "{name}" and ingredients "{ingredients}".
    Find the allergen from the list  [Cereals, Crustaceans, Egg, Fish, Peanuts, SOYBEAN, Latte, Nuts, Celery, Mustard, Sesame seeds, Sulfur dioxide and sulphites, Shell, Clams]
    OUTPUT should be a list.
    OUTPUT ALLERGEN LIST:<list>"""
    print("set_prompt_allergen ended")
    return prompt_template

def set_prompt_option(dish_list):
    name, ingredients, description = dish_list[0], dish_list[1], dish_list[2]
    # Define prompt
    prompt_template = f"""Given the name
    "{name}" and ingredients "{ingredients}".
    Choose values from the list that matches the dish:[Spicy, Vegan, Gluten free, Vegetarian]. reduce the output size in maximum 2 words. return nothing if not found.
    OUTPUT OPTION LIST [Spicy, Vegan, Gluten free, Vegetarian] :"""
    return prompt_template

def find_words_in_sentence(sentence, word_list):
    print("find_words_in_sentence started")
    words_found = []
    for word in word_list:
        if word.lower() in sentence.lower():
            words_found.append(word)
    print("find_words_in_sentence ended")
    return words_found


def processs_menu_data(asset_records):
    print("processs_menu_data started")
    # Initialize an empty DataFrame
    df_new = pd.DataFrame(columns=["name", "ingredients", "description", "allergen", "option"])

    # Process the first 500 rows
    for i in range(min(5, asset_records.shape[0])):
        dish_data = {}

        # Name and description
        dish_nds_list = collect_recipe(asset_records, i)
        basic_prompt = set_prompt(dish_nds_list)
        dish_data["name"] = dish_nds_list[0]
        dish_data["ingredients"] = dish_nds_list[1]
        dish_data["description"] = get_llm_output(basic_prompt)

        # Allergen list
        basic_prompt = set_prompt_allergen(dish_nds_list)
        output = get_llm_output(basic_prompt)
        allergen_list = ["Cereals", "Crustaceans", "Egg", "Fish", "Peanuts", "SOYBEAN", "Latte", "Nuts", "Celery", "Mustard", "Sesame seeds", "Sulfur dioxide and sulphites", "Shell", "Clams"]
        dish_data["allergen"] = find_words_in_sentence(output, allergen_list)

        # Options for dish
        basic_prompt = set_prompt_option(dish_nds_list)
        output = get_llm_output(basic_prompt)
        dish_option_list = ["Spicy", "Vegan", "Gluten free", "Vegetarian"]
        dish_data["option"] = find_words_in_sentence(output, dish_option_list)
        
        # Append the dictionary as a new row to the DataFrame
        df_new = pd.concat([df_new, pd.DataFrame([dish_data])], ignore_index=True)

    # Return the DataFrame
    print("processs_menu_data ended")
    return df_new



def create_text_column(df):
    """
    Creates the 'Text' column based on existing columns.
    """
    df['Text'] = df.apply(lambda row: {
        "ingredients": row['ingredients'],
        "description": row['description'],
        "allergen": row['allergen'],
        "Additional_information": row['option']
    }, axis=1)
    return df


def transform_dataframe(df_transform, INS):
    """
    Transforms the DataFrame by generating 'Text' based on 'INS' and input data.
    """
    print("transform_dataframe started")
    for i in range(len(df_transform)):
        input_data = df_transform['name'][i]
        output_data = df_transform['Text'][i]
        prompt = f"{INS} \n ### Input data: \n {input_data} \n ### Output: \n {output_data}"
        df_transform['Text'].iloc[i] = prompt
    # Drop unnecessary columns
    df_transform.drop(columns=['name','ingredients','description','allergen','option'], inplace=True)
    print("transform_dataframe ended")
    return df_transform  # Returning the first few rows for demonstration


def translate_text_column_to_english(df):
    """
    Translate the 'Text' column of a DataFrame from any language to English.
    """
    print("transform_dataframe started")
    # Copy the original DataFrame to avoid modifying the original data
    translated_df = df.copy()

    # Translate each text in the 'Text' column to English
    translated_df['Text'] = translated_df['Text'].apply(lambda text: GoogleTranslator(source='it', target='en').translate(text))
    print("transform_dataframe ended")
    return translated_df




