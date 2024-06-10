import json
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Define a function to either load a configuration from a JSON file or save a given configuration to a file.
def load_or_save_config(load=True, path=None, config=None):
    if load:
        with open(path, 'r') as file:
            return json.load(file)
    else:
        with open(path, 'w') as file:
            json.dump(config, file, indent=4)

# Prompt the user to specify if they have a configuration file to use
use_config = input("Do you have a config file? (y/n): ").lower()
config = {}

# If user has a configuration file, attempt to load it
if use_config == 'y':
    config_path = input("Enter the path to your config file: ")
    if os.path.exists(config_path):
        config = load_or_save_config(load=True, path=config_path)
    else:
        print("Config file not found, proceeding with manual setup.")
        use_config = 'n'

# Manual setup for collecting necessary parameters if no configuration file is used
if use_config == 'n':
    # Manual Setup
    ACCOUNT_NUMBER = input("Enter your account number: ")
    key_part_of_token = input("Enter the key part of your API token: ")
    AUTHORIZATION_TOKEN = f"Token {key_part_of_token}"  # Construct the authorization token using the provided key part
    # Collect start and end dates for the data query, allowing for an empty input to select the entire range
    START_DATE = input("Enter the start date (YYYY-MM-DD) or press Enter for the earliest records: ")
    END_DATE = input("Enter the end date (YYYY-MM-DD) or press Enter for the latest records: ")

    # Assemble the configuration dictionary with the collected inputs
    config = {
        "ACCOUNT_NUMBER": ACCOUNT_NUMBER,
        "AUTHORIZATION_TOKEN": AUTHORIZATION_TOKEN,
        "START_DATE": START_DATE,
        "END_DATE": END_DATE
    }

else:
    # Load from Config
    ACCOUNT_NUMBER = config.get("ACCOUNT_NUMBER")
    AUTHORIZATION_TOKEN = config.get("AUTHORIZATION_TOKEN")
    START_DATE = config.get("START_DATE", "")
    END_DATE = config.get("END_DATE", "")

# Setup base URL and headers for API requests
BASE_URL = 'https://aware.advact.ch/api'
HEADERS = {
    'Authorization': AUTHORIZATION_TOKEN,
    'Content-Type': 'application/json',
}

# Function to fetch available services from the API
def get_services():
    url = f'{BASE_URL}/service/?account={ACCOUNT_NUMBER}'
    response = requests.get(url, headers=HEADERS)

    if response.status_code == 200:
        services = response.json()
        print("Available Services:")
        user_friendly_id_to_original_id = {}
        for i, service in enumerate(services, start=1):
            print(f'ID: {i} - Name: {service["name"]}')
            user_friendly_id_to_original_id[i] = service["id"]
        return user_friendly_id_to_original_id
    else:
        print(response.content)
        return {}

# Function to fetch custom fields from the API
def get_custom_fields():
    url = f'{BASE_URL}/customfield/?account={ACCOUNT_NUMBER}'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        # Initialize an empty list to store custom fields' info
        custom_fields = []
        for item in data:
            # Create a dictionary for each custom field containing only its id and field_values
            field_info = {
                'id': item['id'],  # Directly access the ID
                'field_values': item['field_values']  # Directly access the field_values
            }
            custom_fields.append(field_info)  # Add the dictionary to the list
        return custom_fields  # Return the list of dictionaries
    else:
        print(response.content)
        return []  # Return an empty list in case of a non-200 response

# Function to fetch report data for a specific custom field and service
def get_report_data(custom_field, SERVICE_NUMBER, custom_field_id):
    url = f'{BASE_URL}/report/single/?account={ACCOUNT_NUMBER}&start_date={START_DATE}&end_date={END_DATE}&attack_type_filter=&field_filter=&service_filter={SERVICE_NUMBER}&template_filter=&field=&template_only=true&field_filters=%5B%7B%22fieldId%22%3A{custom_field_id}%2C%22value%22%3A%5B%22{custom_field}%22%5D%7D%5D'
    response = requests.get(url, headers=HEADERS)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list):
            return {'data': data}
        return data
    else:
        print(response.content)
        return None

