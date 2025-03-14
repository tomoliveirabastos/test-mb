from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker

def get_engine() -> Engine:
    return create_engine("mysql+pymysql://root:123Mudar@localhost:3306/mb_test")

def get_session():
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
    )

    return session()