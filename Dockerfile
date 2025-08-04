# ─────────────────────────────────
# １．ビルドステージ
# ─────────────────────────────────
FROM python:3.12-slim AS builder

# 作業ディレクトリ
WORKDIR /app

# 依存リストだけ先にコピーしてキャッシュ効かせる
COPY requirements.txt .

# pip のキャッシュを残さずにインストール
RUN pip install --user --no-cache-dir -r requirements.txt

# ─────────────────────────────────
# ２．ランタイムステージ
# ─────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

# ビルドステージでインストールしたパッケージだけをコピー
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# アプリ本体をコピー
COPY . .

# Fly.io のデフォルトポートを参照
ENV PORT 8080

# 起動コマンド（Flask＋Gunicorn の例）
ENTRYPOINT ["sh", "-c", "exec gunicorn app:app --bind 0.0.0.0:${PORT}"]


