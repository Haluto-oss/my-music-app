import React, { useState } from 'react';
import './App.css';

// TypeScriptで、APIから返ってくるデータの「型」を定義しておくと便利
interface DiatonicHarmony {
  degree: string;
  function: string;
  chords: string[];
}

function App() {
  // --- コード解析機能の状態 (変更なし) ---
  const [chordInput, setChordInput] = useState('Cmaj7');
  const [analysisResult, setAnalysisResult] = useState('');

  const handleAnalyzeChord = async () => {
    // ... (この関数は変更なし)
  };

  // --- スケール解析機能の状態 ---
  const [scaleInput, setScaleInput] = useState('C major');
  const [scalePitchesResult, setScalePitchesResult] = useState<string[]>([]); // 文字列の配列に
  const [diatonicHarmonyResult, setDiatonicHarmonyResult] = useState<DiatonicHarmony[]>([]); // 上で定義した型の配列に
  const [scaleError, setScaleError] = useState(''); // エラーメッセージ用

  const handleAnalyzeScale = async () => {
    // リセット
    setScaleError('');
    setScalePitchesResult([]);
    setDiatonicHarmonyResult([]);

    if (!scaleInput) {
      setScaleError('スケール名を入力してください。');
      return;
    }
    try {
      const encodedScaleName = encodeURIComponent(scaleInput);
      const response = await fetch(`http://localhost:8080/api/scales?name=${encodedScaleName}`);
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
    }
  };

  return (
    <>
      <h1>My Music App フロントエンド</h1>
      {/* コード解析のUI (変更なし) */}
      <div className="card">
        {/* ... */}
      </div>

      <hr />

      {/* ↓↓↓↓↓↓ スケール解析のUIをテーブル表示に変更 ↓↓↓↓↓↓ */}
      <div className="card">
        <h2>スケール・ダイアトニックコード解析</h2>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          <input
            type="text"
            value={scaleInput}
            onChange={(e) => setScaleInput(e.target.value)}
            placeholder="例: C major"
          />
          <button onClick={handleAnalyzeScale}>
            解析する
          </button>
        </div>

        {/* --- 結果表示 --- */}
        {scaleError && <p style={{ color: 'red' }}>{scaleError}</p>}
        
        {scalePitchesResult.length > 0 && (
          <p><b>スケール構成音: {scalePitchesResult.join(', ')}</b></p>
        )}
        
        {diatonicHarmonyResult.length > 0 && (
          <table>
            <thead>
              <tr>
                <th>機能</th>
                <th>ディグリー</th>
                <th>コード</th>
              </tr>
            </thead>
            <tbody>
              {diatonicHarmonyResult.map((item) => (
                <tr key={item.degree}>
                  <td>{item.function}</td>
                  <td>{item.degree}</td>
                  <td>{item.chords.join(' / ')}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </>
  );
}

export default App;