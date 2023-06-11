import os
from sqlalchemy import (
    create_engine,
)
from sqlalchemy.orm import (
    sessionmaker,
)
    
from db.models import (
    Base,
)

db_user = os.environ.get("DB_USER", 'team_bridge_user')
db_pass = os.environ.get("DB_PASSWORD", 'password')
db_host = os.environ.get("DB_HOST", 'team_bridge')
db_port = os.environ.get("DB_PORT", '5432')
db_name = os.environ.get("DB_NAME", 'team_bridge')

db_string = f'postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}'
engine = create_engine(db_string, echo=True)

Session = sessionmaker(engine)
Base.metadata.create_all(engine)