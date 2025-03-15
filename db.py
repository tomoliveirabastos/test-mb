from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker
from os import environ
import os.path
from dotenv import dotenv_values

def get_engine() -> Engine:
    if os.path.isfile(".env"):
        config = dotenv_values(".env")
        for k in config.keys():
            environ[k] = config[k]

    senha = environ.get("DB_PASSWORD")
    host = environ.get("DB_HOST")
    port = environ.get("DB_PORT")
    dbname = environ.get("DB_NAME")
    username = environ.get("DB_USERNAME")

    url = f"mysql+pymysql://{username}:{senha}@{host}:{port}/{dbname}"
    
    return create_engine(url)

def get_session():
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )

    return session()