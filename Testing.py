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

    return json.loads(json_data)


# Example usage
csv_file_path = r"C:\Users\ABDULLAH\Documents\SGL.csv"  # Replace with your CSV file path

json_result = csv_first_column_to_json_list(r"C:\Users\ABDULLAH\Documents\SGL.csv")
json_result.extend(csv_first_column_to_json_list(r"C:\Users\ABDULLAH\Downloads\Sgl.csv"))
json_result = list(set(json_result))
print(len(json_result))
with open('UniqueData.json', 'r') as json_file:
    data = json.load(json_file)
print(len(data))
remaining_data = {}
for key, value in data.items():
    for item in value:
        if item not in json_result:
            if key not in remaining_data.keys():
                remaining_data[key] = []
            remaining_data[key].append(item)
with open('UniqueData.json', 'w') as json_file:
    json.dump(remaining_data, json_file, indent=4)
