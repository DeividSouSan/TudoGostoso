from typing import Generator
from fastapi import Depends, HTTPException, status
from ..db.connection import engine
from sqlalchemy.orm import Session

def get_db() ->  Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

