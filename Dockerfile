# ベースイメージを指定
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /app

# 依存関係をインストール
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# FFmpegをインストール
RUN apt-get update && apt-get install -y ffmpeg

# アプリケーションコードをコピー
COPY . .

# アプリケーションを起動
CMD ["python", "app.py"]
