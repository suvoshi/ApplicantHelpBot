from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class City(Base):
    __tablename__ = "cities"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    info = Column(Text)
    subject = Column(Text)
    coords = Column(Text)
    population = Column(Integer)
    keywords = Column(Text)


class HI(Base):
    __tablename__ = "HIs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_city = Column(Integer)
    name = Column(Text)
    info = Column(Text)
    url = Column(Text)
    keywords = Column(Text)


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_HI = Column(Integer)
    id_subtype = Column(Integer)
    code = Column(Text)
    info = Column(Text)
    profiles = Column(Text)
    objs = Column(Text)
    form = Column(Integer)
    budget_places = Column(Integer)
    cost_ed = Column(Integer)
    period = Column(Integer)
    last_update = Column(Integer)
    keywords = Column(Text)


class ProgramCode(Base):
    __tablename__ = "programs_codes"

    code = Column(Text, primary_key=True)
    name = Column(Text)


class Obj(Base):
    __tablename__ = "objs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)


class Subtype(Base):
    __tablename__ = "subtypes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_type = Column(Integer)
    name = Column(Text)
