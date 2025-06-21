import { useState } from 'react';
import './App.css'; // スタイルはデフォルトのものを流用します

function App() {
  // サーバーからのメッセージを保存するための状態（変数）
  const [javaMessage, setJavaMessage] = useState('');
  const [pythonMessage, setPythonMessage] = useState('');

  // Javaサーバーを呼び出す関数
  const callJavaApi = async () => {
    try {
      const response = await fetch('http://localhost:8080/api/ping');
      const data = await response.text();
      setJavaMessage(data);
    } catch (error) {
      setJavaMessage('Javaサーバーの呼び出しに失敗しました。');
      console.error(error);
    }
  };

  // Pythonサーバーを呼び出す関数
  const callPythonApi = async () => {
    try {
      const response = await fetch('http://localhost:8000/ai/ping');
      const data = await response.json();
      setPythonMessage(data.message);
    } catch (error) {
      setPythonMessage('Pythonサーバーの呼び出しに失敗しました。');
      console.error(error);
    }
  };

  // --- 新しい機能：コード解析用 ---
    const [chordInput, setChordInput] = useState('Cmaj7'); // 入力欄用の状態
    const [analysisResult, setAnalysisResult] = useState(''); // 結果表示用の状態

    const handleAnalyzeChord = async () => {
        if (!chordInput) {
            setAnalysisResult('コードネームを入力してください。');
            return;
        }
        try {
            // Javaサーバーの新しいAPIを呼び出す
            const response = await fetch(`http://localhost:8080/api/chords/${chordInput}`);
            const data = await response.json();

            if (!response.ok) {
                // Pythonから返されたエラーメッセージを表示
                setAnalysisResult(`エラー: ${data.detail || '不明なエラー'}`);
            } else {
                // 成功した場合は、構成音を整形して表示
                setAnalysisResult(`構成音: ${data.notes.join(', ')}`);
            }
        } catch (error) {
            setAnalysisResult('サーバーの呼び出しに失敗しました。Javaサーバーは起動していますか？');
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
            
            {/* PingのテストUIはコメントアウトまたは削除してもOKです */}
            {/* <hr /> ... */}
        </>
    );
}

export default App;