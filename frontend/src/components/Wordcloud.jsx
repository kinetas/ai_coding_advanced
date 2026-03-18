import { useMemo } from 'react'
import './Wordcloud.css'

/**
 * 워드클라우드 컴포넌트 - 빈도에 따라 글자 크기가 다른 단어들 표시
 */
export default function Wordcloud({ words = [], className = '' }) {
  const { minCount, maxCount } = useMemo(() => {
    if (!words.length) return { minCount: 0, maxCount: 1 }
    const counts = words.map((w) => w.count)
    return {
      minCount: Math.min(...counts),
      maxCount: Math.max(...counts),
    }
  }, [words])

  const getFontSize = (count) => {
    if (maxCount === minCount) return 1
    const ratio = (count - minCount) / (maxCount - minCount)
    return 0.6 + ratio * 1.4 // 0.6 ~ 2.0 범위
  }

  return (
    <div className={`wordcloud ${className}`} role="img" aria-label="워드클라우드">
      {words.map(({ word, count }) => (
        <span
          key={word}
          className="wordcloud-word"
          style={{ '--scale': getFontSize(count) }}
          title={`${word}: ${count}회`}
        >
          {word}
        </span>
      ))}
    </div>
  )
}
