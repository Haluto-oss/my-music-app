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
    スケール名を受け取り、構成音、機能、ダイアトニックコード(3和音と4和音)を返す
    """
    print(f"★ Python received scale name query: '{name}'")
    try:
        # ... (スケールオブジェクトsを作成するまでのロジックは変更なし) ...
        normalized_name = name.lower()
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
        if scale_type in scale_map:
            scale_class = scale_map[scale_type]
            s = scale_class(tonic)
        else:
            raise HTTPException(status_code=400, detail=f"サポートされていないスケールタイプです: '{scale_type}'")

        # --- ↓↓↓ ここから下のロジックを、よりリッチな情報を生成するように変更 ↓↓↓ ---

        scale_pitches_obj = s.pitches[:-1]
        scale_pitches_for_display = [p.name.replace('-', 'b') for p in scale_pitches_obj]
        
        # メジャースケールの機能（Function）を定義
        # (マイナースケールなどは別途定義が必要だが、今回はメジャーのみ対応)
        functions = ["Tonic", "Subdominant", "Tonic", "Subdominant", "Dominant", "Tonic", "Dominant"]
        roman_numerals_upper = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
        
        diatonic_harmony = []
        for i in range(7):
            # --- 3和音（トライアド）を生成 ---
            c3_root = scale_pitches_obj[i]
            c3_third = scale_pitches_obj[(i + 2) % 7]
            c3_fifth = scale_pitches_obj[(i + 4) % 7]
            triad = chord.Chord([c3_root, c3_third, c3_fifth])
            
            # --- 4和音（セブンスコード）を生成 ---
            c4_seventh = scale_pitches_obj[(i + 6) % 7]
            seventh_chord = chord.Chord([c3_root, c3_third, c3_fifth, c4_seventh])
            
            # --- 表示用のデータを整形 ---
            # ディグリーネーム (I, ii, iii°, など)
            quality = triad.quality
            base_roman = roman_numerals_upper[i]
            if quality == 'minor':
                roman_figure = base_roman.lower()
            elif quality == 'diminished':
                roman_figure = base_roman.lower() + '°'
            else: # major
                roman_figure = base_roman

            # コード名 (C, Dm, Cmaj7, Dm7, など)
            triad_name = triad.root().name.replace('-', 'b') + triad.commonName.replace(' major triad', '').replace(' minor triad', 'm').replace(' diminished triad', 'dim')
            seventh_chord_name = seventh_chord.pitchedCommonName.replace('-', 'b')

            # 最終的なデータを組み立てる
            diatonic_harmony.append({
                "degree": roman_figure,
                "function": functions[i],
                "chords": [triad_name, seventh_chord_name]
            })

        return {
            "input_scale": name,
            "scale_pitches": scale_pitches_for_display,
            "diatonic_harmony": diatonic_harmony # <--- 返すデータのキーを変更
        }

    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"'{name}' は無効な、または解釈できないスケール名です。")