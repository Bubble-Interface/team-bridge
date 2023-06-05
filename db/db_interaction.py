from sqlalchemy import (
    select,
)
from sqlalchemy.orm import (
    Session,
)

from db import Session
from db.models import Knowledge

# TODO: try except for checking if acronym is present in db
def get_knowledge(search_text: str) -> str:
    with Session() as session:
        stmt = select(
            Knowledge).where(
            Knowledge.title.ilike(f'%{search_text}%') | Knowledge.description.ilike(f'%{search_text}%')
        )
        result = session.scalars(stmt).all()
        return result

# TODO: try except for adding the acronym (return True is ok, else False)
def add_knowledge(title: str, description: str):
    with Session.begin() as session:
        new_knowledge = Knowledge(
            title=title,
            description=description
        )
        session.add(new_knowledge)
        return True


def list_knowledge():
    with Session() as session:
        stmt = select(Knowledge.title)
        knowledge_list = session.scalars(stmt)
        return knowledge_list