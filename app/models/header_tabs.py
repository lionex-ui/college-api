from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class HeaderTabsModel(Base):
    __tablename__ = "header_tabs"

    id: Mapped[int] = mapped_column(primary_key=True)
    header_id: Mapped[int] = mapped_column(
        ForeignKey("headers.id", ondelete="CASCADE"), index=True
    )
    tab_name: Mapped[str] = mapped_column(String(100))
    tab_url: Mapped[str | None] = mapped_column(String(2048))

    header = relationship("HeadersModel", back_populates="tabs")
