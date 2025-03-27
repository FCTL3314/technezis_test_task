from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from loader import settings

engine = create_engine(settings.db_engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
