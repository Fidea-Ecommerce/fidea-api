from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from config import database_fidea_url

engine = create_engine(database_fidea_url)
metadata = MetaData()
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


def init_db():
    metadata.create_all(bind=engine)
