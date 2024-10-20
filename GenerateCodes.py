import json
import os
import concurrent.futures
from Helpers.JohnDeereScraperHelper import JohnDeereScraperHelper
from Helpers.SqLiteCodesHelper import SQLiteCodesHelper


# Function to process a range of codes
def process_code_range(start, end):
    sql_lite_helper = SQLiteCodesHelper('Codes.db')
    for i in range(start, end):
        code = f'PC{i}'
        if code not in codes:
            pc_number_matches = scraper_helper.get_search_results_exception_messages(pc_model=code).PC_NUMBER
            pc_number_matches = pc_number_matches.replace(' matches', '').strip()
            if pc_number_matches.isdigit() and int(pc_number_matches) >= 1:
                print(f'Found Code : {code} on {i} of {end}')
                codes.append(code)
                sql_lite_helper.insert_record(code)


# Function to divide the range based on the number of workers
def divide_range(start, end, num_workers):
    total_items = end - start
    chunk_size = total_items // num_workers
    ranges = []

    for i in range(num_workers):
        chunk_start = start + i * chunk_size
        # The last chunk should cover any remaining items (if there's a remainder)
        if i == num_workers - 1:
            chunk_end = end
        else:
            chunk_end = chunk_start + chunk_size
        ranges.append((chunk_start, chunk_end))
    return ranges


# Initialize helpers and load data
sql_lite_helper = SQLiteCodesHelper('Codes.db')
scraper_helper = JohnDeereScraperHelper()
with open(os.path.join(os.getcwd(), 'UniqueData.json')) as data_file:
    data = json.load(data_file)

# Prepare the codes list
codes = []
codes.extend(sql_lite_helper.get_records())
codes.extend(data.keys())

# Number of workers (threads) to use
num_workers = 10

# Divide the range of 1 to 20000 based on the number of workers
ranges = divide_range(1, 20000, num_workers)

# Create a thread pool to process the ranges
with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
    # Submit tasks for each range
    futures = [executor.submit(process_code_range, start, end) for start, end in ranges]

    # Wait for all tasks to complete and handle exceptions
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f"Error occurred: {e}")
