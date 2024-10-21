import json
import math
import os
import concurrent.futures
from Helpers.JohnDeereScraperHelper import JohnDeereScraperHelper
from Helpers.SqLiteCodesHelper import SQLiteCodesHelper


# Function to process a range of codes
def process_code_range(chunk):
    sql_lite_helper = SQLiteCodesHelper('Codes.db')
    for item in chunk:
        search_results = scraper_helper.get_search_results_exception_messages(pc_model=item)
        pc_number_matches = search_results.serviceExceptionMessages.PC_NUMBER
        pc_number_matches = pc_number_matches.replace(' matches', '').strip()
        if pc_number_matches.isdigit() and int(pc_number_matches) >= 1:
            sql_lite_helper.insert_record(item, search_results.searchResults[0].model)
        else:
            print(f'Code not found for item : {item}')


# Initialize helpers and load data
scraper_helper = JohnDeereScraperHelper()
with open(os.path.join(os.getcwd(), 'Codes.json')) as data_file:
    codes = json.load(data_file)

# Number of workers (threads) to use
num_workers = 20
chunk_size = math.ceil(len(codes) / num_workers)
chunks = [codes[i:i + chunk_size] for i in range(0, len(codes), chunk_size)]

# Create a thread pool to process the ranges
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Submit tasks for each range
    futures = [executor.submit(process_code_range, chunk) for chunk in chunks]

    # Wait for all tasks to complete and handle exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred: {e}")
