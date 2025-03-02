from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import Depends
from src.infrastructure.database.connection import get_db, User

class BLIPRepository:
    def __init__(self, session : Session = Depends(get_db)):
        self.session = session
    
    def find_by_email(self, email : str) -> User | None:
        return self.session.scalar(select(User).where(User.email == email))
    
    def feedback_save(slef):
        pass #나중개발
    def summary_save(self):
        pass #나중개발