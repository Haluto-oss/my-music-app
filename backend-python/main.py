from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from music21 import harmony
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
        
        note_names = [p.name for p in c.pitches]
        
        # ユーザーへの応答には、デコード後の分かりやすい名前(decoded_name)を使う
        return {"input_chord": decoded_name, "notes": note_names}
    except Exception as e:
        # エラーメッセージにも、デコード後の分かりやすい名前を使う
        raise HTTPException(status_code=400, detail=f"'{decoded_name}' は無効な、または解釈できないコードネームです。")