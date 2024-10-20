import json
import os.path
import re

from Helpers.SqLiteHelper import SQLiteHelper
from Helpers.JohnDeereScraperHelper import JohnDeereScraperHelper
from Helpers.MSSqlHelper import MSSqlHelper
from Models.ApiRequestModel import ApiRequestModel
from Models.GetChildrenResponseModel import NavItem
from Models.GetPartsResponseModel import GetPartsResponseModel


class JohnDeereScraper:
    def __init__(self):
        self._scraper_helper = JohnDeereScraperHelper()
        self._data = self._get_scraper_data()
        self.scraper_name = 'John Deere Scraper'
        self.sqlHelper = MSSqlHelper()
        self.sqliteHelper = SQLiteHelper('diagrams')

    def start_scraping(self):
        total = len(self._data.items())
        for key, value in self._data.items():
            print(f'On code : {key} out of {total}')
            try:
                search_results = self._scraper_helper.get_search_results(pc_model=key)
            except Exception as ex:
                print(f'Exception at search results : {ex}')
                continue
            print(f'Total search results {len(search_results)}')
            for res in search_results:
                nav_items = self._scraper_helper.get_children_response(res.equipmentRefId)
                print(f'Nav Items scraped : {len(nav_items)}')
                self._scrape_parts(ref_id=res.equipmentRefId, nav_items=nav_items, sgl_codes=value)

    def _scrape_parts(self, ref_id: str, nav_items: list[NavItem], sgl_codes: list[str]):
        for item in nav_items:
            if item.level == 'PAGE':
                try:
                    parts_response = self._scraper_helper.get_parts_response(ref_id=ref_id, page_id=item.id)
                except Exception as ex:
                    print(f'Exception at parts response : {ex}')
                    continue
                if parts_response:
                    records = self._create_records(parts_response=parts_response, sgl_codes=sgl_codes)
                    print(f'Sending records to SQL: {len(records)}')
                    self.sqlHelper.insert_many_records(records=records)
                else:
                    print('Error : No parts found')
            else:
                try:
                    nav_items = self._scraper_helper.get_children_response(ref_id, level_index=item.levelIndex, serialized_path=item.serializedPath)
                    print(f'Nav Items scraped : {len(nav_items)}')
                    self._scrape_parts(ref_id=ref_id, nav_items=nav_items, sgl_codes=sgl_codes)
                except Exception as ex:
                    print(f'Exception in recursion at else part : {ex}')

    @staticmethod
    def _get_scraper_data():
        with open(os.path.join(os.getcwd(), 'UniqueData.json')) as data_file:
            return json.load(data_file)

    def _create_records(self, parts_response: GetPartsResponseModel, sgl_codes: list[str]) -> list[dict]:
        records = []
        section_diagram_url = f'data:image/PNG;base64,{parts_response.image}'
        self.sqliteHelper.create_connection()
        for code in sgl_codes:
            image_filename = self._sanitize_filename(f'{code}-{parts_response.name}.jpg')
            self.sqliteHelper.insert_record(section_diagram=image_filename, section_diagram_url=section_diagram_url)
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
        self.sqliteHelper.close_connection()
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
