import time
from typing import Optional

import requests

from Models.GetChildrenResponseModel import GetChildrenResponseModel, NavItem
from Models.GetPartsResponseModel import GetPartsResponseModel
from Models.SearchResultsResponseModel import SearchResultsResponseModel, SearchResult


class JohnDeereScraperHelper:
    def __init__(self):
        self._search_url = 'https://partscatalog.deere.com/jdrc-services/v1/search/model'
        self._search_url_params = {
            'br': '1129',
            'locale': 'en-US',
            'sr': '0',
            'er': '75',
            'mfId': 'null'
        }
        self._get_children_url = 'https://partscatalog.deere.com/jdrc-services/v1/navigation/p/getChildren'
        self._get_children_body = {
            "fr": {
                "currentPin": "",
                "businessRegion": 1129,
                "filtersEnabled": True,
                "filteringLevel": None,
                "encodedFilters": None,
                "encodedFiltersHash": None
            },
            "br": "1129",
            "locale": "en-US",
            "vm": "p",
        }
        self._get_parts_url = 'https://partscatalog.deere.com/jdrc-services/v1/sidebyside/sidebysidePage'
        self._get_parts_body = {
            "fr": {
                "currentPin": "",
                "businessRegion": 1129,
                "filtersEnabled": True,
                "filteringLevel": None,
                "encodedFilters": None,
                "encodedFiltersHash": None
            },
            "brID": "1129",
            "locale": "en-US",
            "fromSearch": False,
            "includeRelatedPictorials": True
        }
        self._headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Captcha-Token": "03AFcWeA6bmBsgHKmjjhoh_c9lIxPk4SecbP5N7jY93ivsKiGc_sN02SwmbH06a6mNHA9ZOWs7vvvR6rNHLGgjS9Y76yp4Z4CTFOyuolAOpSvePYYWU79eHcIjAOar1dySmFOcCifrfkXgWJmY2VWJSt5mfxlHOj2QxBjjw40R3IBut_CarF_PknA9DNLcuFkAFhaWxJS1uZ-evJW0gwPbZfzgjaeS5UCB7R24VL8DBVZ-BHgxUAcmBhbFsFLunZ-dNHtud70pl-XGWKG--ENr7r53RYf_iI3rqTHxlknUpEwAxpbMuPLGU6vRVqPmBNep8OFO2Kp1reyU8831L3lxiAc3YskEIwjIWWal7m52YlOpOK0ykjmNSeS_Qj-9ueQaNxu76mJ2iO-IKAS4_iDP-aOAxtzLg40-xkIrfUKNBFHMjdNWicW7uAlsDW75k_7FJXQ2yJma6ZJzODZ0UN1yxPkDoOXRNJ0lZRa10_Af63pwJ45Y5RsCptZvCTkm6u6UuTsyFzmNu0jqTs4Tz_4Jev_l9H-9V4M4iS05pvRGK434HIJMDSjevFXWVMDwbQsGcBx_LgFczQzOOQ8TZmyACz_g2lXiT5-ocG8ZqGzpaDed8AsySSY4FjlC2ev8OBcMsfesfHSXVaUuHwNGr0ula_KoXyqM6CdHZLF0dcvNW09BkOSzDqBH3FC7ZV37Xolhd5KsT8hECDyORxypzjue2R855V6F8jnc2NC8eAwp-1dnYCk5sgrf5OR9Hs26wKZu_V-t2Coebv4pABa8i3Zi64lt_TqPWjYEynM8aiDlFd0jMdhFuZEXhT5S7W8ekfEzLWxO0mYd2p2PMMe9j4dbc2u5sc4L_Q2xMgGVY3BPMKzQ2ZmfT14lcibG5CCBfvi1u7scR2mDTOj0JzSZSI8z_CtIgOGghUGEMcvLiBHZA4e3Q9pntt91XbpUziGO5YR_xgAb8u5jX67045xu9TeCC2d_6rKmkUdI5-yRrXgEuGg_vhLkUXGKna2l02vobHJGSdK-U34rS6FhPPRZ0SzjI946BGek2k0ARQk4FTMqcM3jJ8yD9Pr3NFu2m-JLoJR9V1alRfcj7I0IZ2OXQD8exIndHTU2piU0ZlqgZobCtC6uKZLusjHeCF_0Fz7pN0F9eYU_T3B_jJvJs35onZWpcpdFc1cI0Ed44S7JQBCVvlCECB1nofHCQbc2fo7SJZG7aHgTua-ek-aBbv3wBZCaLvJDYAfPCjKHLTypvwr5zYOtOl_RB_k5cRZUAHQrHb1_RATKbMI8oiPjWRaeItWKHFT4CJDoAhsuSE_8ny6kmLiWTk7LQK_Fbd3Dxz-6wmCZJoxlCKsqKhqhJ5m-rhREtlaCT_OFR4kBLOM6_cOED3i8EQPABwltztgoDvKQRqA-Pe43mUSI8KUGUIh243Snw4ekYWXmLJ5KctF9fidBvqAl1meK5q8YhOmQPuKZoVITeiBqbYq4Ncnbg_USlND5eFEQlzA3CHr0ZyRTownmVrP7kGj_9pBllJDFgkOAM7ZGifQaLekJK8xiW1DYcMe_s3Fr1xkCVl4SbCCSmjlQ1qSxIQp62YLtag0XpS-HnDPn8kiD0BrF5oIFH8TYcOWK8JWyixBD3lUjVhr60tv1cFJywT8sv9GJQNu3Vdf_-Pz_V0Igwgn8UGFCsc1puDLic2jpPGRX08ypWQHpID6_8c_pRC6yrbf4vDoQEs_xnxquAsP5X4PntHUSNN23DTj05tECYJZnYckjVG9zxAlSOvuwPl-ys4zUZuPgB7JCFOL_kHnpeNQ4wQYfTW2jXt7KT7UVXfiveMX9LFIMiD4o_5YFxfgrzPbqZBqCCFImX7fJlEVfsmoYpcjCX3WffMvwp8hFfOqJIrv4m7wdHkeAFEe8v-jGlF3QN1a79DeLBkH-9UpFreUzi7Rg",
            "Captcha-Version": "Enterprise",
            "Connection": "keep-alive",
            "Cookie": "OptanonConsent=isGpcEnabled=0&datestamp=Sat+Oct+19+2024+01%3A10%3A16+GMT%2B0500+(Pakistan+Standard+Time)&version=202409.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=02848c1b-8b78-4938-98ad-68650dccf500&interactionCount=16&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1&intType=undefined&geolocation=PK%3BPB&AwaitingReconsent=false; OptanonAlertBoxClosed=2024-10-18T20:10:16.939Z; AWSALB=qP2k+o+IhCBaKHYKcsoTKcfskJc/Dcz+R4kRK7Y9BRpGM5UPJ+WVfAM+J32CCqOubfAZTqeu0X33uwtcYqfLRUz4umTSMv0uKSQ8eLgtZPhixjfMvRknaJ2NQupQ; AWSALBCORS=qP2k+o+IhCBaKHYKcsoTKcfskJc/Dcz+R4kRK7Y9BRpGM5UPJ+WVfAM+J32CCqOubfAZTqeu0X33uwtcYqfLRUz4umTSMv0uKSQ8eLgtZPhixjfMvRknaJ2NQupQ",
            "Referer": "https://partscatalog.deere.com/jdrc/search/type/model/term/PC9077",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
            "product-line": "JDRC",
            "sec-ch-ua": '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"'
        }

    def get_search_results(self, pc_model: str, wait_count: int = 25) -> list[SearchResult]:
        self._search_url_params['q'] = pc_model
        response = requests.get(self._search_url, headers=self._headers, params=self._search_url_params)
        if response.status_code == 200:
            return SearchResultsResponseModel(**response.json()).searchResults
        else:
            print(f'Error search response : {response.status_code}, {response.text}')
            print(f'Waiting for {wait_count}sec.')
            time.sleep(wait_count)
            return self.get_search_results(pc_model=pc_model, wait_count=wait_count + 1)

    def get_children_response(self, ref_id: str, level_index: int = 1, serialized_path: str = '', wait_count: int = 25) -> list[NavItem]:
        self._get_children_body['eq'] = ref_id
        self._get_children_body['ln'] = level_index
        self._get_children_body['sp'] = serialized_path
        self._get_children_body['fr']['equipmentRefId'] = ref_id
        response = requests.post(self._get_children_url, headers=self._headers, json=self._get_children_body)
        if response.status_code == 200:
            return GetChildrenResponseModel(**response.json()).navItems
        else:
            print(f'Error children response : {response.status_code}, {response.text}')
            print(f'Waiting for {wait_count}sec.')
            time.sleep(wait_count)
            return self.get_children_response(ref_id=ref_id, level_index=level_index, serialized_path=serialized_path, wait_count=wait_count + 1)

    def get_parts_response(self, ref_id: str, page_id: str, wait_count: int = 25) -> Optional[GetPartsResponseModel]:
        self._get_parts_body['eqID'] = ref_id
        self._get_parts_body['fr']['equipmentRefId'] = ref_id
        self._get_parts_body['pgID'] = page_id
        response = requests.post(self._get_parts_url, headers=self._headers, json=self._get_parts_body)
        if response.status_code == 200:
            return GetPartsResponseModel(**response.json())
        else:
            print(f'Error parts response : {response.status_code}, {response.text}')
            print(f'Waiting for {wait_count}sec.')
            time.sleep(wait_count)
            return self.get_parts_response(ref_id=ref_id, page_id=page_id, wait_count=wait_count + 1)
