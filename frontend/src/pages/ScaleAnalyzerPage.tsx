import { useState } from 'react';

// APIから返ってくるダイアトニックコードのデータの「型」を定義
interface DiatonicHarmony {
  degree: string;
  function: string;
  chords: string[];
}

export function ScaleAnalyzerPage() {
  // スケール解析機能で使う状態（変数）をすべてここで管理
  const [scaleInput, setScaleInput] = useState('C major');
  const [scalePitchesResult, setScalePitchesResult] = useState<string[]>([]);
  const [diatonicHarmonyResult, setDiatonicHarmonyResult] = useState<DiatonicHarmony[]>([]);
  const [scaleError, setScaleError] = useState('');

  const handleAnalyzeScale = async () => {
    // ボタンが押されたら、まず以前の結果をリセットする
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
        // エラー応答の場合
        setScaleError(`エラー: ${data.detail || '不明なエラー'}`);
      } else {
        // 成功した場合
        setScalePitchesResult(data.scale_pitches);
        setDiatonicHarmonyResult(data.diatonic_harmony);
      }
    } catch (error) {
      setScaleError('サーバーの呼び出しに失敗しました。');
      console.error(error);
    }
  };

  return (
    <div className="card">
      <h2>スケール・ダイアトニックコード解析</h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <input
          type="text"
          value={scaleInput}
          onChange={(e) => setScaleInput(e.target.value)}
          placeholder="例: C major, A harmonic minor"
        />
        <button onClick={handleAnalyzeScale}>
          解析する
        </button>
      </div>

      {/* --- 結果表示エリア --- */}
      {/* エラーがある場合のみ表示 */}
      {scaleError && <p style={{ color: 'red' }}>{scaleError}</p>}
      
      {/* スケール構成音の結果がある場合のみ表示 */}
      {(scalePitchesResult && scalePitchesResult.length > 0) && (
        <p><b>スケール構成音: {scalePitchesResult.join(', ')}</b></p>
      )}
      
      {/* ダイアトニックコードの結果がある場合のみ表示 */}
      {(diatonicHarmonyResult && diatonicHarmonyResult.length > 0) && (
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
  );
}