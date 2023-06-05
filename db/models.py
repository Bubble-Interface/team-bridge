
from sqlalchemy import (
    String,
    create_engine,
    select
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    Session,
)



class Base(DeclarativeBase):
    pass


class Acronym(Base):
    __tablename__ = "acronyms"
    id: Mapped[int] = mapped_column(primary_key=True)
    acronym: Mapped[str] = mapped_column(String(30), unique=True)
    description: Mapped[str] = mapped_column(String(120))

    def __repr__(self) -> str:
        return f"{self.acronym}: {self.description}"

