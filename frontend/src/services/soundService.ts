import * as Tone from 'tone';

// シンプルなシンセサイザーを1つだけ作成し、アプリ全体で使い回す
const synth = new Tone.Synth().toDestination();

/**
 * 指定された音を再生する関数
 * @param note - 再生する音名 (例: "C4", "F#5")
 */
export async function playSound(note: string) {
  try {
    // ユーザーがページ上で何か操作をするまで、音声はミュートされている
    // Tone.start()は、ユーザーの操作をきっかけに音声のミュートを解除する重要な命令
    if (Tone.context.state !== 'running') {
      await Tone.start();
    }
    // 指定された音を、8分音符の長さで再生する
    synth.triggerAttackRelease(note, "8n");
  } catch (e) {
    console.error("サウンドの再生に失敗しました。", e);
  }
}