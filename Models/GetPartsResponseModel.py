from typing import Optional

from pydantic import BaseModel


class GetPartsResponseModel(BaseModel):
    name: str
    image: str
    partItems: Optional[list['PartItem']]


class PartItem(BaseModel):
    partNumber: Optional[str]
    partDescription: str
    sortCalloutLabel: str
