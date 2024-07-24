import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

URL_DATABASE = os.getenv("DATABASE_URL")

engine = create_engine(URL_DATABASE)
