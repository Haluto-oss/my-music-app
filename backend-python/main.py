from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale
from urllib.parse import unquote

app = FastAPI()

# CORS設定
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
    print(f"★ Python received raw query: '{name}'")
    decoded_name = unquote(name)
    print(f"★ Python after unquote: '{decoded_name}'")
    canonical_name = decoded_name.replace('b', '-')
    print(f"★ Python canonical name for music21: '{canonical_name}'")
    try:
        c = harmony.ChordSymbol(canonical_name)
        note_names_from_music21 = [p.name for p in c.pitches]
        display_note_names = [note.replace('-', 'b') for note in note_names_from_music21]
        return {"input_chord": decoded_name, "notes": display_note_names}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"'{decoded_name}' は無効な、または解釈できないコードネームです。")


# main.py の analyze_scale 関数をこれに置き換えてください

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
        
        scale_pitches = [p.name.replace('-', 'b') for p in s.getPitches()]
        
        diatonic_chords = []
        for degree in range(1, 8):
            chord_obj = s.getChord(degree)
            roman_numeral = chord_obj.romanNumeral.figure
            common_name = chord_obj.commonName.replace(' minor triad', 'm').replace(' major triad', '').replace(' diminished triad', 'dim')
            diatonic_chords.append(f"{common_name} ({roman_numeral})")

        return {
            "input_scale": name,
            "scale_pitches": scale_pitches,
            "diatonic_chords": diatonic_chords
        }

    except Exception as e:
        # --- ↓↓↓ ここからがデバッグ用のコードです ↓↓↓ ---
        print("="*30)
        print("!!! AN EXCEPTION OCCURRED IN analyze_scale !!!")
        import traceback
        traceback.print_exc() # これがエラーの詳細を出力します
        print("="*30)
        # --- ↑↑↑ ここまでがデバッグ用のコードです ↑↑↑ ---
        raise HTTPException(status_code=400, detail=f"'{name}' は無効な、または解釈できないスケール名です。")