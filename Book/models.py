from sqlalchemy import Column, String, Integer
from .database import Base


# ###### Describe your Table look here
class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    synopsis = Column(String, index=True)
    published = Column(Integer, index=True)
