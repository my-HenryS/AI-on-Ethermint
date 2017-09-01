from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os
import sys
sys.path.append(os.path.dirname(__file__)+'/'+'..')
from config import Config


class SqlalchemyEngine:
    engine = create_engine(Config.conn_url, echo=True, client_encoding='utf-8')

    def getSession(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()
        return session
