from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale
from urllib.parse import unquote  # <--- URLデコードのために追加


app = FastAPI()

# CORS設定 (変更なし)
origins = [
    "http://localhost:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/ai/ping")
def ping():
    return {"message": "Pong from Python! (Pythonからの返事です)"}


@app.get("/ai/analyze/chord")
def analyze_chord(name: str):
    """
    コードネームを受け取り、前処理をしてからmusic21で解析するエンドポイント
    """
    # --- ここから下が最終修正版 ---
    print(f"★ Python received raw query: '{name}'")

    # 1. URLデコード処理 (例: 'C%23' を 'C#' に戻す)
    decoded_name = unquote(name)
    print(f"★ Python after unquote: '{decoded_name}'")

    # 2. フラット記号の正規化 (例: 'Bb' を 'B-' に変換)
    # これで music21 が最も解釈しやすい形式になる
    canonical_name = decoded_name.replace('b', '-')
    print(f"★ Python canonical name for music21: '{canonical_name}'")

    try:
        # music21には、正規化された名前(canonical_name)を渡す
        c = harmony.ChordSymbol(canonical_name)

        # 1. music21から標準的な構成音リストを取得 (例: ['B-', 'D', 'F'])
        note_names_from_music21 = [p.name for p in c.pitches]
        
        # 2. ユーザー表示用に '-' を 'b' に変換 (例: ['Bb', 'D', 'F'])
        display_note_names = [note.replace('-', 'b') for note in note_names_from_music21]
        
        # 3. 変換後のリスト(display_note_names)を返す
        return {"input_chord": decoded_name, "notes": display_note_names}
        
        note_names = [p.name for p in c.pitches]
        
        # ユーザーへの応答には、デコード後の分かりやすい名前(decoded_name)を使う
        return {"input_chord": decoded_name, "notes": note_names}
    except Exception as e:
        # エラーメッセージにも、デコード後の分かりやすい名前を使う
        raise HTTPException(status_code=400, detail=f"'{decoded_name}' は無効な、または解釈できないコードネームです。")
    
@app.get("/ai/analyze/scale")
def analyze_scale(name: str):
    """
    スケール名を受け取り、その構成音とダイアトニックトライアド（3和音）を返す
    """
    print(f"★ Python received scale name query: '{name}'")
    try:
        normalized_name = name.lower()
        parts = normalized_name.split()

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="スケールの種類を指定してください (例: 'C major', 'A minor')")

        tonic = parts[0]
        scale_type = " ".join(parts[1:])

        scale_map = {
            "major": scale.MajorScale,
            "minor": scale.MinorScale,
            "natural minor": scale.MinorScale,
            "harmonic minor": scale.HarmonicMinorScale,
            "melodic minor": scale.MelodicMinorScale
        }

        if scale_type in scale_map:
            scale_class = scale_map[scale_type]
            s = scale_class(tonic)
        else:
            raise HTTPException(status_code=400, detail=f"サポートされていないスケールタイプです: '{scale_type}'")
        
        # 1. スケール構成音のリストを作成
        scale_pitches = [p.name.replace('-', 'b') for p in s.getPitches()]
        
        # 2. ダイアトニックコード（3和音）のリストを作成
        diatonic_chords = []
        # 1から7の各音度についてループ
        for degree in range(1, 8):
            # その音度上の3和音を取得
            chord_obj = s.getChord(degree)
            # 'C major triad' のような名前から、'C' や 'Dm' のような一般的な名前に変換
            # ダイアトニックコードの表示に、C (I)やDm (ii)のようにローマ数字のディグリーネームも追加
            chord_name_with_degree = f"{chord_obj.commonName.replace(' minor triad', 'm').replace(' major triad', '').replace(' diminished triad', 'dim')} ({chord_obj.romanNumeral.figure})"
            diatonic_chords.append(chord_name_with_degree)

        return {
            "input_scale": name,
            "scale_pitches": scale_pitches,
            "diatonic_chords": diatonic_chords
        }

    except Exception as e:
        # music21が音名を解釈できない場合などもここでエラーになる
        raise HTTPException(status_code=400, detail=f"'{name}' は無効な、または解釈できないスケール名です。")