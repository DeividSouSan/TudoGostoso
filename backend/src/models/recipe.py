from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from src.db.base import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id_recipe: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
