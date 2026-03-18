"""FastAPI 메인 애플리케이션"""
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db, init_db
from app.models import Category, SubCategory, WordcloudData
from app.wordcloud_service import generate_wordcloud_from_text, save_wordcloud_to_db

app = FastAPI(title="농산물 시세 분석 API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def root():
    return {"message": "농산물 시세 분석 API", "docs": "/docs"}


@app.get("/api/categories")
def list_categories(db: Session = Depends(get_db)):
    """카테고리 목록 조회"""
    categories = db.query(Category).all()
    return [{"id": c.id, "name": c.name} for c in categories]


@app.get("/api/sub-categories")
def list_sub_categories(
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db)
):
    """중분류 목록 조회"""
    q = db.query(SubCategory)
    if category_id:
        q = q.filter(SubCategory.category_id == category_id)
    items = q.all()
    return [{"id": s.id, "name": s.name, "category_id": s.category_id} for s in items]


@app.get("/api/wordcloud/{sub_category_id}")
def get_wordcloud(sub_category_id: int, db: Session = Depends(get_db)):
    """특정 분야의 워드클라우드 데이터 조회"""
    items = (
        db.query(WordcloudData)
        .filter(WordcloudData.sub_category_id == sub_category_id)
        .order_by(WordcloudData.count.desc())
        .all()
    )
    if not items:
        return {"sub_category_id": sub_category_id, "words": []}
    return {
        "sub_category_id": sub_category_id,
        "words": [{"word": w.word, "count": w.count} for w in items]
    }


@app.get("/api/wordcloud")
def get_all_wordclouds(db: Session = Depends(get_db)):
    """모든 분야의 워드클라우드 데이터 조회 (메인페이지용)"""
    sub_cats = db.query(SubCategory).all()
    result = []
    for sc in sub_cats:
        items = (
            db.query(WordcloudData)
            .filter(WordcloudData.sub_category_id == sc.id)
            .order_by(WordcloudData.count.desc())
            .limit(30)
            .all()
        )
        result.append({
            "sub_category_id": sc.id,
            "sub_category_name": sc.name,
            "words": [{"word": w.word, "count": w.count} for w in items]
        })
    return result


@app.post("/api/seed")
def seed_sample_data(db: Session = Depends(get_db)):
    """샘플 데이터 시드 (개발/데모용 - 작업 1,2 미완료 시 사용)"""
    from app.models import RawData

    # 카테고리 및 중분류 생성
    cat = db.query(Category).filter(Category.name == "농산물").first()
    if not cat:
        cat = Category(name="농산물")
        db.add(cat)
        db.commit()
        db.refresh(cat)

    sub_names = ["채소", "과일", "곡물"]
    sub_cats = []
    for name in sub_names:
        sub = db.query(SubCategory).filter(
            SubCategory.category_id == cat.id,
            SubCategory.name == name
        ).first()
        if not sub:
            sub = SubCategory(category_id=cat.id, name=name)
            db.add(sub)
            db.commit()
            db.refresh(sub)
        sub_cats.append(sub)

    # 샘플 원시 데이터 (워드클라우드용)
    sample_texts = [
        "배추 가격 상승 배추 김치 시장 수요 증가 배추 재배 농가",
        "사과 당도 품질 사과 수확 시즌 사과 가격 하락 사과 유통",
        "쌀 수확량 쌀 가격 쌀 품질 쌀 수입 쌀 자급률",
    ]
    for i, (sub, text) in enumerate(zip(sub_cats, sample_texts)):
        existing = db.query(RawData).filter(RawData.sub_category_id == sub.id).first()
        if not existing:
            db.add(RawData(sub_category_id=sub.id, content=text, source="seed"))
    db.commit()

    # 워드클라우드 생성
    from app.wordcloud_service import regenerate_wordcloud_for_category
    for sub in sub_cats:
        regenerate_wordcloud_for_category(db, sub.id)

    return {"message": "샘플 데이터 시드 완료"}
