from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
import json

class ActionFetchPersonDetails(Action):

    def name(self) -> Text:
        return "action_fetch_person_details"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the person's name from the slot or from the last user message
        person_name = tracker.get_slot("person") or tracker.latest_message.get('entities')[0].get('value')
        
        # Load the data from the JSON file
        with open('C:\\Sketo\\BHASAKR\\RASA\\Data\\data_extended.json', 'r') as json_file:
            data = json.load(json_file)
        
        # Fetch details for the given name
        details = data.get(person_name, {"message": "Person not found in our database."})
        
        # Check the intent and respond accordingly
        last_intent = tracker.latest_message.get('intent').get('name')
        
        response = {
            "person_birthplace": f"{person_name} was born in {details.get('birthplace', 'unknown place')}.",
            "person_profession": f"{person_name} is known as {details.get('profession', 'unknown profession')}.",
            "person_date_of_birth": f"{person_name} was born on {details.get('date_of_birth', 'unknown date')}.",
            "person_nationality": f"{person_name} is {details.get('nationality', 'of unknown nationality')}.",
            "person_education": f"{person_name} studied at {details.get('education', 'unknown institution')}.",
            "person_known_for": f"{person_name} is known for {details.get('known_for', 'unknown reasons')}."
        }.get(last_intent, f"{person_name} was born in {details.get('birthplace', 'unknown place')}, and is known as {details.get('profession', 'unknown profession')}.")
        
        # Respond with the details
        dispatcher.utter_message(text=response)

        # Set the person slot for future reference
        return [SlotSet("person", person_name)]

from rasa_sdk.events import UserUtteranceReverted



from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionDefaultFallback(Action):
    def name(self) -> str:
        return "action_default_fallback"
    
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: dict) -> list:
        # Access the last user message's intent confidence
        confidence = tracker.latest_message.get("intent", {}).get("confidence", 1.0)

        if confidence < 0.4:
            # If confidence is below threshold, set the slot
            dispatcher.utter_message(text="I'm sorry, I didn't understand that. Could you rephrase or provide more details?")
            return [SlotSet("predicted_confidence_below_threshold", True)]
        else:
            return []


# import pandas as pd

# def analyze_sales_data(file_path):
#     # Read the CSV file
#     df = pd.read_csv(file_path)

#     # Perform your analysis here
#     # Example: Calculate the increase in sales, popular products, etc.
#     # Return a narrative based on the analysis

#     narrative = "Sales have increased by 20% in the last quarter. The biggest increase has come from customers aged 25-34, whose purchases have gone up by 35%. The most popular product category for this age group was electronics, with smartphones being the most purchased product. Most purchases were made late in the evening."
#     return narrative

import pandas as pd

def analyze_sales_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)

    # Perform the analysis
    # Calculate the overall sales increase in the last quarter (Q4)
    q4_sales = df[df['Quarter'] == 'Q4']['Purchase Amount'].sum()
    other_quarter_sales = df[df['Quarter'] != 'Q4']['Purchase Amount'].sum()
    sales_increase = ((q4_sales - other_quarter_sales) / other_quarter_sales) * 100

    # Calculate the increase in purchases for the 25-34 age group in Q4
    age_group_sales_q4 = df[(df['Quarter'] == 'Q4') & (df['Age Group'] == '25-34')]['Purchase Amount'].sum()
    age_group_sales_other = df[(df['Quarter'] != 'Q4') & (df['Age Group'] == '25-34')]['Purchase Amount'].sum()
    age_group_increase = ((age_group_sales_q4 - age_group_sales_other) / age_group_sales_other) * 100

    # Find the most popular product category for the 25-34 age group in Q4
    popular_category = df[(df['Quarter'] == 'Q4') & (df['Age Group'] == '25-34')]['Product Category'].value_counts().idxmax()

    # Check if smartphones are the most purchased product in the electronics category for the 25-34 age group in Q4
    smartphone_sales = df[(df['Quarter'] == 'Q4') & (df['Age Group'] == '25-34') & (df['Product Category'] == 'Electronics') & (df['Specific Product'] == 'Smartphone')].shape[0]
    electronics_sales = df[(df['Quarter'] == 'Q4') & (df['Age Group'] == '25-34') & (df['Product Category'] == 'Electronics')].shape[0]
    smartphone_most_purchased = smartphone_sales == electronics_sales

    # Find the most common time of purchase in Q4
    common_purchase_time = df[df['Quarter'] == 'Q4']['Time of Day'].value_counts().idxmax()

    # Construct the narrative
    narrative = f"Sales have increased by {sales_increase:.2f}% in the last quarter. The biggest increase has come from customers aged 25-34, whose purchases have gone up by {age_group_increase:.2f}%. The most popular product category for this age group was {popular_category.lower()}, with smartphones being the most purchased product" if smartphone_most_purchased else "one of the most purchased products"
    narrative += f". Most purchases were made {common_purchase_time.lower()}."

    return narrative

