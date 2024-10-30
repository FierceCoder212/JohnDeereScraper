import concurrent.futures
import json
import math
import os

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Scrapers.JohnDeereScraper import JohnDeereScraper

with open(os.path.join(os.getcwd(), 'All Data.json')) as data_file:
    data = json.load(data_file)
google_drive_helper = GoogleDriverHelper('John Dheere Scraper')


def start_scraper(chunk: dict):
    scraper_helper = JohnDeereScraper(chunk, google_drive_helper)
    scraper_helper.start_scraping()


num_threads = 10
data_items = list(data.items())
chunk_size = math.ceil(len(data_items) / num_threads)
chunks = [dict(data_items[i:i + chunk_size]) for i in range(0, len(data_items), chunk_size)]
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(start_scraper, chunk) for chunk in chunks]
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as ex:
            print(f'Error in thread: {ex}')
