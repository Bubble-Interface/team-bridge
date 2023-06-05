
from sqlalchemy import (
    String,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
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

