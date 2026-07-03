from .settings import *  # noqa: F401,F403

# pytest実行時はSupabase(リモートPostgres)に接続せず、SQLiteを使う。
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
