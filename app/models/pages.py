from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class PagesModel(Base):
    __tablename__ = "pages"

    url: Mapped[str] = mapped_column(String(32), primary_key=True)

    blocks = relationship("BlocksModel", back_populates="page", passive_deletes=True)
