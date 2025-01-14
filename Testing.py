import json
import os

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Scrapers.JohnDeereScraper import JohnDeereScraper

# from Helpers.GoogleDriveHelper import GoogleDriverHelper
#
# google_drive_helper = GoogleDriverHelper('Login')
with open(os.path.join(os.getcwd(), 'Unique Data.json')) as data_file:
    data = json.load(data_file)
# google_drive_helper = GoogleDriverHelper('John Dheere Scraper')
# scraper_helper = JohnDeereScraper(data, google_drive_helper)
# scraper_helper.start_scraping()
