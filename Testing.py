import csv
import json


def csv_first_column_to_json_list(csv_file_path):
    data_list = []

    # Open the CSV file
    with open(csv_file_path, mode='r') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)

        # Skip the header row (optional, if your CSV has headers)
        next(csv_reader, None)

        # Extract the first column (index 0) and append to the list
        for row in csv_reader:
            data_list.append(row[0])  # Access the first column by index

    # Convert the list to JSON format
    json_data = json.dumps(data_list, indent=4)

    return json_data


# Example usage
csv_file_path = r"C:\Users\ABDULLAH\Downloads\Sgl.csv"  # Replace with your CSV file path

json_result = csv_first_column_to_json_list(csv_file_path)
with open('NewUniqueData.json', 'r') as json_file:
    data = json.load(json_file)
remaining_data = {}
for key, value in data.items():
    for item in value:
        if item in json_result:
            if key not in remaining_data.keys():
                remaining_data[key] = []
            remaining_data[key].append(item)
print(json.dumps(remaining_data, indent=4))
print(len(remaining_data.keys()))
