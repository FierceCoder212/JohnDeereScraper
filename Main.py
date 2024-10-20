from Scrapers.JohnDeereScraper import JohnDeereScraper

JohnDeereScraper().start_scraping()
# import json
# import os

# with open(os.path.join(os.getcwd(), 'UniqueData.json')) as data_file:
#     data = json.load(data_file)
# existing_codes = data.keys()
# new_codes = []
# for i in range(1, 20000):
#     code = f'PC{i}'
#     if code not in existing_codes:
#         new_codes.append(code)
# print(f'Existing Codes : {len(existing_codes)}')
# print(f'New Codes : {len(new_codes)}')
