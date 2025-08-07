import { useState, useEffect } from 'react';

// APIから受け取るデータの型を定義
interface ProgressionData {
  name: string;
  description: string;
  key: string;      // APIからはデフォルトキーが "key" という名前で返ってくる
  degrees: string[];
  chords: string[]; // APIからはデフォルトキーのコードネームが返ってくる
}

// ページ内で管理するコード進行のデータの型
interface ProgressionDisplay extends ProgressionData {
  displayChords: string[]; // ユーザーがキーを変更した際に、移調後のコードを保持する
}

export function FamousProgressionsPage() {
  const [progressions, setProgressions] = useState<ProgressionDisplay[]>([]);
  const [error, setError] = useState('');
  // 表示モード（コードネームかディグリーネームか）を管理する新しい状態
  const [displayMode, setDisplayMode] = useState<'chords' | 'degrees'>('chords');

  // キーの選択肢
  const keys = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "G#", "A", "Bb", "B"];
  const minorKeys = ["Am", "A#m", "Bm", "Cm", "C#m", "Dm", "D#m", "Em", "Fm", "F#m", "Gm", "G#m"];


  // ページ読み込み時に、有名コード進行の基本データを取得する
  useEffect(() => {
    const fetchInitialProgressions = async () => {
      try {
        const response = await fetch('http://localhost:8080/api/progressions');
        if (!response.ok) {
          throw new Error('データの取得に失敗しました。');
        }
        const data: ProgressionData[] = await response.json();

        // 取得したデータに、移調後のコードを保持する場所を追加してstateに保存
        setProgressions(data.map(p => ({ ...p, displayChords: p.chords })));
      } catch (err) {
        setError('サーバーからデータを取得できませんでした。');
      }
    };

    fetchInitialProgressions();
  }, []); // 第2引数の配列が空なので、初回レンダリング時にのみ実行される

  // キーが変更されたときに、Pythonに移調をリクエストする関数
  const handleKeyChange = async (progIndex: number, newKey: string) => {
    const targetProg = progressions[progIndex];

    // もし移調先のキーが現在のキーと同じなら、何もしない
    if (targetProg.key === newKey) return;

    try {
      // Javaに新しく作るAPIを呼び出す
      const response = await fetch(`http://localhost:8080/api/progressions/transpose`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ key_name: newKey, degrees: targetProg.degrees }),
      });
      if (!response.ok) throw new Error('移調失敗');
      const data = await response.json();

      // progressions配列の、特定の要素だけを更新する
      const updatedProgressions = [...progressions];
      updatedProgressions[progIndex] = {
        ...targetProg,
        key: newKey,
        displayChords: data.transposed_chords,
      };
      setProgressions(updatedProgressions);

    } catch (err) {
      // エラー表示（今回はシンプルにconsole.log）
      console.error("移調に失敗しました:", err);
      alert(`キー「${newKey}」への移調に失敗しました。`);
    }
  };


  if (error) {
    return <p style={{ color: 'red' }}>{error}</p>;
  }

  return (
    <div>
      <h2>有名コード進行まとめ</h2>
      {/* 表示モードを切り替えるボタン */}
      <button onClick={() => setDisplayMode(displayMode === 'chords' ? 'degrees' : 'chords')} style={{ marginBottom: '1rem' }}>
        {displayMode === 'chords' ? 'ディグリーネームで表示' : 'コードネームで表示'}
      </button>

      {progressions.map((prog, index) => (
        <div key={prog.name} className="card">
          <h3>{prog.name}</h3>
          <p>{prog.description}</p>
          
          {/* キーを選択するためのドロップダウンメニュー */}
          <div style={{ marginBottom: '1rem' }}>
            <strong>キー: </strong>
            <select value={prog.key} onChange={(e) => handleKeyChange(index, e.target.value)}>
              <optgroup label="Major Keys">
                {keys.map(k => <option key={k} value={k}>{k}</option>)}
              </optgroup>
              <optgroup label="Minor Keys">
                {minorKeys.map(k => <option key={k} value={k}>{k}</option>)}
              </optgroup>
            </select>
          </div>

          {/* コード/ディグリー進行の表示 */}
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {(displayMode === 'chords' ? (prog.displayChords || []) : prog.degrees).map((item, i) => (
              <span key={i} className="note-tag">{item}</span>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}