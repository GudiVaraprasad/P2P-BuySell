import json
import os

# Path to save the CSV file
config_json_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'network', 'config.json')

# Load the configuration from the config.json file
def load_config():
    with open(config_json_file_path, "r") as file:
        config = json.load(file)
    return config