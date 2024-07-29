from DBManager.base import Base
from sqlalchemy import Column, Integer, String, Boolean, BigInteger
from sqlalchemy.orm import Session

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True)
    username = Column(String)

class UserManager:
    GOOD = -1
    BAD = -2
    NOT_FOUND = -3
    def __init__(self, session:Session):
        self.session = session

    def add_user(self, user_id:int, username:str):
        try:
            user = User(user_id=user_id, username=username)
            self.session.add(user)
            self.session.commit()
            return user
        except:
            self.session.rollback()
            return None

    def is_user_exist(self, user_id:int):
        return self.session.query(User).filter_by(user_id=user_id).scalar() is not None

    def get_user(self, user_id:int):
        return self.session.query(User).filter_by(user_id=user_id).scalar()

    def get_all_users(self):
        return self.session.query(User).all()

    def delete_user(self, user_id:int):
        return self.session.query(User).filter_by(user_id=user_id).delete()
