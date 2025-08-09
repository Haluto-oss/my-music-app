from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony, scale, chord, roman, key, interval
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
        if len(parts) == 0:
             raise HTTPException(status_code=400, detail="スケール名を入力してください。")
        
        # ユーザー入力からtonicとscale_typeを抽出
        tonic_str = parts[0]
        # 'c', 'major' -> 'major' | 'c', 'harmonic', 'minor' -> 'harmonic minor'
        scale_type = " ".join(parts[1:]) if len(parts) > 1 else "major" # 1単語の場合はmajorとみなす

        scale_map = {
            "major": scale.MajorScale, "ionian": scale.MajorScale,
            "minor": scale.MinorScale, "natural minor": scale.MinorScale, "aeolian": scale.MinorScale,
            "harmonic minor": scale.HarmonicMinorScale,
            "melodic minor": scale.MelodicMinorScale,
            "dorian": scale.DorianScale, "phrygian": scale.PhrygianScale,
            "lydian": scale.LydianScale, "mixolydian": scale.MixolydianScale,
            "locrian": scale.LocrianScale,
            "whole tone": scale.WholeToneScale, "chromatic": scale.ChromaticScale,
            # lambda式でカスタムスケールを定義するのは素晴らしいアプローチです！
            "pentatonic": lambda p: scale.ConcreteScale(pitches=[p, p.transpose('M2'), p.transpose('M3'), p.transpose('P5'), p.transpose('M6')]),
            "minor pentatonic": lambda p: scale.ConcreteScale(pitches=[p, p.transpose('m3'), p.transpose('P4'), p.transpose('P5'), p.transpose('m7')]),
            "blues": lambda p: scale.ConcreteScale(pitches=[p, p.transpose('m3'), p.transpose('P4'), p.transpose('d5'), p.transpose('P5'), p.transpose('m7')])
        }

        if scale_type not in scale_map:
            raise HTTPException(status_code=400, detail=f"サポートされていないスケールタイプです: '{scale_type}'")

        scale_creator = scale_map[scale_type]
        # ConcreteScaleはtonicを引数に取らないため、分岐を追加
        if isinstance(scale_creator, type): # MajorScaleなどのクラスの場合
             s = scale_creator(tonic_str)
        else: # lambda式の場合
             from music21 import pitch
             s = scale_creator(pitch.Pitch(tonic_str))

        scale_pitches_obj = s.pitches
        # オクターブ違いの最後の音を削除（7音以上のスケールの場合）
        if len(scale_pitches_obj) > 7:
            scale_pitches_obj = scale_pitches_obj[:-1]
            
        scale_pitches_for_display = [p.name.replace('-', 'b') for p in scale_pitches_obj]
        
        diatonic_harmony_data = []
        # ダイアトニックコードは7音スケールの場合のみ生成
        if len(scale_pitches_obj) == 7:
            functions = ["Tonic", "Supertonic", "Mediant", "Subdominant", "Dominant", "Submediant", "Leading Tone"]
            roman_numerals_upper = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII']
            
            for i in range(7):
                root = scale_pitches_obj[i]
                third = scale_pitches_obj[(i + 2) % 7]
                fifth = scale_pitches_obj[(i + 4) % 7]
                seventh = scale_pitches_obj[(i + 6) % 7]
                
                triad = chord.Chord([root, third, fifth])
                seventh_chord = chord.Chord([root, third, fifth, seventh])
                
                # Roman Numeral Figure
                quality = triad.quality
                base_roman = roman_numerals_upper[i]
                roman_figure = base_roman
                if quality == 'minor':
                    roman_figure = base_roman.lower()
                elif quality == 'diminished':
                    roman_figure = base_roman.lower() + '°'
                elif quality == 'augmented':
                    roman_figure = base_roman.upper() + '+'

                # Triad Name
                root_display_name = triad.root().name.replace('-', 'b')
                triad_suffix = ''
                if quality == 'minor':
                    triad_suffix = 'm'
                elif quality == 'diminished':
                    triad_suffix = 'dim'
                elif quality == 'augmented':
                    triad_suffix = 'aug'
                triad_name = f"{root_display_name}{triad_suffix}"
                
                # Seventh Chord Name
                seventh_quality = seventh_chord.quality
                seventh_suffix = '7'
                if seventh_quality == 'major-seventh':
                    seventh_suffix = 'maj7'
                elif seventh_quality == 'minor-seventh':
                    seventh_suffix = 'm7'
                elif seventh_quality in ['half-diminished-seventh', 'half-diminished']:
                    seventh_suffix = 'm7(b5)'
                elif seventh_quality == 'diminished-seventh':
                    seventh_suffix = 'dim7'
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
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"'{unquote(name)}' は無効な、または解釈できないスケール名です。エラー: {e}")


@app.get("/ai/transpose")
def transpose_progression(
    key_name: str,
    degrees: list[str] = Query(...)
):
    """
    キーとディグリーネームのリストを受け取り、移調したコードネームのリストを返す
    """
    try:
        # --- ↓↓↓ このURLデコード処理を追加しました ↓↓↓ ---
        decoded_key_name = unquote(key_name)
        
        # --- ↓↓↓ キーの解釈を、より正確にするロジックに修正しました ↓↓↓ ---
        key_str_lower = decoded_key_name.lower()
        mode = 'major' # デフォルトはメジャー
        tonic_str = key_str_lower.replace('major', '').strip()

        if 'm' in key_str_lower and not key_str_lower.endswith('major'):
            mode = 'minor'
            tonic_str = key_str_lower.replace('m', '')
        
        target_key = key.Key(tonic_str, mode)
        
        transposed_chords = []
        for degree_str in degrees:
            rn = roman.RomanNumeral(degree_str, target_key)
            
            root_display_name = rn.root().name.replace('-', 'b')
            quality = rn.quality
            
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
        raise HTTPException(status_code=400, detail=f"移調の処理中にエラーが発生しました。")
