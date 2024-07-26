from uuid import UUID, uuid4
from sqlalchemy import ForeignKey, String, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from sqlalchemy.types import Uuid



from ..db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id_recipe: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(200), nullable=True)
    creation_date: Mapped[date] = mapped_column(Date, nullable=False)
    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey('users.id_user'), nullable=False)
    user = relationship("User", back_populates="recipes")
    