from pydantic import Field, HttpUrl

from app.schemas.config_base_model import Schema


class HeadersSchema(Schema):
    header_name: str = Field(alias="headerName", max_length=100)
    header_url: HttpUrl | None = Field(alias="headerUrl", max_length=2048)
    tabs: list["HeaderTabsSchema"]


class HeaderTabsSchema(Schema):
    tab_name: str = Field(alias="tabName", max_length=100)
    tab_url: HttpUrl | None = Field(alias="tabUrl", max_length=2048)


class HeadersResponse(Schema):
    message: str = "Headers successfully saved"
