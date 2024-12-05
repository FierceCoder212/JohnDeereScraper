import json

from googleapiclient.errors import HttpError

from Helpers.GoogleDriveHelper import GoogleDriverHelper

google_drive_helper = GoogleDriverHelper('Login')
# files = google_drive_helper.save_prev_drive_files_on_folder()

# with open('Unique Data.json' , 'r') as json_file:
#     print(len(list(json.load(json_file).keys())))
