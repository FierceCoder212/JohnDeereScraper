import json
import threading

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriverHelper:
    folder_lock = threading.Lock()

    def __init__(self, folder_name: str, folder_suffix=0):
        self.drive = self._get_drive()
        self.folder_suffix = folder_suffix
        self.folder_name = folder_name
        self.folder_id = self._setup_folder(folder_name=folder_name)

    def upload_file_from_path(self, file_path: str, file_name: str):
        while True:
            file_metadata = {'title': file_name, 'parents': [{'id': self.folder_id}]}
            try:
                file = self.drive.CreateFile(file_metadata)
                file.SetContentFile(file_path)
                file.Upload()
                break
            except Exception as e:
                if "The limit for this folder's number of children" in str(e):
                    with GoogleDriverHelper.folder_lock:
                        if file_metadata['parents'][0]['id'] == self.folder_id:
                            self._create_new_folder()

    def _create_new_folder(self):
        self.folder_suffix += 1
        new_folder_name = f"{self.folder_name}_{self.folder_suffix}"
        self.folder_id = self._setup_folder(new_folder_name)

    def upload_file_from_content(self, file_bytes: bytes, file_name: str):
        with open(file_name, 'wb') as img_file:
            img_file.write(file_bytes)
        self.upload_file_from_path(file_path=file_name, file_name=file_name)

    def get_files_from_folder(self) -> list[str]:
        file_list = self.drive.ListFile(
            {'q': f"'{self.folder_id}' in parents and trashed=false"}
        ).GetList()
        return [file['title'] for file in file_list]

    def get_files_from_folder_chunk(self) -> list[str]:
        filenames = []
        query = f"'{self.folder_id}' in parents and trashed=false"
        page_token = None
        while True:
            param = {
                'q': query,
                'maxResults': 1000,  # Limit results to chunks of 1000
                'fields': 'nextPageToken, items(title)'
            }
            if page_token:
                param['pageToken'] = page_token

            # Fetch the file list
            file_list = self.drive.ListFile(param).GetList()
            filenames.extend(file['title'] for file in file_list)

            # Check if there's a next page
            if hasattr(file_list, 'nextPageToken') and file_list['nextPageToken']:
                page_token = file_list['nextPageToken']
            else:
                break  # No more pages

        return filenames

    def save_prev_drive_files_on_folder(self):
        files = self.get_files_from_folder()
        with open("Uploaded Files.json", "w") as all_uploaded_images:
            all_uploaded_images.write(json.dumps(files, indent=4))

    def _setup_folder(self, folder_name: str):
        query = f"title='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        file_list = self.drive.ListFile({'q': query}).GetList()
        if not file_list:
            folder_metadata = {
                'title': folder_name,
                'mimeType': 'application/vnd.google-apps.folder',
            }
            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()
            folder_id = folder['id']
        else:
            folder_id = file_list[0]['id']
        return folder_id

    @staticmethod
    def _get_drive() -> GoogleDrive:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        return GoogleDrive(gauth)
