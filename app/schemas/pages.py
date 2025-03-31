from pydantic import Field

from app.enums import BlockTypeEnum
from app.schemas.config_base_model import Schema


class PagesSchema(Schema):
    url: str = Field(max_length=32)
    content: list["BlocksSchema"]


class BlocksSchema(Schema):
    block_id: str = Field(alias="blockId", max_length=5)
    content: str
    type: BlockTypeEnum


class AddPageResponse(Schema):
    message: str = "Page successfully saved"


class DeletePageResponse(Schema):
    message: str = "Page successfully deleted"
