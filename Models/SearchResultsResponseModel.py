from pydantic import BaseModel


class SearchResultsResponseModel(BaseModel):
    searchResults: list['SearchResult']


class SearchResult(BaseModel):
    model: str
    equipmentName: str
    equipmentRefId: str
