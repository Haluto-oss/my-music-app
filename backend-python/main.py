from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale, chord
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

@app.get("/ai/analyze/chord")
def analyze_chord(name: str):
    try:
        decoded_name = unquote(name)
        canonical_name = decoded_name.replace('b', '-')
        c = harmony.ChordSymbol(canonical_name)
        note_names_from_music21 = [p.name for p in c.pitches]
        display_note_names = [note.replace('-', 'b') for note in note_names_from_music21]
        return {"input_chord": decoded_name, "notes": display_note_names}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないコードネームです。")


# main.py の analyze_scale 関数をこれに置き換えてください

@app.get("/ai/analyze/scale")
def analyze_scale(name: str):
    """
    スケール名を受け取り、その構成音とダイアトニックコードを返す
    """
    try:
        decoded_name = unquote(name)
        normalized_name = decoded_name.lower()
        parts = normalized_name.split()

        if len(parts) < 2:
            raise HTTPException(status_code=400, detail="スケールの種類を指定してください (例: 'C major', 'A minor')")

        tonic = parts[0]
        scale_type = " ".join(parts[1:])

        scale_map = {
            "major": scale.MajorScale, "minor": scale.MinorScale,
            "natural minor": scale.MinorScale, "harmonic minor": scale.HarmonicMinorScale,
            "melodic minor": scale.MelodicMinorScale
        }

        if scale_type not in scale_map:
            raise HTTPException(status_code=400, detail=f"サポートされていないスケールタイプです: '{scale_type}'")
        
        scale_class = scale_map[scale_type]
        s = scale_class(tonic)
        
        scale_pitches_obj = s.pitches[:-1]
        scale_pitches_for_display = [p.name.replace('-', 'b') for p in scale_pitches_obj]
        
        diatonic_harmony_data = []
        roman_numerals_upper = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        functions = ["Tonic", "Subdominant", "Tonic", "Subdominant", "Dominant", "Tonic", "Dominant"]
        
        for i in range(7):
            root = scale_pitches_obj[i]
            third = scale_pitches_obj[(i + 2) % 7]
            fifth = scale_pitches_obj[(i + 4) % 7]
            seventh = scale_pitches_obj[(i + 6) % 7]
            
            triad = chord.Chord([root, third, fifth])
            seventh_chord = chord.Chord([root, third, fifth, seventh])

            # ディグリーネームの整形
            triad_quality = triad.quality
            base_roman = roman_numerals_upper[i]
            roman_figure = base_roman
            if triad_quality == 'minor':
                roman_figure = base_roman.lower()
            elif triad_quality == 'diminished':
                roman_figure = base_roman.lower() + '°'
            
            # 3和音のコード名の整形
            root_display_name = triad.root().name.replace('-', 'b')
            triad_suffix = ''
            if triad_quality == 'minor':
                triad_suffix = 'm'
            elif triad_quality == 'diminished':
                triad_suffix = 'dim'
            triad_name = f"{root_display_name}{triad_suffix}"

            # --- ↓↓↓ セブンスコード名の生成ロジックを、最も確実な方法に修正しました ↓↓↓ ---
            
            # 4和音のクオリティを取得
            seventh_quality = seventh_chord.quality
            
            # クオリティの文字列に応じてサフィックスを決定する
            seventh_suffix = '7' # デフォルト (ドミナントセブンス)
            if seventh_quality == 'major-seventh':
                seventh_suffix = 'maj7'
            elif seventh_quality == 'minor-seventh':
                seventh_suffix = 'm7'
            elif seventh_quality == 'diminished-seventh':
                seventh_suffix = 'dim7'
            elif seventh_quality == 'half-diminished':
                seventh_suffix = 'm7(b5)'
                
            seventh_chord_name = f"{root_display_name}{seventh_suffix}"

            diatonic_harmony_data.append({
                "degree": roman_figure,
                "function": functions[i],
                "chords": [triad_name, seventh_chord_name]
            })

        return {
            "input_scale": decoded_name,
            "scale_pitches": scale_pitches_for_display,
            "diatonic_harmony": diatonic_harmony_data
        }

    except Exception as e:
        # デバッグが終わったらこの3行は消してもOKです
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないスケール名です。")