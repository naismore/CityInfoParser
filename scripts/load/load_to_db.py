import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

load_dotenv()
engine = create_async_engine(url=os.getenv('SQLALCHEMY_URL'))
connection = engine.connect()
async_session = sessionmaker(engine, class_=AsyncSession)
