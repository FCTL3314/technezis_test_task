from sqlalchemy import Column, String, Integer

from db.core import Base


class Source(Base):
    __tablename__ = "sources"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    url = Column(String, nullable=False)
    xpath = Column(String, nullable=False)