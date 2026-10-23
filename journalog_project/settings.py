from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Security fix: Remove wildcard '*' to prevent Host Header Injection attack.
# Explicitly list allowed hosts. Replace 'your-production-domain.com' with your actual domain.
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', 'journalog-app.onrender.com']

# 本番（DEBUG=False）のときだけ有効にするHTTPS・Cookieのセキュリティ設定。
# ローカル開発（DEBUG=True、http://localhost）には影響しない。
# `python manage.py check --deploy` の警告（W004 / W008 / W012 / W016）への対応。
if not DEBUG:
    # Render はHTTPSをプロキシで終端するため、プロキシが付ける X-Forwarded-Proto を信頼して
    # 「元のリクエストはHTTPSだった」と判断する（これがないとHTTPSリダイレクトが無限ループする）。
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    # HTTPでのアクセスを、HTTPSへリダイレクトする。
    SECURE_SSL_REDIRECT = True
    # ログイン状態（セッション）とCSRFトークンのCookieを、HTTPS経由でのみ送る。
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    # ブラウザに「このサイトは一定期間HTTPSでのみ接続する」と覚えさせる（HSTS）。
    # 一度設定すると、期間内はブラウザがHTTPで接続できなくなるため、まず1時間から始め、
    # 問題がないことを確認してから段階的に延ばす（最終的には1年 = 31536000 を目安にする）。
    SECURE_HSTS_SECONDS = 3600
    # このサイト（journalog-app.onrender.com）にサブドメインはなく、すべてHTTPSで配信されるため問題ない（W005）。
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    # W021（HSTSプリロードリストへの登録）は、自分で所有するドメインだけが対象。
    # *.onrender.com は登録できないため、意図的に無効にする。独自ドメインを使うようになったら見直す。
    SILENCED_SYSTEM_CHECKS = ['security.W021']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'journal.apps.JournalConfig',
    'accounts.apps.AccountsConfig',
    'widget_tweaks',
    'tailwind',
    'theme',
    'django_browser_reload',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django_browser_reload.middleware.BrowserReloadMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'journalog_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates' ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'journalog_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL')
    )
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_USER_MODEL = 'accounts.CustomUser'

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/




STATICFILES_DIRS = [
    BASE_DIR / 'static',
]
STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'journal:home'
LOGOUT_REDIRECT_URL = 'accounts:login'

TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
