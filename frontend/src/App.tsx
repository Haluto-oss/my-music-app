import { useState } from 'react';
import './App.css';

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

    // --- ↓↓↓↓↓↓ ここからがスケール解析用の新しいコードです ↓↓↓↓↓↓ ---

    const [scaleInput, setScaleInput] = useState('C major');
    const [scalePitchesResult, setScalePitchesResult] = useState('');
    const [diatonicChordsResult, setDiatonicChordsResult] = useState('');

    const handleAnalyzeScale = async () => {
        if (!scaleInput) {
            setScalePitchesResult('スケール名を入力してください。');
            setDiatonicChordsResult('');
            return;
        }
        try {
            const encodedScaleName = encodeURIComponent(scaleInput);
            const response = await fetch(`http://localhost:8080/api/scales?name=${encodedScaleName}`);
            const data = await response.json();

            if (!response.ok) {
                setScalePitchesResult(`エラー: ${data.detail || '不明なエラー'}`);
                setDiatonicChordsResult('');
            } else {
                setScalePitchesResult(`スケール構成音: ${data.scale_pitches.join(', ')}`);
                setDiatonicChordsResult(`ダイアトニックコード: ${data.diatonic_chords.join(' | ')}`);
            }
        } catch (error) {
            setScalePitchesResult('サーバーの呼び出しに失敗しました。');
            setDiatonicChordsResult('');
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

            {/* ↓↓↓↓↓↓ ここからがスケール解析用の新しいUIです ↓↓↓↓↓↓ */}
            <div className="card">
                <h2>スケール・ダイアトニックコード解析</h2>
                <input
                    type="text"
                    value={scaleInput}
                    onChange={(e) => setScaleInput(e.target.value)}
                    placeholder="例: C major, A harmonic minor"
                />
                <button onClick={handleAnalyzeScale}>
                    解析する
                </button>
                <p><b>{scalePitchesResult}</b></p>
                <p>{diatonicChordsResult}</p>
            </div>
        </>
    );
}

export default App;