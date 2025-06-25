# --- 第1ステージ: ビルド環境 ---
# Maven(ビルドツール)とJava 17(JDK)が入ったイメージをベースにする
FROM maven:3.9-eclipse-temurin-17 AS builder

# 作業ディレクトリを作成
WORKDIR /app

# 最初にpom.xmlだけをコピーして、依存関係を先にダウンロードする
COPY pom.xml .
RUN mvn dependency:go-offline

# ソースコードをコピー
COPY src ./src

# アプリケーションをビルド（コンパイルしてjarファイルを作成）
RUN mvn package -DskipTests


# --- 第2ステージ: 実行環境 ---
# Javaの実行環境(JRE)のみの、非常に軽量なイメージをベースにする
FROM eclipse-temurin:17-jre-jammy

# 作業ディレクトリを作成
WORKDIR /app

# 第1ステージ(builder)から、ビルドされたjarファイルだけをコピーしてくる
COPY --from=builder /app/target/*.jar app.jar

# コンテナ起動時に、そのjarファイルを実行するコマンド
CMD ["java", "-jar", "app.jar"]