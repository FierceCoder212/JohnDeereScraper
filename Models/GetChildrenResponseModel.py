from pydantic import BaseModel


class GetChildrenResponseModel(BaseModel):
    navItems: list['NavItem']


class NavItem(BaseModel):
    id: str
    name: str
    serializedPath: str
    level: str
    levelIndex: int
