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

  return (
    <>
      <h1>My Music App フロントエンド</h1>
      <div className="card">
        <button onClick={callJavaApi}>
          Javaサーバーを呼ぶ
        </button>
        <p>サーバーからの返事: {javaMessage}</p>
      </div>
      <hr />
      <div className="card">
        <button onClick={callPythonApi}>
          Pythonサーバーを呼ぶ
        </button>
        <p>サーバーからの返事: {pythonMessage}</p>
      </div>
    </>
  );
}

export default App;