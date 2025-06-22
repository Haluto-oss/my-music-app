from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale, chord, roman  # <--- roman を追加
from urllib.parse import unquote

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
    # (この関数は変更なし)
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
        
        scale_pitches_obj = s.pitches
        scale_pitches_for_display = [p.name.replace('-', 'b') for p in scale_pitches_obj]
        
        # --- ↓↓↓↓↓↓ この部分を、完全に手動のロジックに書き換えました ↓↓↓↓↓↓ ---
        diatonic_chords = []
        # ローマ数字の基本形
        roman_numerals_upper = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']

        for i in range(7):
            root = scale_pitches_obj[i]
            third = scale_pitches_obj[(i + 2) % 7]
            fifth = scale_pitches_obj[(i + 4) % 7]
            
            chord_obj = chord.Chord([root, third, fifth])
            
            # コードのクオリティ（major, minor, diminishedなど）を判定
            quality = chord_obj.quality
            
            # クオリティに応じてディグリーネームを組み立てる
            base_roman = roman_numerals_upper[i]
            if quality == 'minor':
                roman_figure = base_roman.lower()
            elif quality == 'diminished':
                roman_figure = base_roman.lower() + '°'
            else: # major or other
                roman_figure = base_roman

            # 表示用のコード名を整形
            common_name = chord_obj.commonName.replace(' triad', '')
            display_name = common_name.replace('-', 'b')
            
            diatonic_chords.append(f"{display_name} ({roman_figure})")

        return {
            "input_scale": name,
            "scale_pitches": scale_pitches_for_display,
            "diatonic_chords": diatonic_chords
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"'{name}' は無効な、または解釈できないスケール名です。")