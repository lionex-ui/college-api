from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class HeadersModel(Base):
    __tablename__ = "headers"

    id: Mapped[int] = mapped_column(primary_key=True)
    header_name: Mapped[str] = mapped_column(String(100), unique=True)
    header_url: Mapped[str | None] = mapped_column(String(2048))

    tabs = relationship("HeaderTabsModel", back_populates="header", passive_deletes=True)
