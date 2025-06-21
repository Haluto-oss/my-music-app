from fastapi import FastAPI, HTTPException  # <--- HTTPExceptionを追加
from fastapi.middleware.cors import CORSMiddleware
from music21 import chord  # <--- music21ライブラリからchordをインポート
from music21 import harmony

app = FastAPI()

# CORS設定: フロントエンド(http://localhost:5173)からのアクセスを許可
# 将来フロントエンドと通信するために、この設定を入れておきます
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

# ---Chord分析のコード---

@app.get("/ai/analyze/chord/{chordName}")
def analyze_chord(chordName: str):
    """
    コードネームを受け取り、music21を使って構成音を解析して返すエンドポイント
    """
    try:
        # chord.Chord() の代わりに harmony.ChordSymbol() を使います
        c = harmony.ChordSymbol(chordName)
        
        # 構成音の名前をリストとして取得 (例: ['C', 'E', 'G'])
        note_names = [p.name for p in c.pitches]
        
        # 成功した場合は、入力されたコードと構成音のリストを返す
        return {"input_chord": chordName, "notes": note_names}
    except Exception as e:
        # music21が解析に失敗した場合（無効なコードネームなど）
        # 400 Bad Requestエラーをクライアントに返す
        raise HTTPException(status_code=400, detail=f"'{chordName}' は無効な、または解釈できないコードネームです。")