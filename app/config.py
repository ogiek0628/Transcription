import os

# セキュリティ用のシークレットキー
SECRET_KEY = 'secret_key'  # 変更してください

# アップロード先のディレクトリ
UPLOAD_FOLDER = 'uploads/'

# アップロードする最大サイズを指定（例: 16MB）
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 最大200MB

# SQLAlchemyの設定（使用している場合）
SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # SQLiteの例
SQLALCHEMY_TRACK_MODIFICATIONS = False
