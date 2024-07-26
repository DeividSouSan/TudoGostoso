import enum
from uuid import UUID, uuid4

from sqlalchemy import String, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..db.base import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"


class User(Base):
    __tablename__ = "users"

    id_user: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    role: Mapped[UserRole] = mapped_column(nullable=False, default=UserRole.USER)
    
    recipes: Mapped[list["Recipe"]] = relationship("Recipe", back_populates="user")
