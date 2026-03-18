"""데이터베이스 연결 및 초기화"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from pathlib import Path

_db_path = Path(__file__).resolve().parent.parent / "data.db"
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"sqlite:///{_db_path}"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """테이블 생성"""
    from app.models import Base
    Base.metadata.create_all(bind=engine)
