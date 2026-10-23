from .settings import *  # noqa: F401,F403

# pytest実行時はSupabase(リモートPostgres)に接続せず、SQLiteを使う。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# テストのクライアントは http://testserver へアクセスするため、本番用のHTTPS関連の設定
# （settings.py の `if not DEBUG:` ブロック）は無効にする。
# 本番設定が正しいかは test_security_settings.py で別途確認する。
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_HSTS_SECONDS = 0
