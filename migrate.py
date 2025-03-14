from db import get_engine
from sqlalchemy_utils import database_exists, create_database
from models.logs import Logs

engine = get_engine()

if not database_exists(engine.url):
    create_database(engine.url)

Logs.metadata.create_all(engine)