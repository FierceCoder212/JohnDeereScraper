import json
import os.path
import re

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

    def start_scraping(self):
        for key, value in self._data.items():
            print(f'On code : {key}')
            search_results = self._scraper_helper.get_search_results(pc_model=key)
            parts_scraped: list[GetPartsResponseModel] = []
            print(f'Total search results {len(search_results)}')
            for res in search_results:
                nav_items = self._scraper_helper.get_children_response(res.equipmentRefId)
                print(f'Nav Items scraped : {len(nav_items)}')
                parts = self._get_parts(ref_id=res.equipmentRefId, nav_items=nav_items)
                parts_scraped.extend(parts)
            records = self._create_records(parts_responses=parts_scraped, sgl_codes=value)
            print(f'Sending records to SQL: {len(records)}')
            self.sqlHelper.insert_many_records(records=records)

    def _get_parts(self, ref_id: str, nav_items: list[NavItem]) -> list[GetPartsResponseModel]:
        curr_parts: list[GetPartsResponseModel] = []
        for item in nav_items:
            if item.level == 'PAGE':
                parts_response = self._scraper_helper.get_parts_response(ref_id=ref_id, page_id=item.id)
                if parts_response:
                    curr_parts.append(parts_response)
                    print(f'Parts scraped : {len(parts_response.partItems)}')
                else:
                    print('Error : No parts found')
            else:
                nav_items = self._scraper_helper.get_children_response(ref_id, level_index=item.levelIndex, serialized_path=item.serializedPath)
                print(f'Nav Items scraped : {len(nav_items)}')
                parts = self._get_parts(ref_id=ref_id, nav_items=nav_items)
                curr_parts.extend(parts)
        return curr_parts

    @staticmethod
    def _get_scraper_data():
        with open(os.path.join(os.getcwd(), 'UniqueData.json')) as data_file:
            return json.load(data_file)

    def _create_records(self, parts_responses: list[GetPartsResponseModel], sgl_codes: list[str]) -> list[dict]:
        records = []
        for code in sgl_codes:
            for item in parts_responses:
                image_filename = self._sanitize_filename(f'{code}-{item.name}.jpg')
                for part in item.partItems:
                    records.append(ApiRequestModel(
                        id=0,
                        sglUniqueModelCode=code,
                        section=item.name,
                        partNumber=part.partNumber,
                        description=part.partDescription,
                        itemNumber=part.sortCalloutLabel,
                        sectonDiagram=image_filename,
                        sectonDiagramUrl=f'data:image/PNG;base64,{item.image}',
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
