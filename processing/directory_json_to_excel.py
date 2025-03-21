import os
import json
import pandas as pd
from pathlib import Path

# Set the directory path where your JSON files are stored
json_directory = 'your_JSON_output_directory'

# Prepare a list to hold data
data_for_excel = []

# List of all possible categories, you can change this to your own categories, or if you want to replicate the original categories, you can use this list.
all_categories = ['SIT', 'STD', "ECP",
                 'ART','HTR',
                  'HFN', 'HTC',
                  'LTB', "HRL"]

# Iterate over all JSON files in the specified directory
for json_file_path in Path(json_directory).glob('*.json'):
    try:
        # Read the JSON file
        with open(json_file_path, 'r') as file:
            json_data = json.load(file)

        # Extract the 'content' field from the 'choices' list
        content = json_data['choices'][0]['message']['content']

        # Split the content to get the categories
        categories = content.split(', ')

        # Create a dictionary to store binary values for each category
        category_dict = {category: 0 for category in all_categories}

        # Set the binary values for the present categories
        for category in categories:
            category_dict[category] = 1

        # Append the extracted data to our list
        data_for_excel.append({
            'Name': json_file_path.stem,
            **category_dict
        })

    except (KeyError, IndexError) as e:
        # Log the file path and the error
        print(f"{json_file_path.name}: {str(e)}")

# Create a dataframe from the data
df = pd.DataFrame(data_for_excel)

# Write the dataframe to an Excel file
output_excel_file = 'your_output_excel_file_name.xlsx'
df.to_excel(output_excel_file, index=False)