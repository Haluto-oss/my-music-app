// src/pages/FamousProgressionsPage.tsx
import { useState, useEffect } from 'react';

// Javaのレコードに対応するTypeScriptの型を定義
interface Progression {
  name: string;
  description: string;
  key: string;
  chords: string[];
}

export function FamousProgressionsPage() {
  const [progressions, setProgressions] = useState<Progression[]>([]);
  const [error, setError] = useState('');

  // このページが読み込まれた時に、一度だけデータを取得する
  useEffect(() => {
    const fetchProgressions = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/progressions');
        if (!response.ok) {
          throw new Error('データの取得に失敗しました。');
        }
        const data = await response.json();
        setProgressions(data);
      } catch (err) {
        setError('サーバーからデータを取得できませんでした。');
      }
    };

    fetchProgressions();
  }, []); // 第2引数の配列が空なので、初回レンダリング時にのみ実行される

  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  return (
    <div>
      <h2>有名コード進行まとめ</h2>
      {progressions.map((prog, index) => (
        <div key={index} className="card">
          <h3>{prog.name}</h3>
          <p>{prog.description}</p>
          <p><strong>キー:</strong> {prog.key}</p>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {prog.chords.map((chord, i) => (
              <span key={i} className="note-tag">{chord}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}