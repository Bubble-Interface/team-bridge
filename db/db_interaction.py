from sqlalchemy import (
    select,
)
from sqlalchemy.orm import (
    Session,
)

from db import Session
from db.models import Acronym


# TODO: try except for adding the acronym (return True is ok, else False)
def save_acronym(acronym: str, description: str):
    with Session.begin() as session:
        new_acronym = Acronym(
            acronym=acronym,
            description=description
        )
        session.add(new_acronym)
        return True

# TODO: try except for checking if acronym is present in db
def get_acronym_description(acronym: str) -> str:
    with Session.begin() as session:
        stmt = select(Acronym.description).where(Acronym.acronym == acronym)
        acronym_description = session.scalar(stmt)
        return acronym_description

def list_acronyms():
    with Session.begin() as session:
        stmt = select(Acronym.acronym)
        acronym_list = session.scalars(stmt)
        return acronym_list
    