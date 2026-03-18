"""워드클라우드 생성 서비스"""
import re
from collections import Counter
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base, RawData, WordcloudData, SubCategory


def tokenize_korean(text: str) -> list[str]:
    """한국어 텍스트 토큰화 (간단한 형태소 분석)"""
    # 불용어
    stopwords = {
        "의", "가", "이", "은", "는", "을", "를", "에", "와", "과", "로", "으로",
        "에서", "까지", "하다", "있다", "되다", "그", "이", "저", "그것", "이것",
        "등", "및", "또는", "그리고", "하지만", "따라서"
    }
    # 2글자 이상 한글, 영문, 숫자만 추출
    tokens = re.findall(r'[가-힣]{2,}|[a-zA-Z]{2,}|\d+', text)
    return [t for t in tokens if t not in stopwords and len(t) >= 2]


def generate_wordcloud_from_text(text: str, top_n: int = 50) -> list[dict]:
    """텍스트에서 워드클라우드 데이터 생성"""
    tokens = tokenize_korean(text)
    counter = Counter(tokens)
    return [{"word": word, "count": count} for word, count in counter.most_common(top_n)]


def save_wordcloud_to_db(db: Session, sub_category_id: int, word_data: list[dict]) -> None:
    """워드클라우드 데이터를 DB에 저장 (기존 데이터 삭제 후 갱신)"""
    db.query(WordcloudData).filter(WordcloudData.sub_category_id == sub_category_id).delete()
    for item in word_data:
        wc = WordcloudData(
            sub_category_id=sub_category_id,
            word=item["word"],
            count=item["count"]
        )
        db.add(wc)
    db.commit()


def regenerate_wordcloud_for_category(db: Session, sub_category_id: int) -> list[dict]:
    """특정 분야의 원시 데이터에서 워드클라우드 재생성"""
    raw_records = db.query(RawData).filter(RawData.sub_category_id == sub_category_id).all()
    if not raw_records:
        return []

    all_text = " ".join(r.content for r in raw_records if r.content)
    word_data = generate_wordcloud_from_text(all_text)
    save_wordcloud_to_db(db, sub_category_id, word_data)
    return word_data
