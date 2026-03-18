"""데이터베이스 모델"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Category(Base):
    """카테고리 테이블 (예: 농산물)"""
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class SubCategory(Base):
    """중분류 테이블 (예: 채소, 과일)"""
    __tablename__ = "sub_categories"

    id = Column(Integer, primary_key=True, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class RawData(Base):
    """원시 데이터 테이블 (크롤링 결과 - ETL에서 채움)"""
    __tablename__ = "raw_data"

    id = Column(Integer, primary_key=True, index=True)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)


class WordcloudData(Base):
    """워드클라우드 데이터 테이블"""
    __tablename__ = "wordcloud_data"

    id = Column(Integer, primary_key=True, index=True)
    sub_category_id = Column(Integer, ForeignKey("sub_categories.id"), nullable=False)
    word = Column(String(100), nullable=False)
    count = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
