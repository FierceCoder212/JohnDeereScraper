import base64
import json
import logging
import os
import re

from Helpers.GoogleDriveHelper import GoogleDriverHelper
from Helpers.JohnDeereScraperHelper import JohnDeereScraperHelper
from Helpers.MSSqlHelper import MSSqlHelper
from Models.ApiRequestModel import ApiRequestModel
from Models.GetChildrenResponseModel import NavItem
from Models.GetPartsResponseModel import GetPartsResponseModel

logging.basicConfig(
    filename='john_deere_scraper.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JohnDeereScraper:
    def __init__(self, data_chunk: dict, google_drive_helper: GoogleDriverHelper):
        self._scraper_helper = JohnDeereScraperHelper()
        self._data = data_chunk
        self.scraper_name = 'John Deere Scraper'
        self.sqlHelper = MSSqlHelper()
        self.google_drive_helper = google_drive_helper

    def start_scraping(self):
        total = len(self._data)
        index = 0
        for key, value in self._data.items():
            print(f'On code : {index + 1} out of {total}')
            try:
                search_results = self._scraper_helper.get_search_results(pc_model=key)
            except Exception as ex:
                print(f'Exception at search results : {ex}')
                continue
            print(f'Total search results {len(search_results)}')
            for res in search_results:
                nav_items = self._scraper_helper.get_children_response(res.equipmentRefId)
                # print(f'Nav Items scraped : {len(nav_items)}')
                self._scrape_parts(ref_id=res.equipmentRefId, nav_items=nav_items, sgl_codes=value)
            index += 1

    def _scrape_parts(self, ref_id: str, nav_items: list[NavItem], sgl_codes: list[str]):
        for item in nav_items:
            if item.level == 'PAGE':
                try:
                    parts_response = self._scraper_helper.get_parts_response(ref_id=ref_id, page_id=item.id)
                except Exception as ex:
                    print(f'Exception at parts response : {ex}')
                    logger.error(f'Parts Error at sgl : {ex}')
                    logger.error(json.dumps(sgl_codes, indent=4))
                    continue
                if parts_response:
                    records = self._create_records(parts_response=parts_response, sgl_codes=sgl_codes)
                    # print(f'Sending records to SQL: {len(records)}')
                    self.sqlHelper.insert_many_records(records=records)
                else:
                    print('Error : No parts found')
            else:
                try:
                    nav_items = self._scraper_helper.get_children_response(ref_id, level_index=item.levelIndex, serialized_path=item.serializedPath)
                    # print(f'Nav Items scraped : {len(nav_items)}')
                    self._scrape_parts(ref_id=ref_id, nav_items=nav_items, sgl_codes=sgl_codes)
                except Exception as ex:
                    print(f'Exception in recursion at else part : {ex}')

    def _create_records(self, parts_response: GetPartsResponseModel, sgl_codes: list[str]) -> list[dict]:
        records = []
        section_diagram = base64.b64decode(parts_response.image)
        for code in sgl_codes:
            image_filename = self._sanitize_filename(f'{code}-{parts_response.name}.jpg')
            # print(f'Uploading {image_filename} to google drive')
            self.google_drive_helper.upload_file_from_content(file_bytes=section_diagram, file_name=image_filename)
            if os.path.exists(image_filename):
                os.remove(image_filename)
            for part in parts_response.partItems:
                records.append(ApiRequestModel(
                    id=0,
                    sglUniqueModelCode=code,
                    section=parts_response.name,
                    partNumber=part.partNumber if part.partNumber else '',
                    description=part.partDescription,
                    itemNumber=part.sortCalloutLabel,
                    sectonDiagram=image_filename,
                    sectonDiagramUrl='',
                    scraperName=self.scraper_name).model_dump())
        return records

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        """
        Convert invalid filenames to valid filenames by replacing or removing invalid characters.
        """
        invalid_chars = r'[<>:"/\\|?*\']'
        sanitized_filename = re.sub(invalid_chars, "_", filename)
        sanitized_filename = sanitized_filename.strip()
        sanitized_filename = sanitized_filename[:255]
        return sanitized_filename
