// src/pages/ChordAnalyzerPage.tsx

import { useState } from 'react';
import { Piano } from 'react-piano';
import { Note } from 'tonal';
import { playSound } from '../services/soundService';

// react-piano用のCSSをインポート
import 'react-piano/dist/styles.css';

export function ChordAnalyzerPage() {
  // --- 既存の状態管理 ---
  const [chordInput, setChordInput] = useState('Cmaj7');
  const [analysisResult, setAnalysisResult] = useState('');
  const [constituentNotes, setConstituentNotes] = useState<string[]>([]);

  // --- UIと連携するための新しい状態管理 ---
  const [activeMidiNotes, setActiveMidiNotes] = useState<number[]>([]);
  const [instrument, setInstrument] = useState<'none' | 'piano'>('none');

  const handleAnalyzeChord = async () => {
    // 以前の結果をリセット
    setAnalysisResult('');
    setConstituentNotes([]);
    setActiveMidiNotes([]);

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
        // 解析結果をそれぞれの状態に保存
        setAnalysisResult(`構成音: ${data.notes.join(', ')}`);
        setConstituentNotes(data.notes);

        // ピアノのハイライト用に、音名をMIDI番号に変換して保存
        const midiNotes = data.notes.map((note: string) => Note.midi(`${note}4`)).filter(Boolean) as number[];
        setActiveMidiNotes(midiNotes);
      }
    } catch (error) {
      setAnalysisResult('サーバーの呼び出しに失敗しました。');
      console.error(error);
    }
  };

  const handlePlayNote = (note: string) => {
    // 音名にオクターブ番号'4'を付けて再生
    playSound(`${note}4`);
  };

  return (
    <div className="card">
      <h2>コード構成音 解析</h2>
      <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
        <input
          type="text"
          value={chordInput}
          onChange={(e) => setChordInput(e.target.value)}
          placeholder="例: Cmaj7, Fm7b5"
        />
        <button onClick={handleAnalyzeChord}>解析する</button>
      </div>
      
      {/* --- 結果表示エリア --- */}
      {/* constituentNotes配列の各音を、クリック可能なボタンとして表示 */}
      <div style={{ marginTop: '1rem' }}>
        {constituentNotes.length > 0 ? (
          <p>
            構成音:
            {constituentNotes.map((note) => (
              <button key={note} onClick={() => handlePlayNote(note)} className="note-tag">
                {note}
              </button>
            ))}
          </p>
        ) : (
          <p>{analysisResult}</p>
        )}
      </div>

      {/* --- 楽器の表示切り替えボタン --- */}
      <div style={{ marginTop: '2rem' }}>
        <button onClick={() => setInstrument(instrument === 'piano' ? 'none' : 'piano')}>
          {instrument === 'piano' ? 'ピアノを隠す' : 'ピアノを表示'}
        </button>
        {/* 将来的にギターやベースのボタンもここに追加できる */}
      </div>

      {/* --- ピアノUIの表示 --- */}
      {instrument === 'piano' && (
        <div style={{ marginTop: '1rem' }}>
          <Piano
            noteRange={{ first: Note.midi('C3') as number, last: Note.midi('B5') as number }}
            playNote={() => {}} // 音声再生は自前のTone.jsで行うため、ここでは何もしない
            stopNote={() => {}}
            width={500}
            activeNotes={activeMidiNotes} // 解析結果の音をハイライト
          />
        </div>
      )}
    </div>
  );
}