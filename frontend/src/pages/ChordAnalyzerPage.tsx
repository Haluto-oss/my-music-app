import { playSound } from '../services/soundService';import { useState } from 'react';

export function ChordAnalyzerPage() {
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

  return (
    <div className="card">
      <h2>コード構成音 解析（ボタン表示テスト中）</h2>
      <input
        type="text"
        value={chordInput}
        onChange={(e) => setChordInput(e.target.value)}
        placeholder="例: Cmaj7, Fm7b5"
      />
      <button onClick={handleAnalyzeChord}>解析する</button>
      <p>解析結果: {analysisResult}</p>
      {/* ↓↓↓↓↓↓ このテスト用ボタンを追加します ↓↓↓↓↓↓ */}
      <hr style={{ margin: '20px 0' }} />
      <button onClick={() => playSound('C4')}>
        テストサウンドを鳴らす (C4)
      </button>
      {/* ↑↑↑↑↑↑ このテスト用ボタンを追加します ↑↑↑↑↑↑ */}

    </div>
  );
}