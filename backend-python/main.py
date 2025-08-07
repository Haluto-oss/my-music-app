from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale, chord, roman, key
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
    try:
        decoded_name = unquote(name)
        canonical_name = decoded_name.replace('b', '-')
        c = harmony.ChordSymbol(canonical_name)
        note_names_from_music21 = [p.name for p in c.pitches]
        display_note_names = [note.replace('-', 'b') for note in note_names_from_music21]
        return {"input_chord": decoded_name, "notes": display_note_names}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないコードネームです。")


@app.get("/ai/analyze/scale")
def analyze_scale(name: str):
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

# main.py の transpose_progression 関数をこれに置き換えてください

@app.get("/ai/transpose")
def transpose_progression(
    key_name: str,
    degrees: list[str] = Query(...)
):
    """
    キーとディグリーネームのリストを受け取り、移調したコードネームのリストを返す
    """
    try:
        # --- ↓↓↓ キーとディグリーからコードを特定するロジックを、根本から書き直しました ↓↓↓ ---

        # 1. まず、指定されたキーのスケール（音階）を特定する
        key_str_lower = key_name.lower()
        scale_type = 'major'
        tonic = key_str_lower
        if 'm' in key_str_lower:
            scale_type = 'minor'
            tonic = key_str_lower.replace('m', '')
        
        target_scale = scale.MinorScale(tonic) if scale_type == 'minor' else scale.MajorScale(tonic)
        
        # 2. スケールの構成音（ピッチオブジェクト）を取得
        scale_pitches = target_scale.getPitches()

        # 3. ディグリーネームと、スケールの何番目の音かを対応付ける辞書
        degree_map = {
            'i': 1, 'I': 1,
            'ii': 2, 'II': 2,
            'iii': 3, 'III': 3,
            'iv': 4, 'IV': 4,
            'v': 5, 'V': 5,
            'vi': 6, 'VI': 6,
            'vii': 7, 'VII': 7
        }

        transposed_chords = []
        for degree_str in degrees:
            # "vi" や "iv" から "vi" や "iv" を取り出す
            # "VII" から "VII" を取り出す
            clean_degree = degree_str.replace('°', '').replace('dim', '')
            
            if clean_degree not in degree_map:
                # 不明なディグリーの場合はスキップ
                transposed_chords.append('?')
                continue

            # 4. ディグリーに対応するルート音をスケールから取得
            # (リストのインデックスは0から始まるので、-1する)
            root_pitch = scale_pitches[degree_map[clean_degree] - 1]

            # 5. コードのクオリティ（major/minor/diminished）をディグリーから判断
            # (小文字のローマ数字はマイナーかディミニッシュ)
            quality = 'major'
            if degree_str.islower():
                quality = 'minor'
            if '°' in degree_str or 'dim' in degree_str:
                quality = 'diminished'
            
            # 6. ルート音とクオリティからコード名を組み立てる
            root_display_name = root_pitch.name.replace('-', 'b')
            suffix = ''
            if quality == 'minor':
                suffix = 'm'
            elif quality == 'diminished':
                suffix = 'dim'
            
            final_chord_name = f"{root_display_name}{suffix}"
            transposed_chords.append(final_chord_name)

        return {"transposed_chords": transposed_chords}

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail="移調の処理中にエラーが発生しました。")