# Function to extract and format the report data into a pandas DataFrame
def extract_data(json_data):
    data_content = json_data.get('data', [])
    data_extracted = []
    for d in data_content:
        if 'data' in d and all(k in d['data'] for k in ['ok_percent', 'link_clicked_percent', 'wrong_behaviour_percent']):
            data_extracted.append({
                'Scenario': d['value'],
                'OK': round(d['data']['ok_percent']),
                'Only Link Clicked': round(d['data']['link_clicked_percent']),
                'Wrong Behaviour': round(d['data']['wrong_behaviour_percent'])
            })
    return pd.DataFrame(data_extracted)

# Function to plot a stacked bar chart for the extracted data
def plot_stacked_bar_chart(df, custom_field, start_date, end_date):
    sns.set_style("whitegrid")

    # Dynamic figure size based on the number of records
    base_height = 8  # Minimum height for the figure
    height_per_record = 0.3  # Additional height per record
    total_height = base_height + len(df) * height_per_record
    plt.figure(figsize=(12, max(total_height, base_height)))

    positions = range(len(df))

    bars_ok = plt.barh(positions, df['OK'], color='lightgreen', edgecolor='white', height=0.6, label='OK')
    bars_link_clicked = plt.barh(positions, df['Only Link Clicked'], left=df['OK'], color='orange', edgecolor='white', height=0.6, label='Only Link Clicked')
    bars_wrong = plt.barh(positions, df['Wrong Behaviour'], left=df['OK'] + df['Only Link Clicked'], color='salmon', edgecolor='white', height=0.6, label='Wrong Behaviour')

    plt.yticks(positions, df['Scenario'], fontsize=12)
    plt.xticks(fontsize=10)
    plt.xlabel('Percentage', fontsize=14)

    # Adjust title to handle empty start or end date
    date_range = f"({start_date} - {end_date})" if start_date and end_date else "All time"
    full_title = f"{custom_field} {date_range}"
    plt.title(full_title, fontsize=16)

    for bars in [bars_ok, bars_link_clicked, bars_wrong]:
        for bar in bars:
            width = bar.get_width()
            label_x_pos = bar.get_x() + width / 2
            if width > 0:
                plt.text(label_x_pos, bar.get_y() + bar.get_height() / 2, f'{width}%', ha='center', va='center', color='black', fontsize=10)

    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), shadow=True, ncol=3, fontsize=12)
    plt.tight_layout()

    file_name = f'{custom_field.replace(" ", "_").replace("/", "_")}.png'
    plt.savefig(file_name)
    plt.close()

# Main function to orchestrate the fetching of services, custom fields, and generating reports
def main():
    # services = get_services()
    custom_fields_data = get_custom_fields()

    user_friendly_id_to_original_id = get_services()

    if user_friendly_id_to_original_id:
        # Ask the user to enter the service number based on the printed list
        selected_service_user_friendly_id = int(input("Enter the service number (Leave empty if all should be selected): "))

        # Translate user-friendly ID to actual service ID
        actual_service_id = user_friendly_id_to_original_id.get(selected_service_user_friendly_id)

        # Now you can use `actual_service_id` for API requests where needed
        # For example, when fetching report data or any other operation that requires the service ID
    else:
        print("No services available or an error occurred.")
        return

    for field_data in custom_fields_data:
        custom_field_id = field_data['id']  # Extract the ID of the custom field
        for custom_field_value in field_data['field_values']:  # Iterate over each value in field_values
            # Now pass both custom_field_value and custom_field_id to get_report_data
            report_data = get_report_data(custom_field_value, actual_service_id, custom_field_id)
            if report_data:
                df = extract_data(report_data)
                if not df.empty:
                    plot_stacked_bar_chart(df, custom_field_value, START_DATE, END_DATE)
                    print(f"Successfully created the stacked bar chart for '{custom_field_value}'")
                else:
                    print(f"No relevant data found for '{custom_field_value}'. Skipping this custom field.")
            else:
                print(f"No report data returned for '{custom_field_value}'. Skipping this custom field.")

    if use_config == 'n':
        save_config = input("Would you like to save your settings to a config file? (y/n): ").lower()
        if save_config == 'y':
            config_path = input("Enter the full path and filename to save your config file (e.g., C:\\Users\\YourName\\Desktop\\config.json): ")
            try:
                load_or_save_config(load=False, path=config_path, config=config)
                print("Config file saved.")
            except FileNotFoundError as e:
                print(f"Error saving config file: {e}")

if __name__ == "__main__":
    main()
