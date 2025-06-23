import React, { useState } from 'react';
import './App.css';

// TypeScriptで、APIから返ってくるデータの「型」を定義
interface DiatonicHarmony {
  degree: string;
  function: string;
  chords: string[];
}

function App() {
  // --- コード解析機能の状態 ---
  const [chordInput, setChordInput] = useState('Cmaj7');
  const [analysisResult, setAnalysisResult] = useState('');

  const handleAnalyzeChord = async () => {
    if (!chordInput) {
        setAnalysisResult('コードネームを入力してください。');
        return;
    }
    try {
        const encodedChordName = encodeURIComponent(chordInput);
        const response = await fetch(`http://localhost:8080/api/chords?name=${encodedChordName}`);
        const data = await response.json();
        if (!response.ok) {
            setAnalysisResult(`エラー: ${data.detail || '不明なエラー'}`);
        } else {
            setAnalysisResult(`構成音: ${data.notes.join(', ')}`);
        }
    } catch (error) {
        setAnalysisResult('サーバーの呼び出しに失敗しました。');
        console.error(error);
    }
  };

  // --- スケール解析機能の状態 ---
  const [scaleInput, setScaleInput] = useState('C major');
  const [scalePitchesResult, setScalePitchesResult] = useState<string[]>([]);
  const [diatonicHarmonyResult, setDiatonicHarmonyResult] = useState<DiatonicHarmony[]>([]);
  const [scaleError, setScaleError] = useState('');

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
      
      // 1. まずは生のテキストとして受け取る
      const jsonText = await response.text();
      console.log("★★★★★ Received RAW STRING from server:", jsonText);
      
      // 2. 受け取ったテキストをJSONオブジェクトとして手動で解析
      const data = JSON.parse(jsonText);
      console.log("★★★★★ Parsed data object:", data);


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
      <div className="card">
        <h2>コード構成音 解析</h2>
        <input
          type="text"
          value={chordInput}
          onChange={(e) => setChordInput(e.target.value)}
          placeholder="例: Cmaj7, Fm7b5"
        />
        <button onClick={handleAnalyzeChord}>
          解析する
        </button>
        <p>解析結果: {analysisResult}</p>
      </div>

      <hr />

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
        
        {/* ↓↓↓↓↓↓ scalePitchesResult && を追加 ↓↓↓↓↓↓ */}
        {(scalePitchesResult && scalePitchesResult.length > 0) && (
          <p><b>スケール構成音: {scalePitchesResult.join(', ')}</b></p>
        )}
        
        {/* ↓↓↓↓↓↓ diatonicHarmonyResult && を追加 ↓↓↓↓↓↓ */}
        {(diatonicHarmonyResult && diatonicHarmonyResult.length > 0) && (
          <table>
            {/* ... テーブルの中身は変更なし ... */}
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