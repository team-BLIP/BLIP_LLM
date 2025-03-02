from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.env_variable import DATABASE_URL
from sqlalchemy.ext.automap import automap_base

engine = create_engine(DATABASE_URL)

Base = automap_base()
Base.prepare(engine, reflect=True)

User = Base.classes.user
Team = Base.classes.team
TeamMember = Base.classes.team_member
MeetingFeedback = Base.classes.meeting_feedback

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


