import { useState } from 'react';
import './ScaleAnalyzerPage.css';

interface DiatonicHarmony {
  degree: string;
  function: string;
  chords: string[];
}

export function ScaleAnalyzerPage() {
  const [scaleInput, setScaleInput] = useState('C major');
  const [scalePitchesResult, setScalePitchesResult] = useState<string[]>([]);
  const [diatonicHarmonyResult, setDiatonicHarmonyResult] = useState<DiatonicHarmony[]>([]);
  const [scaleError, setScaleError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleAnalyzeScale = async () => {
    if (isLoading) return;
    setIsLoading(true);
    setScaleError('');
    setScalePitchesResult([]);
    setDiatonicHarmonyResult([]);
    if (!scaleInput) {
      setScaleError('スケール名を入力してください。');
      setIsLoading(false);
      return;
    }
    try {
      const encodedScaleName = encodeURIComponent(scaleInput);
      const response = await fetch(`http://127.0.0.1:8000/ai/analyze/scale?name=${encodedScaleName}`);
      const data = await response.json();
      if (!response.ok) {
        setScaleError(`エラー: ${data.detail || '不明なエラー'}`);
      } else {
        setScalePitchesResult(data.scale_pitches);
        setDiatonicHarmonyResult(data.diatonic_harmony);
      }
    } catch (error) {
      setScaleError('サーバーの呼び出しに失敗しました。');
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter') {
      handleAnalyzeScale();
    }
  };

  return (
    <div className="analyzer-card">
      <h2>スケール・ダイアトニックコード解析</h2>
      <div className="input-area">
        <input
          type="text"
          value={scaleInput}
          onChange={(e) => setScaleInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="例: D dorian, F harmonic minor"
          disabled={isLoading}
        />
        <button onClick={handleAnalyzeScale} disabled={isLoading}>
          {isLoading ? '解析中...' : '解析する'}
        </button>
      </div>

      <div className="results-area">
        {scaleError && <p className="error-message">{scaleError}</p>}
        
        {scalePitchesResult.length > 0 && (
          <p className="scale-pitches">
            <b>スケール構成音: {scalePitchesResult.join(', ')}</b>
          </p>
        )}
        
        {/* 結果が1件以上ある場合のみ表示 */}
        {diatonicHarmonyResult.length > 0 && (
          <div className="results-list">
            <div className="results-header">
              <div className="results-col function">機能</div>
              <div className="results-col degree">ディグリー</div>
              <div className="results-col chord">コード</div>
            </div>
            {diatonicHarmonyResult.map((item) => (
              <div className="results-row" key={item.degree}>
                <div className="results-col function">{item.function}</div>
                <div className="results-col degree">
                  <strong>{item.degree}</strong>
                </div>
                <div className="results-col chord">{item.chords.join(' / ')}</div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}