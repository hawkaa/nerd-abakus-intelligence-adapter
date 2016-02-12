from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

def get_session(connection_string):
    engine = create_engine(connection_string)
    Session.configure(bind = engine)
    return Session()

