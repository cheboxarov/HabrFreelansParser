from DBManager.user import User, UserManager
from DBManager.base import Base
from sqlalchemy import create_engine, Engine, MetaData, ForeignKey, select
from sqlalchemy.orm import Session

class DbManager:
    def __init__(self, dburl):
        self._engine = create_engine(dburl)
        self.session = Session(autoflush=False, bind=self._engine)
        Base.metadata.create_all(bind=self._engine)
        self.user = UserManager(self.session)
