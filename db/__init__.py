from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)
    
from db.models import (
    Base,
)

engine = create_engine("sqlite:///slack_app.db", echo=True)
Session = sessionmaker(engine)
Base.metadata.create_all(engine)