from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.env_variable import DATABASE_URL
from sqlalchemy.ext.automap import automap_base
import logging

try:
    engine = create_engine(DATABASE_URL)
    
    # 연결 테스트
    with engine.connect() as conn:
        pass
        
    Base = automap_base()
    Base.prepare(engine, reflect=True)
    
    # 필요한 테이블이 존재하는지 확인
    required_tables = ["user", "team", "team_member", "meeting_feedback"]
    missing_tables = [table for table in required_tables if table not in Base.classes.keys()]
    if missing_tables:
        raise ValueError(f"필수 테이블이 누락되었습니다: {', '.join(missing_tables)}")
    
    User = Base.classes.user
    Team = Base.classes.team
    TeamMember = Base.classes.team_member
    MeetingFeedback = Base.classes.meeting_feedback
except Exception as e:
    logging.error(f"데이터베이스 연결 또는 매핑 중 오류 발생: {str(e)}")
    raise