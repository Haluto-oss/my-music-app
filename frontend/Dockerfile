# --- 第1ステージ: ビルド環境 ---
# Node.jsの公式イメージをベースにする
FROM node:20-alpine AS builder

# 作業ディレクトリを作成
WORKDIR /app

# package.jsonとlockファイルを先にコピーして、依存関係をインストール
COPY package*.json ./
RUN npm install

# ソースコードをコピー
COPY . .

# Reactアプリをビルド（静的なHTML/CSS/JSファイルに変換）
RUN npm run build


# --- 第2ステージ: 実行環境 ---
# Nginxという軽量なWebサーバーの公式イメージをベースにする
FROM nginx:stable-alpine

# 第1ステージ(builder)でビルドされた静的ファイル群を、Nginxの公開フォルダにコピー
COPY --from=builder /app/dist /usr/share/nginx/html

# Nginxサーバーはデフォルトで80番ポートを公開する
EXPOSE 80