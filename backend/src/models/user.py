from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from database import Base
from uuid import UUID, uuid4

class User(Base):
    __tablename__ = "users"
    
    id_user: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    fullname: Mapped[str] = mapped_column(String(100))
    password_hash: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(100))
     
    # ! Marcar nullable = false onde precisar (no caso tudo)