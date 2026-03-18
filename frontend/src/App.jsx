import { useState, useEffect } from 'react'
import Wordcloud from './components/Wordcloud'
import './App.css'

const API_BASE = '/api'

export default function App() {
  const [wordclouds, setWordclouds] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedCategory, setSelectedCategory] = useState(null)

  useEffect(() => {
    fetchWordclouds()
  }, [])

  const fetchWordclouds = async () => {
    setLoading(true)
    setError(null)
    try {
      const res = await fetch(`${API_BASE}/wordcloud`)
      if (!res.ok) throw new Error('워드클라우드 데이터를 불러올 수 없습니다.')
      const data = await res.json()
      setWordclouds(data)
      if (data.length > 0 && !selectedCategory) {
        setSelectedCategory(data[0])
      }
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const handleSeed = async () => {
    try {
      const res = await fetch(`${API_BASE}/seed`, { method: 'POST' })
      if (!res.ok) throw new Error('시드 실패')
      await fetchWordclouds()
    } catch (err) {
      setError(err.message)
    }
  }

  const displayData = selectedCategory || (wordclouds.length > 0 ? wordclouds[0] : null)

  return (
    <div className="app">
      <header className="header">
        <h1>농산물 시세 분석</h1>
        <p className="tagline">
          분야별 핵심 키워드와 트렌드를 한눈에 확인하세요
        </p>
      </header>

      <main className="main">
        {error && (
          <div className="error-banner">
            <span>{error}</span>
            <button onClick={handleSeed}>샘플 데이터 로드</button>
          </div>
        )}

        {loading ? (
          <div className="loading">
            <div className="spinner" />
            <p>데이터를 불러오는 중...</p>
          </div>
        ) : wordclouds.length === 0 ? (
          <div className="empty-state">
            <p>표시할 워드클라우드 데이터가 없습니다.</p>
            <button className="seed-btn" onClick={handleSeed}>
              샘플 데이터 로드
            </button>
          </div>
        ) : (
          <>
            <nav className="category-tabs">
              {wordclouds.map((wc) => (
                <button
                  key={wc.sub_category_id}
                  className={`tab ${selectedCategory?.sub_category_id === wc.sub_category_id ? 'active' : ''}`}
                  onClick={() => setSelectedCategory(wc)}
                >
                  {wc.sub_category_name}
                </button>
              ))}
            </nav>

            {displayData && (
              <section className="wordcloud-section">
                <h2>{displayData.sub_category_name} 키워드</h2>
                <Wordcloud words={displayData.words} />
              </section>
            )}
          </>
        )}
      </main>

      <footer className="footer">
        <p>카테고리 → 분야 → 세부 선택으로 더 자세한 분석을 확인할 수 있습니다.</p>
      </footer>
    </div>
  )
}
