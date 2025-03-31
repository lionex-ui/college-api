from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql.sqltypes import Enum

from app.enums import BlockTypeEnum
from app.models.base import Base


class BlocksModel(Base):
    __tablename__ = "blocks"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_url: Mapped[int] = mapped_column(ForeignKey("pages.url", ondelete="CASCADE"), index=True)
    block_id: Mapped[str] = mapped_column(String(5))
    content: Mapped[str]
    type: Mapped[BlockTypeEnum] = mapped_column(Enum(BlockTypeEnum))

    page = relationship("PagesModel", back_populates="blocks")
