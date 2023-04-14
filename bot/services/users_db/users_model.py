from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class Chat(Base):
    __tablename__ = "chats"

    id_chat = Column(Integer, primary_key=True)
    session = Column(Text)
