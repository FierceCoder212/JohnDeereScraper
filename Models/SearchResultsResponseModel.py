from pydantic import BaseModel


class SearchResultsResponseModel(BaseModel):
    searchResults: list['SearchResult']
    serviceExceptionMessages: 'ExceptionMessage'


class SearchResult(BaseModel):
    model: str
    equipmentName: str
    equipmentRefId: str


class ExceptionMessage(BaseModel):
    PC_NUMBER: str
