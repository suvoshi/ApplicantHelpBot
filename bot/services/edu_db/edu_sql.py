from sqlalchemy import create_engine, select as db_select
from sqlalchemy.orm import Session

from bot.services.edu_db.edu_model import *

EDU_DATABASE = "./data/edu.db"

edu_engine = create_engine(f"sqlite:///{EDU_DATABASE}")
edu_session = Session(edu_engine)


def select(table: str, condition: str, quantity="all"):
    """Returns list or model based on quantity param"""

    request = db_select(eval(table)).where(eval(condition))
    result = edu_session.scalars(request).all()

    if quantity == "one":
        return result[0]
    else:
        return result
