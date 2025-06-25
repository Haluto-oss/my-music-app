# 1. Python 3.11 の軽量な公式イメージをベースにする
FROM python:3.11-slim

# 2. コンテナ内の作業ディレクトリを作成・指定
WORKDIR /app

# 3. 最初にrequirements.txtだけをコピーする（キャッシュを効かせるため）
COPY ./requirements.txt /app/requirements.txt

# 4. 依存ライブラリをインストールする
RUN python -m pip install --no-cache-dir -r requirements.txt

# 5. プロジェクトのすべてのファイルをコピーする
COPY . /app

# 6. コンテナ起動時に実行するコマンドを指定
# --host 0.0.0.0 は、コンテナの外からアクセスできるようにするために必須
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]