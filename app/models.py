# models.py
from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RSVP(Base):
    __tablename__ = 'rsvps'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    attending = Column(Boolean, default=False)
    bringing_food = Column(Boolean, default=False)
    bringing_drink = Column(Boolean, default=False)
    message = Column(String, nullable=True)


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
