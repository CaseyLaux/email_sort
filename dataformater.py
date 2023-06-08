import os
import json

# Directory path containing the JSON files
directory = 'C:\\Users\\casey\\PycharmProjects\\email_sort\\email_data'

# Output file path for the combined JSON
output_file = 'C:\\Users\\casey\\PycharmProjects\\email_sort\\email_data\\combined.json'

# List to store the data from all JSON files
combined_data = []

# Iterate over each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        file_path = os.path.join(directory, filename)
        with open(file_path, 'r') as file:
            json_data = json.load(file)
            combined_data.append(json_data)

# Write the combined data to the output JSON file
with open(output_file, 'w') as output:
    json.dump(combined_data, output, indent=4)

print("JSON files combined successfully.")