# # Usage example (replace with your actual file path)
# file_path = '/path/to/your/csvfile.csv'
# print(analyze_sales_data(file_path))



from rasa_sdk import Action

class ActionAnalyzeSales(Action):
    def name(self):
        return "action_analyze_sales"

    async def run(self, dispatcher, tracker, domain):
        # Path to your CSV file
        file_path = 'C:\\Sketo\\BHASAKR\RASA\\sales_data_example.csv'

        # Get the narrative
        narrative = analyze_sales_data(file_path)

        # Send the narrative to the user
        dispatcher.utter_message(text=narrative)

        return []


import pandas as pd

def describe_dataframe(df):
    description = []

    for column in df.columns:
        col_data = df[column]
        col_desc = {
            'Column': column,
            'Count': col_data.count(),
            'Unique': col_data.nunique(),
            'Representation': col_data.dtypes
        }

        # Check if the column is numeric or not
        if pd.api.types.is_numeric_dtype(col_data):
            col_desc['Mean'] = col_data.mean()
            col_desc['Median'] = col_data.median()
            col_desc['Min'] = col_data.min()
            col_desc['Max'] = col_data.max()
            col_desc['Avg'] = col_data.mean()
            col_desc['Abs'] = col_data.abs().mean()
            col_desc['Category'] = 'Measure'
        else:
            col_desc.update({'Mean': 'N/A', 'Median': 'N/A', 'Min': 'N/A', 'Max': 'N/A', 'Avg': 'N/A', 'Abs': 'N/A'})
            if col_data.dtype == 'object':
                col_desc['Category'] = 'Nominal'
            else:
                col_desc['Category'] = 'Enum'

        description.append(col_desc)

    return description

# Example usage
# df = pd.read_csv('your_data.csv')
# result = describe_dataframe(df)
# print(result)


import pandas as pd
from rasa_sdk import Action
from rasa_sdk.events import SlotSet

class ActionDescribeDataFrame(Action):
    def name(self):
        return "action_describe_dataframe"

    async def run(self, dispatcher, tracker, domain):
        # Assuming the DataFrame is loaded from a CSV file
        # You can modify this part to suit how you obtain your DataFrame
        file_path = 'C:\\Sketo\\BHASAKR\RASA\\sales_data_example.csv'
        df = pd.read_csv(file_path)
        

        # Get the description of the DataFrame
        description = describe_dataframe(df)

        # Create a response message
        response_message = "Here's the description of the dataset:\n"
        for col_desc in description:
            response_message += f"\nColumn: {col_desc['Column']}, Count: {col_desc['Count']}, Unique: {col_desc['Unique']}, Mean: {col_desc['Mean']}, Median: {col_desc['Median']}, Min: {col_desc['Min']}, Max: {col_desc['Max']}, Avg: {col_desc['Avg']}, Abs: {col_desc['Abs']}, Representation: {col_desc['Representation']}, Category: {col_desc['Category']}"

        # Send the response message
        dispatcher.utter_message(text=response_message)

        return []
