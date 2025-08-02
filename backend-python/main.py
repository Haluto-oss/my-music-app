from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale, chord, roman
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

@app.get("/ai/analyze/chord")
def analyze_chord(name: str):
    # (この関数は変更なし)
    decoded_name = unquote(name)
    canonical_name = decoded_name.replace('b', '-')
    try:
        c = harmony.ChordSymbol(canonical_name)
        note_names_from_music21 = [p.name for p in c.pitches]
        display_note_names = [note.replace('-', 'b') for note in note_names_from_music21]
        return {"input_chord": decoded_name, "notes": display_note_names}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないコードネームです。")

@app.get("/ai/analyze/scale")
def analyze_scale(name: str):
    # (この関数は変更なし)
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
            quality = triad.quality
            base_roman = roman_numerals_upper[i]
            roman_figure = base_roman
            if quality == 'minor':
                roman_figure = base_roman.lower()
            elif quality == 'diminished':
                roman_figure = base_roman.lower() + '°'
            root_display_name = triad.root().name.replace('-', 'b')
            triad_suffix = ''
            if triad.quality == 'minor':
                triad_suffix = 'm'
            elif triad.quality == 'diminished':
                triad_suffix = 'dim'
            triad_name = f"{root_display_name}{triad_suffix}"
            seventh_suffix = '7'
            if seventh_chord.isMajorSeventh():
                seventh_suffix = 'maj7'
            elif seventh_chord.isMinorSeventh():
                seventh_suffix = 'm7'
            elif seventh_chord.isDiminishedSeventh():
                seventh_suffix = 'dim7'
            elif seventh_chord.isHalfDiminished():
                seventh_suffix = 'm7(b5)'
            seventh_chord_name = f"{root_display_name}{seventh_suffix}"
            diatonic_harmony_data.append({
                "degree": roman_figure, "function": functions[i],
                "chords": [triad_name, seventh_chord_name]
            })
        return {
            "input_scale": decoded_name,
            "scale_pitches": scale_pitches_for_display,
            "diatonic_harmony": diatonic_harmony_data
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないスケール名です。")

# --- ↓↓↓↓↓↓ この関数の中身を、より堅牢なロジックに修正しました ↓↓↓↓↓↓ ---
@app.post("/ai/transpose")
def transpose_progression(
    key_name: str = Body(...),
    degrees: list[str] = Body(...)
):
    """
    キーとディグリーネームのリストを受け取り、移調したコードネームのリストを返す
    """
    print(f"★ Python received transpose request: Key={key_name}, Degrees={degrees}")
    try:
        # music21でキーオブジェクトを作成
        # 'C' や 'c' -> C major, 'a' -> a minorのように賢く解釈してくれる
        target_key = harmony.key.Key(key_name)
        
        transposed_chords = []
        for degree_str in degrees:
            # ディグリーネームからローマ数字オブジェクトを作成
            rn = roman.RomanNumeral(degree_str, target_key)
            
            # ローマ数字オブジェクトから、ルート音とクオリティを取得してコード名を整形
            root_display_name = rn.root().name.replace('-', 'b')
            quality = rn.quality
            
            suffix = ''
            if quality == 'minor':
                suffix = 'm'
            elif quality == 'diminished':
                suffix = 'dim'
            
            # 7thなどの情報も考慮したい場合は、ここをさらに拡張できる
            final_chord_name = f"{root_display_name}{suffix}"
            transposed_chords.append(final_chord_name)

        return {"transposed_chords": transposed_chords}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="移調の処理中にエラーが発生しました。")