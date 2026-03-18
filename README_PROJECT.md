# 농산물 시세 분석 프로젝트

PRD 기반 농산물 시세·트렌드 분석 웹 애플리케이션입니다.

## 작업 3: 메인페이지 & 워드클라우드 (구현 완료)

### 실행 방법

1. **백엔드 실행**
   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **샘플 데이터 시드** (작업 1, 2 미완료 시)
   - 브라우저에서 `http://localhost:8000/api/seed` POST 요청
   - 또는 프론트엔드에서 "샘플 데이터 로드" 버튼 클릭

3. **프론트엔드 실행**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. `http://localhost:5173` 접속

### 구조

- `backend/` - FastAPI, SQLAlchemy, SQLite
- `frontend/` - React + Vite, 반응형 UI
- API: `/api/wordcloud`, `/api/seed`, `/api/categories`, `/api/sub-categories`
