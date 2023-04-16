from sqlalchemy import create_engine
from sqlalchemy import select as db_select
from sqlalchemy import insert as db_insert
from sqlalchemy import update as db_update
from sqlalchemy.orm import Session

from bot.services.users_db.users_model import Chat

USERS_DATABASE = "./data/users.db"

users_engine = create_engine(f"sqlite:///{USERS_DATABASE}")
users_session = Session(users_engine)


def select(id_chat: int):
    """Returns Chat object with given id_chat"""
    request = db_select(Chat).where(Chat.id_chat == id_chat)
    result = users_session.scalars(request).all()

    if len(result) > 0:
        return result[0]
    else:
        return []


def insert(id_chat: int, session: str):
    """Insert id_chat, session into Chat table"""
    request = db_insert(Chat).values(id_chat=id_chat, session=session)
    users_session.execute(request)
    users_session.commit()


def update(id_chat: int, session: str):
    """Update session Chat object with given id_chat"""
    request = db_update(Chat).where(Chat.id_chat == id_chat).values(session=session)
    users_session.execute(request)
    users_session.commit()
