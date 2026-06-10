# Bootstrap → Tailwind CSS 移行 実装計画

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bootstrap 5.3.0 を完全削除し、Tailwind CSS v3（django-tailwind）+ Alpine.js へ移行しながらモダン・カード型 UI に刷新する。

**Architecture:** django-tailwind が Tailwind v3 の npm ビルドを manage.py ワークフローに統合。Alpine.js（CDN）がナビバードロップダウンの Bootstrap JS を置き換える。フィーチャーテーマ（goal/todo/schedule/reflection）は `@layer components` でコンポーネントクラスとして定義し、`{{ feature }}-card` のような動的クラス生成に対応する。

**Tech Stack:** Django 6.0, django-tailwind (Tailwind CSS v3), Alpine.js v3 (CDN), django-browser-reload, whitenoise

---

## ファイルマップ

| 操作 | パス |
|------|------|
| 修正 | `requirements.txt` |
| 修正 | `journalog_project/settings.py` |
| 修正 | `journalog_project/urls.py` |
| 生成 | `theme/`（django-tailwind が自動生成） |
| 修正 | `theme/static_src/tailwind.config.js` |
| 修正 | `theme/static_src/src/styles.css` |
| 修正 | `templates/base.html` |
| 修正 | `accounts/templates/registration/login.html` |
| 修正 | `accounts/templates/accounts/signup.html` |
| 修正 | `journal/templates/journal/home.html` |
| 修正 | `journal/templates/journal/journal_init.html` |
| 修正 | `journal/templates/journal/journal_over.html` |
| 修正 | `templates/common/create_base.html` |
| 修正 | `templates/common/update_base.html` |
| 修正 | `templates/common/delete_base.html` |
| 確認 | `journal/templates/journal/create_*.html`（4 ファイル） |
| 確認 | `journal/templates/journal/update_*.html`（4 ファイル） |
| 確認 | `journal/templates/journal/delete_*.html`（3 ファイル） |
| 削除 | `static/css/` 以下の全ファイル（20 ファイル） |

---

## Task 1: パッケージインストール・settings.py・urls.py の更新

**Files:**
- Modify: `requirements.txt`
- Modify: `journalog_project/settings.py`
- Modify: `journalog_project/urls.py`

- [ ] **Step 1: パッケージをインストール**

```bash
pip install django-tailwind==3.8.0 django-browser-reload==1.17.0
pip freeze > requirements.txt
```

- [ ] **Step 2: settings.py の INSTALLED_APPS を更新**

```python
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
```

- [ ] **Step 3: settings.py 末尾に Tailwind 設定を追加**

```python
TAILWIND_APP_NAME = 'theme'
INTERNAL_IPS = ['127.0.0.1']
```

- [ ] **Step 4: settings.py の MIDDLEWARE を更新**

```python
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
```

- [ ] **Step 5: urls.py に browser-reload URL を追加**

```python
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', include('journal.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
]
```

- [ ] **Step 6: Node.js インストール確認**

```bash
node --version
npm --version
```

期待値: バージョン番号が表示される。未インストールの場合は https://nodejs.org からインストール。

- [ ] **Step 7: コミット**

```bash
git add requirements.txt journalog_project/settings.py journalog_project/urls.py
git commit -m "django-tailwind と django-browser-reload をインストール"
```

---

## Task 2: Tailwind テーマの初期化・設定

**Files:**
- Create: `theme/`（自動生成）
- Modify: `theme/static_src/tailwind.config.js`
- Modify: `theme/static_src/src/styles.css`

- [ ] **Step 1: Tailwind テーマアプリを初期化**

```bash
python manage.py tailwind init theme
```

期待値: `theme/` ディレクトリが生成される。

- [ ] **Step 2: npm パッケージをインストール**

```bash
python manage.py tailwind install
```

期待値: `theme/static_src/node_modules/` が生成される（数分かかる場合あり）。

- [ ] **Step 3: tailwind.config.js のコンテンツパスを設定**

`theme/static_src/tailwind.config.js` の `content` を書き換える：

```js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    '../../../templates/**/*.html',
    '../../../**/templates/**/*.html',
    '../../../**/*.js',
    '../../../**/*.py',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

- [ ] **Step 4: styles.css にベーススタイルとコンポーネントクラスを定義**

`theme/static_src/src/styles.css` を以下で全置換する：

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply bg-slate-50 text-slate-700;
  }

  input[type="text"],
  input[type="password"],
  input[type="time"],
  input[type="email"],
  textarea,
  select {
    @apply w-full border border-slate-300 rounded-xl px-3 py-2
           focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500
           focus:outline-none text-slate-700 bg-white transition-colors;
  }
}

@layer components {

  /* カードコンポーネント */
  .journal-card {
    @apply bg-white rounded-2xl shadow-md;
  }
  .card-header {
    @apply flex items-center justify-between px-4 pt-4 pb-2;
  }
  .card-body {
    @apply px-4 pb-4;
  }
  .section-divider {
    @apply border-t border-slate-100 mx-4 my-0;
  }
  .journal-input-card {
    @apply bg-slate-50 rounded-xl px-3 py-2;
  }
  .view-title {
    @apply font-semibold text-base m-0;
  }

  /* リスト・アイテム */
  .item-list {
    @apply space-y-1 list-none p-0 m-0 mt-2;
  }
  .item-row {
    @apply flex items-center gap-3 px-2 py-2 rounded-xl hover:bg-slate-50 transition-colors;
  }
  .item-title {
    @apply flex-1 text-slate-700 text-sm;
  }
  .item-time {
    @apply text-xs text-slate-400;
  }
  .item-actions {
    @apply flex items-center gap-1;
  }
  .empty-state {
    @apply text-center py-8;
  }

  /* ボタン基本 */
  .edit-btn {
    @apply p-1.5 rounded-lg hover:bg-slate-100 transition-colors inline-flex items-center;
  }
  .delete-btn {
    @apply p-1.5 rounded-lg hover:bg-red-50 transition-colors inline-flex items-center;
  }
  .plus-btn {
    @apply p-1.5 rounded-lg transition-colors inline-flex items-center;
  }
  .back-btn {
    @apply text-sm border rounded-xl px-3 py-1 transition-colors;
  }
  .date-nav-btn {
    @apply text-sm border rounded-xl px-4 py-1.5 transition-colors;
  }
  .submit-btn {
    @apply bg-indigo-600 hover:bg-indigo-700 text-white font-medium
           rounded-xl px-8 py-3 transition-colors text-base;
  }

  /* 日付ナビ */
  .journal-date-nav {
    @apply flex items-center justify-between mb-4;
  }
  .journal-divider {
    @apply border-t border-slate-200 my-4;
  }

  /* Todo 完了状態 */
  .is-done .item-title {
    @apply line-through text-slate-400;
  }

  /* カレンダー */
  .calendar-wrapper {
    @apply overflow-x-auto rounded-2xl shadow-md;
  }
  .calendar-cell {
    @apply align-top p-1 h-10 cursor-pointer hover:bg-slate-50 transition-colors;
  }
  .calendar-day {
    @apply text-sm font-medium;
  }
  .other-month .calendar-day { @apply text-slate-300; }
  .today { @apply bg-indigo-50; }
  .today .calendar-day { @apply text-indigo-600 font-bold; }
  .has-journal { @apply bg-emerald-50; }
  .has-journal .calendar-day { @apply text-emerald-700; }
  .weekday-sun, .weekday-sun .calendar-day { @apply text-red-500; }
  .weekday-sat, .weekday-sat .calendar-day { @apply text-blue-500; }
  .calendar-outline { @apply mb-3; }

  /* Goal テーマ */
  .goal-card    { @apply border-l-4 border-emerald-400; }
  .goal-field   { @apply border-l-4 border-emerald-400; }
  .goal-text    { @apply text-emerald-600; }
  .goal-divider { @apply border-emerald-100; }
  .goal-btn     { @apply text-emerald-600 border-emerald-300 hover:bg-emerald-50; }
  .goal-bg      { @apply bg-emerald-50 text-emerald-700; }

  /* Todo テーマ */
  .todo-card    { @apply border-l-4 border-indigo-400; }
  .todo-field   { @apply border-l-4 border-indigo-400; }
  .todo-text    { @apply text-indigo-600; }
  .todo-divider { @apply border-indigo-100; }
  .todo-btn     { @apply text-indigo-600 border-indigo-300 hover:bg-indigo-50; }
  .todo-bg      { @apply bg-indigo-50 text-indigo-700; }

  /* Schedule テーマ */
  .schedule-card    { @apply border-l-4 border-violet-400; }
  .schedule-field   { @apply border-l-4 border-violet-400; }
  .schedule-text    { @apply text-violet-600; }
  .schedule-divider { @apply border-violet-100; }
  .schedule-btn     { @apply text-violet-600 border-violet-300 hover:bg-violet-50; }
  .schedule-bg      { @apply bg-violet-50 text-violet-700; }

  /* Reflection テーマ */
  .reflection-card    { @apply border-l-4 border-amber-400; }
  .reflection-field   { @apply border-l-4 border-amber-400; }
  .reflection-text    { @apply text-amber-600; }
  .reflection-divider { @apply border-amber-100; }
  .reflection-btn     { @apply text-amber-600 border-amber-300 hover:bg-amber-50; }
  .reflection-bg      { @apply bg-amber-50 text-amber-700; }
}
```

- [ ] **Step 5: 開発サーバーとビルドウォッチャーを起動して確認**

ターミナル 1（Tailwind ウォッチ）:
```bash
python manage.py tailwind start
```

ターミナル 2（Django サーバー）:
```bash
python manage.py runserver
```

期待値: `theme/static/css/dist/styles.css` が生成される。エラーなし。

- [ ] **Step 6: コミット**

```bash
git add theme/ journalog_project/
git commit -m "Tailwind テーマアプリを初期化・コンポーネントクラスを定義"
```

---

## Task 3: base.html の移行

**Files:**
- Modify: `templates/base.html`

- [ ] **Step 1: base.html を全置換**

```html
{% load static %}
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="ja">

<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JournaLog - {% block title %}{% endblock %}</title>
  <link rel="shortcut icon" href="{% static 'img/favicon.ico' %}" type="image/x-icon">
  {% tailwind_css %}
  {% block extra_css %}{% endblock %}
</head>

<body class="bg-slate-50 text-slate-700 {% block body_class %}{% endblock %}">

  <header>
    <nav class="sticky top-0 z-50 backdrop-blur-sm bg-white/90 border-b border-slate-200 shadow-sm">
      <div class="max-w-4xl mx-auto px-4 h-14 flex items-center justify-between">

        <div class="flex items-center gap-3">
          <a class="font-bold text-lg text-indigo-600 hover:text-indigo-700 transition-colors"
             href="{% url 'journal:home' %}">JournaLog</a>
          <a href="{% url 'journal:home' %}"
             class="text-sm text-slate-600 border border-slate-300 rounded-lg px-3 py-1
                    hover:bg-slate-100 transition-colors">Home</a>
          {% block back_journalover %}{% endblock %}
        </div>

        <div x-data="{ open: false }" class="relative">
          <button @click="open = !open"
                  @keydown.escape.window="open = false"
                  class="p-2 rounded-lg hover:bg-slate-100 transition-colors"
                  aria-label="アカウントメニュー">
            <img src="{% static 'img/menu-btn.svg' %}" alt="メニュー" class="w-6 h-6">
          </button>
          <div x-show="open"
               @click.away="open = false"
               x-transition:enter="transition ease-out duration-100"
               x-transition:enter-start="opacity-0 scale-95"
               x-transition:enter-end="opacity-100 scale-100"
               x-transition:leave="transition ease-in duration-75"
               x-transition:leave-start="opacity-100 scale-100"
               x-transition:leave-end="opacity-0 scale-95"
               class="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-lg
                      border border-slate-100 p-3 z-50"
               style="display: none;">
            <div class="mb-3">
              <div class="text-xs text-slate-400">ログイン中</div>
              <div class="font-semibold text-slate-700">{{ user.username }}</div>
            </div>
            <hr class="border-slate-100 mb-3">
            <form method="post" action="{% url 'accounts:logout' %}">
              {% csrf_token %}
              <button class="w-full text-sm text-red-500 border border-red-300 rounded-xl
                             px-3 py-1.5 hover:bg-red-50 transition-colors" type="submit">
                ログアウト
              </button>
            </form>
          </div>
        </div>

      </div>
    </nav>
  </header>

  <main class="max-w-4xl mx-auto px-4 py-4 md:py-6">
    {% block content %}{% endblock %}
  </main>

  <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
  {% load django_browser_reload %}
  {% django_browser_reload_script %}
  <script src="{% static 'js/page_transition.js' %}"></script>
  {% block extra_js %}{% endblock %}
  <form style="display:none;">{% csrf_token %}</form>
</body>
</html>
```

- [ ] **Step 2: ブラウザで動作確認**

`http://127.0.0.1:8000/` にアクセスし確認：
- ナビバーが正しく表示される
- ハンバーガーアイコンをクリックするとドロップダウンが開閉する
- ドロップダウン外クリック・Escape キーで閉じる
- DevTools Network タブで Bootstrap CDN への 404 がないこと

- [ ] **Step 3: コミット**

```bash
git add templates/base.html
git commit -m "base.html を Tailwind + Alpine.js に移行"
```

---

## Task 4: login.html の移行

**Files:**
- Modify: `accounts/templates/registration/login.html`

- [ ] **Step 1: login.html を全置換**

```html
{% load static %}
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JournaLog - ログイン</title>
  <link rel="shortcut icon" href="{% static 'img/favicon.ico' %}" type="image/x-icon">
  {% tailwind_css %}
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center px-4">

  <div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-8">
    <h2 class="text-xl font-bold text-slate-800 mb-6">ログイン</h2>
    <form method="post">
      {% csrf_token %}
      <div class="mb-4">
        <label class="block text-sm font-medium text-slate-600 mb-1">ユーザーネーム</label>
        {{ form.username }}
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium text-slate-600 mb-1">パスワード</label>
        {{ form.password }}
      </div>
      <button type="submit"
              class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium
                     rounded-xl px-4 py-2.5 transition-colors">
        ログイン
      </button>
    </form>
    <div class="border-t border-slate-100 my-6"></div>
    <p class="text-sm text-slate-500 text-center mb-3">アカウントをお持ちでない方</p>
    <a href="{% url 'accounts:signup' %}"
       class="block w-full text-center text-sm text-indigo-600 border border-indigo-300
              rounded-xl px-4 py-2.5 hover:bg-indigo-50 transition-colors">
      新規登録
    </a>
  </div>

  {% load django_browser_reload %}
  {% django_browser_reload_script %}
</body>
</html>
```

- [ ] **Step 2: `http://127.0.0.1:8000/accounts/login/` を確認**

- カード中央揃えレイアウト
- 入力フォーカス時に indigo のリングが出る
- ログインが正常に動作する

- [ ] **Step 3: コミット**

```bash
git add accounts/templates/registration/login.html
git commit -m "login.html を Tailwind に移行"
```

---

## Task 5: signup.html の移行

**Files:**
- Modify: `accounts/templates/accounts/signup.html`

- [ ] **Step 1: signup.html を全置換**

```html
{% load static %}
{% load tailwind_tags %}
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JournaLog - サインアップ</title>
  <link rel="shortcut icon" href="{% static 'img/favicon.ico' %}" type="image/x-icon">
  {% tailwind_css %}
</head>
<body class="bg-slate-50 min-h-screen flex items-center justify-center px-4">

  <div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-8">
    <h2 class="text-xl font-bold text-slate-800 mb-2">サインアップ</h2>
    <p class="text-sm text-slate-500 mb-6">アカウントを作成して JournaLog を始めよう!</p>

    <form method="post">
      {% csrf_token %}
      {% if form.non_field_errors %}
      <div class="mb-4 text-sm text-red-600 bg-red-50 rounded-xl px-3 py-2">
        {{ form.non_field_errors }}
      </div>
      {% endif %}
      <div class="mb-4">
        <label class="block text-sm font-medium text-slate-600 mb-1">ユーザーネーム</label>
        {{ form.username }}
        {% if form.username.errors %}
        <p class="mt-1 text-xs text-red-500">{{ form.username.errors|join:", " }}</p>
        {% endif %}
      </div>
      <div class="mb-4">
        <label class="block text-sm font-medium text-slate-600 mb-1">パスワード</label>
        {{ form.password1 }}
        {% if form.password1.errors %}
        <p class="mt-1 text-xs text-red-500">{{ form.password1.errors|join:", " }}</p>
        {% endif %}
      </div>
      <div class="mb-6">
        <label class="block text-sm font-medium text-slate-600 mb-1">パスワード（確認）</label>
        {{ form.password2 }}
        {% if form.password2.errors %}
        <p class="mt-1 text-xs text-red-500">{{ form.password2.errors|join:", " }}</p>
        {% endif %}
      </div>
      <button type="submit"
              class="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-medium
                     rounded-xl px-4 py-2.5 transition-colors">
        アカウントを作成
      </button>
    </form>
    <div class="border-t border-slate-100 my-6"></div>
    <p class="text-sm text-slate-500 text-center mb-3">すでにアカウントをお持ちの方</p>
    <a href="{% url 'accounts:login' %}"
       class="block w-full text-center text-sm text-indigo-600 border border-indigo-300
              rounded-xl px-4 py-2.5 hover:bg-indigo-50 transition-colors">
      ログイン
    </a>
  </div>

  {% load django_browser_reload %}
  {% django_browser_reload_script %}
</body>
</html>
```

- [ ] **Step 2: `http://127.0.0.1:8000/accounts/signup/` を確認**

- バリデーションエラー（空送信）が赤文字で表示される
- アカウント作成が正常に動作する

- [ ] **Step 3: コミット**

```bash
git add accounts/templates/accounts/signup.html
git commit -m "signup.html を Tailwind に移行"
```

---

## Task 6: home.html の移行

**Files:**
- Modify: `journal/templates/journal/home.html`

- [ ] **Step 1: home.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}ホーム{% endblock %}

{% block content %}
<div>

  <div class="flex flex-col md:flex-row md:items-center justify-between mb-4 gap-2">
    <h5 class="font-semibold text-slate-700 m-0">{{ user.username }} さんの記録</h5>
    <div class="flex rounded-xl overflow-hidden border border-slate-200 w-fit">
      <a href="?view=month"
         class="px-4 py-1.5 text-sm transition-colors
                {% if view_mode == 'month' %}bg-indigo-600 text-white{% else %}text-slate-600 hover:bg-slate-100{% endif %}">
        月表示
      </a>
      <a href="?view=week"
         class="px-4 py-1.5 text-sm transition-colors border-l border-slate-200
                {% if view_mode == 'week' %}bg-indigo-600 text-white{% else %}text-slate-600 hover:bg-slate-100{% endif %}">
        週表示
      </a>
    </div>
  </div>

  {% if view_mode == "month" %}

  <div class="calendar-outline">
    <form method="get">
      <input type="hidden" name="view" value="month">
      <div class="flex gap-2">
        <select name="year"
                class="border border-slate-300 rounded-xl px-3 py-1.5 text-sm w-auto
                       focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                onchange="this.form.submit();">
          {% for y in years %}
          <option value="{{ y }}" {% if y == year %}selected{% endif %}>{{ y }}年</option>
          {% endfor %}
        </select>
        <select name="month"
                class="border border-slate-300 rounded-xl px-3 py-1.5 text-sm w-auto
                       focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                onchange="this.form.submit();">
          {% for m in months %}
          <option value="{{ m }}" {% if m == month %}selected{% endif %}>{{ m }}月</option>
          {% endfor %}
        </select>
      </div>
    </form>
  </div>

  <div class="calendar-wrapper">
    <table class="w-full border-collapse bg-white text-center text-sm">
      <thead class="bg-slate-50">
        <tr>
          <th class="weekday-sun py-2 font-medium text-xs">日</th>
          <th class="py-2 font-medium text-xs text-slate-600">月</th>
          <th class="py-2 font-medium text-xs text-slate-600">火</th>
          <th class="py-2 font-medium text-xs text-slate-600">水</th>
          <th class="py-2 font-medium text-xs text-slate-600">木</th>
          <th class="py-2 font-medium text-xs text-slate-600">金</th>
          <th class="weekday-sat py-2 font-medium text-xs">土</th>
        </tr>
      </thead>
      <tbody>
        {% for week in cal_data %}
        <tr class="border-t border-slate-100">
          {% for d in week %}
          <td class="calendar-cell
                     {% if d.is_other_month %}other-month{% endif %}
                     {% if d.is_today %}today{% endif %}
                     {% if d.has_journal %}has-journal{% endif %}">
            {% if d.is_other_month %}
            <span class="calendar-day text-slate-300">{{ d.day.day }}</span>
            {% else %}
            <a href="{% url 'journal:journal_router' d.day.year d.day.month d.day.day %}">
              <span class="calendar-day">{{ d.day.day }}</span>
            </a>
            {% endif %}
          </td>
          {% endfor %}
        </tr>
        {% endfor %}
      </tbody>
    </table>
  </div>

  {% else %}

  <div class="flex items-center justify-between mb-3">
    <a href="?view=week&week_start={{ prev_week|date:'Y-m-d' }}"
       class="text-sm text-slate-600 border border-slate-300 rounded-xl px-3 py-1.5
              hover:bg-slate-100 transition-colors">← 前の週</a>
    <div class="text-center text-sm text-slate-600">
      {{ week_start|date:"Y年n月j日" }} 〜 {{ week_end|date:"n月j日" }}
    </div>
    <a href="?view=week&week_start={{ next_week|date:'Y-m-d' }}"
       class="text-sm text-slate-600 border border-slate-300 rounded-xl px-3 py-1.5
              hover:bg-slate-100 transition-colors">次の週 →</a>
  </div>

  <div class="text-center mb-4">
    <a href="?view=week"
       class="text-sm text-indigo-600 border border-indigo-300 rounded-xl px-4 py-1.5
              hover:bg-indigo-50 transition-colors">今週に戻る</a>
  </div>

  <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
    {% for d in week_data %}
    <a href="{% url 'journal:journal_router' d.day.year d.day.month d.day.day %}"
       class="text-decoration-none">
      <div class="bg-white rounded-2xl shadow-md hover:shadow-lg transition-shadow p-3 text-center
                  {% if d.is_today %}ring-2 ring-indigo-400{% endif %}">
        <div class="text-xs text-slate-400 mb-1">{{ d.day|date:"D" }}</div>
        <div class="font-bold text-slate-700 text-lg">{{ d.day|date:"j" }}</div>
        {% if d.has_journal %}
        <span class="inline-block mt-2 bg-emerald-100 text-emerald-700 rounded-full
                     text-xs px-2 py-0.5 font-medium">記録あり</span>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>

  {% endif %}
</div>
{% endblock %}
```

- [ ] **Step 2: `http://127.0.0.1:8000/` を確認**

- 月表示・週表示の切り替えが動作する
- 年月セレクタが動作する
- 週カレンダーのカードにホバー時に影が強くなる
- 「記録あり」バッジが表示される

- [ ] **Step 3: コミット**

```bash
git add journal/templates/journal/home.html
git commit -m "home.html（カレンダー）を Tailwind に移行"
```

---

## Task 7: journal_init.html の移行

**Files:**
- Modify: `journal/templates/journal/journal_init.html`

- [ ] **Step 1: journal_init.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Journal作成{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">

  <header class="mb-4">
    <div class="journal-date-nav">
      <a href="{% url 'journal:journal_router' prev_day.year prev_day.month prev_day.day %}"
         class="text-sm text-slate-500 hover:text-slate-700 transition-colors">← 前日</a>
      <h3 class="text-base font-semibold text-slate-700">{{ journal_date|date:"Y年n月j日" }}</h3>
      <a href="{% url 'journal:journal_router' next_day.year next_day.month next_day.day %}"
         class="text-sm text-slate-500 hover:text-slate-700 transition-colors">翌日 →</a>
    </div>
    <p class="text-sm text-slate-400 text-center">ジャーナルの記録を作成します</p>
  </header>

  <div class="journal-divider"></div>

  <section class="my-4 text-center">
    <p class="text-slate-600 mb-1">まずは今日のゴールとやることを決めましょう。</p>
    <p class="text-sm text-slate-400">細かい計画や振り返りはあとから追加できます。</p>
  </section>

  <div class="journal-divider"></div>

  <form method="post">
    {% csrf_token %}

    <section class="journal-card goal-field mb-4">
      <div class="card-header">
        <h5 class="goal-text view-title">今日のGoal作成</h5>
        <button type="button" id="add-goal" class="plus-btn goal-btn">
          <img src="{% static 'img/plus-icon.svg' %}" alt="Goal追加" class="w-5 h-5">
        </button>
      </div>
      <div class="card-body">
        <hr class="section-divider goal-divider mb-3">
        <div id="goal-formset" class="space-y-2">
          {{ goal_formset.management_form }}
          {% for form in goal_formset %}
          <div class="goal-form journal-input-card flex items-center gap-2">
            {{ form.title }}
            {{ form.DELETE }}
            <button type="button" class="delete-btn goal-btn shrink-0 remove-form">
              <img src="{% static 'img/close-icon.svg' %}" alt="Goal削除" class="w-4 h-4">
            </button>
          </div>
          {% endfor %}
        </div>
      </div>
    </section>

    <section class="journal-card todo-field mb-4">
      <div class="card-header">
        <h5 class="todo-text view-title">今日のTodo作成</h5>
        <button type="button" id="add-todo" class="plus-btn todo-btn">
          <img src="{% static 'img/plus-icon.svg' %}" alt="Todo追加" class="w-5 h-5">
        </button>
      </div>
      <div class="card-body">
        <hr class="section-divider todo-divider mb-3">
        <div id="todo-formset" class="space-y-2">
          {{ todo_formset.management_form }}
          {% for form in todo_formset %}
          <div class="todo-form journal-input-card flex items-center gap-2">
            {{ form.title }}
            {{ form.DELETE }}
            <button type="button" class="delete-btn todo-btn shrink-0 remove-form">
              <img src="{% static 'img/close-icon.svg' %}" alt="Todo削除" class="w-4 h-4">
            </button>
          </div>
          {% endfor %}
        </div>
      </div>
    </section>

    <div id="goal-empty-form" class="hidden">
      <div class="goal-form journal-input-card flex items-center gap-2">
        <input type="text" name="goal-__prefix__-title" id="id_goal-__prefix__-title"
               placeholder="目標内容">
        <input type="hidden" name="goal-__prefix__-DELETE" id="id_goal-__prefix__-DELETE">
        <button type="button" class="delete-btn goal-btn shrink-0 remove-form">
          <img src="{% static 'img/close-icon.svg' %}" alt="Goal削除" class="w-4 h-4">
        </button>
      </div>
    </div>

    <div id="todo-empty-form" class="hidden">
      <div class="todo-form journal-input-card flex items-center gap-2">
        <input type="text" name="todo-__prefix__-title" id="id_todo-__prefix__-title"
               placeholder="Todo内容">
        <input type="hidden" name="todo-__prefix__-DELETE" id="id_todo-__prefix__-DELETE">
        <button type="button" class="delete-btn todo-btn shrink-0 remove-form">
          <img src="{% static 'img/close-icon.svg' %}" alt="Todo削除" class="w-4 h-4">
        </button>
      </div>
    </div>

    <div class="text-center mt-6">
      <button type="submit" class="submit-btn">今日の目標を作成</button>
    </div>
  </form>
</div>

{% block extra_js %}
<script src="{% static 'js/journal_init.js' %}"></script>
{% endblock %}
{% endblock %}
```

- [ ] **Step 2: journal_init ページを確認**

任意の日付の init ページにアクセスし確認：
- Goal・Todo カードが emerald・indigo でカラー区分される
- 「+」ボタンで入力行が追加される（JS 動作）
- 削除ボタンで行が消える
- フォーム送信が成功する

- [ ] **Step 3: コミット**

```bash
git add journal/templates/journal/journal_init.html
git commit -m "journal_init.html を Tailwind に移行"
```

---

## Task 8: journal_over.html の移行

**Files:**
- Modify: `journal/templates/journal/journal_over.html`

- [ ] **Step 1: journal_over.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}Journal記録{% endblock %}

{% block extra_js %}
<script src="{% static 'js/todo_toggle.js' %}"></script>
<script src="{% static 'js/journal_over_animation.js' %}"></script>
{% endblock %}

{% block content %}

<div class="journal-date-nav">
  <a href="{% url 'journal:journal_router' prev_day.year prev_day.month prev_day.day %}"
     class="date-nav-btn todo-btn">← 前日</a>
  <h4 class="text-base font-semibold text-slate-700">
    {{ journal_date|date:"Y年n月j日" }} のジャーナル
  </h4>
  <a href="{% url 'journal:journal_router' next_day.year next_day.month next_day.day %}"
     class="date-nav-btn todo-btn">翌日 →</a>
</div>

<div class="space-y-4">

  <section class="journal-card goal-field">
    <div class="card-header">
      <h5 class="goal-text view-title">Goal一覧</h5>
      {% if goals %}
      <a href="{% url 'journal:create_goal' journal_date.year journal_date.month journal_date.day %}"
         class="plus-btn goal-btn">
        <img src="{% static 'img/plus-icon.svg' %}" alt="Goal追加" class="w-5 h-5">
      </a>
      {% endif %}
    </div>
    <div class="card-body">
      <hr class="section-divider goal-divider mb-2">
      {% if goals %}
      <ul class="item-list">
        {% for goal in goals %}
        <li class="item-row">
          <span class="item-title">{{ goal.title }}</span>
          <div class="item-actions">
            <a href="{% url 'journal:update_goal' goal.pk %}" class="edit-btn goal-btn">
              <img src="{% static 'img/edit-icon.svg' %}" alt="Goal編集" class="w-4 h-4">
            </a>
            <a href="{% url 'journal:delete_goal' goal.pk %}" class="delete-btn goal-btn">
              <img src="{% static 'img/delete-icon.svg' %}" alt="Goal削除" class="w-4 h-4">
            </a>
          </div>
        </li>
        {% endfor %}
      </ul>
      {% else %}
      <div class="empty-state">
        <a href="{% url 'journal:create_goal' journal_date.year journal_date.month journal_date.day %}"
           class="inline-block goal-bg goal-btn px-6 py-2 rounded-xl text-sm font-medium">
          今日のGoalを記録しましょう
        </a>
      </div>
      {% endif %}
    </div>
  </section>

  <section class="journal-card todo-field">
    <div class="card-header">
      <h5 class="todo-text view-title">Todo一覧</h5>
      {% if todos %}
      <a href="{% url 'journal:create_todo' journal_date.year journal_date.month journal_date.day %}"
         class="plus-btn todo-btn">
        <img src="{% static 'img/plus-icon.svg' %}" alt="Todo追加" class="w-5 h-5">
      </a>
      {% endif %}
    </div>
    <div class="card-body">
      <hr class="section-divider todo-divider mb-2">
      {% if todos %}
      <ul class="item-list">
        {% for todo in todos %}
        <li class="item-row {% if todo.is_done %}is-done{% endif %}">
          <input type="checkbox"
                 class="w-4 h-4 rounded accent-indigo-500 cursor-pointer shrink-0"
                 data-todo-id="{{ todo.id }}"
                 {% if todo.is_done %}checked{% endif %}>
          <span class="item-title">{{ todo.title }}</span>
          <div class="item-actions">
            <a href="{% url 'journal:update_todo' todo.pk %}" class="edit-btn todo-btn">
              <img src="{% static 'img/edit-icon.svg' %}" alt="Todo編集" class="w-4 h-4">
            </a>
            <a href="{% url 'journal:delete_todo' todo.pk %}" class="delete-btn todo-btn">
              <img src="{% static 'img/delete-icon.svg' %}" alt="Todo削除" class="w-4 h-4">
            </a>
          </div>
        </li>
        {% endfor %}
      </ul>
      {% else %}
      <div class="empty-state">
        <a href="{% url 'journal:create_todo' journal_date.year journal_date.month journal_date.day %}"
           class="inline-block todo-bg todo-btn px-6 py-2 rounded-xl text-sm font-medium">
          今日のTodoを記録しましょう
        </a>
      </div>
      {% endif %}
    </div>
  </section>

  <section class="journal-card schedule-field">
    <div class="card-header">
      <h5 class="schedule-text view-title">スケジュール一覧</h5>
      {% if schedules %}
      <a href="{% url 'journal:create_schedule' journal_date.year journal_date.month journal_date.day %}"
         class="plus-btn schedule-btn">
        <img src="{% static 'img/plus-icon.svg' %}" alt="スケジュール追加" class="w-5 h-5">
      </a>
      {% endif %}
    </div>
    <div class="card-body">
      <hr class="section-divider schedule-divider mb-2">
      {% if schedules %}
      <ul class="item-list">
        {% for schedule in schedules %}
        <li class="item-row">
          <span class="item-title">{{ schedule.title }}</span>
          {% if schedule.start_time or schedule.end_time %}
          <span class="item-time">
            {% if schedule.start_time %}{{ schedule.start_time|time:"H:i" }}{% endif %}
            {% if schedule.start_time and schedule.end_time %}~{% endif %}
            {% if schedule.end_time %}{{ schedule.end_time|time:"H:i" }}{% endif %}
          </span>
          {% endif %}
          <div class="item-actions">
            <a href="{% url 'journal:update_schedule' schedule.pk %}" class="edit-btn schedule-btn">
              <img src="{% static 'img/edit-icon.svg' %}" alt="Schedule編集" class="w-4 h-4">
            </a>
            <a href="{% url 'journal:delete_schedule' schedule.pk %}" class="delete-btn schedule-btn">
              <img src="{% static 'img/delete-icon.svg' %}" alt="Schedule削除" class="w-4 h-4">
            </a>
          </div>
        </li>
        {% endfor %}
      </ul>
      {% else %}
      <div class="empty-state">
        <a href="{% url 'journal:create_schedule' journal_date.year journal_date.month journal_date.day %}"
           class="inline-block schedule-bg schedule-btn px-6 py-2 rounded-xl text-sm font-medium">
          スケジュールを記録する
        </a>
      </div>
      {% endif %}
    </div>
  </section>

  <section class="journal-card reflection-field">
    <div class="card-header">
      <h5 class="reflection-text view-title">振り返り</h5>
      {% if reflection %}
      <a href="{% url 'journal:update_reflection' reflection.pk %}" class="edit-btn reflection-btn">
        <img src="{% static 'img/edit-icon.svg' %}" alt="振り返り編集" class="w-4 h-4">
      </a>
      {% endif %}
    </div>
    <div class="card-body">
      <hr class="section-divider reflection-divider mb-2">
      {% if reflection %}
      <p class="text-slate-600 text-sm leading-relaxed">{{ reflection.content }}</p>
      {% else %}
      <div class="empty-state">
        <a href="{% url 'journal:create_reflection' journal_date.year journal_date.month journal_date.day %}"
           class="inline-block reflection-bg reflection-btn px-6 py-2 rounded-xl text-sm font-medium">
          今日の1日を振り返る
        </a>
      </div>
      {% endif %}
    </div>
  </section>

</div>
{% endblock %}
```

- [ ] **Step 2: journal_over ページを確認**

- 4 セクション（Goal・Todo・Schedule・Reflection）がカラー区分される
- Todo チェックボックスで打ち消し線が切り替わる
- 編集・削除リンクが機能する
- 空の場合は CTA ボタンが表示される

- [ ] **Step 3: コミット**

```bash
git add journal/templates/journal/journal_over.html
git commit -m "journal_over.html を Tailwind に移行"
```

---

## Task 9: create_base.html の移行

**Files:**
- Modify: `templates/common/create_base.html`

- [ ] **Step 1: create_base.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block back_journalover %}
<a href="{% url 'journal:journal_over' journal.date.year journal.date.month journal.date.day %}"
   class="text-sm text-slate-600 border border-slate-300 rounded-lg px-3 py-1
          hover:bg-slate-100 transition-colors">
  今日のジャーナルに戻る
</a>
{% endblock %}

{% block content %}
<div class="max-w-2xl mx-auto">
  <section class="journal-card {{ feature }}-card" data-feature="{{ feature }}">
    <div class="card-header">
      <h5 class="{{ feature }}-text view-title">{% block section_title %}{% endblock %}</h5>
      {% if allow_multiple %}
      <button type="button" class="plus-btn {{ feature }}-btn" data-add-btn>
        <img src="{% static 'img/plus-icon.svg' %}" alt="追加" class="w-5 h-5">
      </button>
      {% endif %}
    </div>
    <div class="card-body">
      <hr class="section-divider {{ feature }}-divider mb-3">
      <form method="post">
        {% csrf_token %}
        <div data-formset class="space-y-2">
          {{ formset.management_form }}
          {% for form in formset %}
          <div class="journal-input-card flex items-center gap-2">
            {% block form_fields %}{% endblock %}
            {% if allow_multiple %}
            <button type="button" class="remove-form delete-btn shrink-0">
              <img src="{% static 'img/delete-icon.svg' %}" alt="削除" class="w-4 h-4">
            </button>
            {% endif %}
          </div>
          {% endfor %}
        </div>
        <template data-empty-form>
          <div class="journal-input-card flex items-center gap-2">
            {% block empty_form_fields %}{% endblock %}
            {% if allow_multiple %}
            <button type="button" class="remove-form delete-btn shrink-0">
              <img src="{% static 'img/delete-icon.svg' %}" alt="削除" class="w-4 h-4">
            </button>
            {% endif %}
          </div>
        </template>
        <div class="text-center mt-4">
          <button type="submit" class="submit-btn">{% block submit_label %}{% endblock %}</button>
        </div>
      </form>
    </div>
  </section>
</div>

{% block extra_js %}
<script src="{% static 'js/create_formset.js' %}" defer></script>
{% endblock %}
{% endblock %}
```

- [ ] **Step 2: Goal 作成ページを確認**

journal_over の「今日のGoalを記録しましょう」から作成ページに遷移し確認：
- ナビに「今日のジャーナルに戻る」ボタンが出る
- カードがフィーチャーカラーで表示される
- 複数入力の追加・削除が機能する

- [ ] **Step 3: コミット**

```bash
git add templates/common/create_base.html
git commit -m "create_base.html を Tailwind に移行"
```

---

## Task 10: update_base.html の移行

**Files:**
- Modify: `templates/common/update_base.html`

- [ ] **Step 1: update_base.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="max-w-2xl mx-auto">
  <section class="journal-card {{ feature }}-card" data-feature="{{ feature }}">
    <div class="card-header">
      <h5 class="{{ feature }}-text view-title">{% block section_title %}{% endblock %}</h5>
      <a href="{{ cancel_url }}" class="back-btn {{ feature }}-btn {{ feature }}-text">
        キャンセル
      </a>
    </div>
    <div class="card-body">
      <hr class="section-divider {{ feature }}-divider mb-3">
      <form method="post">
        {% csrf_token %}
        {% block form_fields %}{% endblock %}
        <div class="text-center mt-4">
          <button type="submit" class="submit-btn">編集を完了</button>
        </div>
      </form>
    </div>
  </section>
</div>
{% endblock %}
```

- [ ] **Step 2: Goal 編集ページを確認**

任意の Goal の編集ページにアクセスし確認：
- フィーチャーカラーが適用される
- 「キャンセル」で前のページに戻れる
- フォーム送信が成功する

- [ ] **Step 3: コミット**

```bash
git add templates/common/update_base.html
git commit -m "update_base.html を Tailwind に移行"
```

---

## Task 11: delete_base.html の移行

**Files:**
- Modify: `templates/common/delete_base.html`

- [ ] **Step 1: delete_base.html を全置換**

```html
{% extends "base.html" %}
{% load static %}

{% block content %}
<div class="max-w-2xl mx-auto">
  <section class="journal-card {{ feature }}-card" data-feature="{{ feature }}">
    <div class="card-header">
      <h5 class="{{ feature }}-text view-title">{% block section_title %}{% endblock %}</h5>
      <a href="{{ cancel_url|default:'javascript:history.back()' }}"
         class="back-btn {{ feature }}-btn">キャンセル</a>
    </div>
    <div class="card-body">
      <hr class="section-divider {{ feature }}-divider mb-3">
      <p class="text-sm text-slate-500 mb-4">以下の{{ model_label }}の投稿を削除しますか？</p>
      <div class="journal-input-card mb-4">
        {% block delete_object %}{% endblock %}
      </div>
      <form method="post">
        {% csrf_token %}
        <div class="text-center">
          <button type="submit"
                  class="bg-red-500 hover:bg-red-600 text-white font-medium
                         rounded-xl px-8 py-3 transition-colors">
            削除する
          </button>
        </div>
      </form>
    </div>
  </section>
</div>
{% endblock %}
```

- [ ] **Step 2: Goal 削除ページを確認**

任意の Goal の削除ページにアクセスし確認：
- 削除確認カードが表示される
- 「削除する」ボタンが赤く表示される
- 削除が正常に実行される

- [ ] **Step 3: コミット**

```bash
git add templates/common/delete_base.html
git commit -m "delete_base.html を Tailwind に移行"
```

---

## Task 12: 子テンプレートの確認

**Files:**
- Verify: `journal/templates/journal/` 以下の create/update/delete 子テンプレート（11 ファイル）

子テンプレートはレイアウトを親テンプレートに委ねているため変更は最小限。

- [ ] **Step 1: 旧 CSS リンクが残っていないか確認**

```bash
grep -r "css/pages" journal/templates/journal/create_*.html \
    journal/templates/journal/update_*.html \
    journal/templates/journal/delete_*.html 2>/dev/null
```

期待値: 出力なし。出力があった場合は対象ファイルの `{% block extra_css %}` ブロックを削除する。

- [ ] **Step 2: 全 CRUD ページを動作確認**

| 操作 | 確認内容 |
|------|---------|
| Goal 作成・編集・削除 | goal-card (emerald) が適用される |
| Todo 作成・編集・削除 | todo-card (indigo) が適用される |
| Schedule 作成・編集・削除 | schedule-card (violet) が適用される |
| Reflection 作成・編集 | reflection-card (amber) が適用される |

- [ ] **Step 3: コミット（変更があった場合のみ）**

```bash
git add journal/templates/journal/
git commit -m "子テンプレートの旧 CSS 参照を削除"
```

---

## Task 13: 旧 CSS 削除・本番ビルド

**Files:**
- Delete: `static/css/` 以下の全ファイル

- [ ] **Step 1: 全ページの最終確認**

以下を順番に確認する：
- `http://127.0.0.1:8000/accounts/login/`
- `http://127.0.0.1:8000/accounts/signup/`
- `http://127.0.0.1:8000/` （月表示・週表示）
- 任意の日付の journal_init・journal_over・各 CRUD ページ

DevTools Console でエラーなし、Network タブで CSS 404 なしを確認。

- [ ] **Step 2: 旧 CSS ディレクトリを削除**

```bash
rm -rf static/css/
```

- [ ] **Step 3: 削除後に再確認**

```bash
python manage.py runserver
```

`http://127.0.0.1:8000/` でレイアウト崩れなし、Console エラーなしを確認。

- [ ] **Step 4: 本番用 CSS をビルド**

```bash
python manage.py tailwind build
```

期待値: `theme/static/css/dist/styles.css` が minify された状態で生成される。エラーなし。

- [ ] **Step 5: collectstatic を実行**

```bash
python manage.py collectstatic --noinput
```

期待値: `staticfiles/` に Tailwind の CSS が含まれる。エラーなし。

- [ ] **Step 6: 最終コミット**

```bash
git add -A
git commit -m "旧 CSS を削除し Bootstrap→Tailwind 移行を完了"
```

---

## 完了条件チェックリスト

- [ ] Bootstrap CDN リンクがすべてのテンプレートから削除されている
- [ ] `static/css/` 以下が全削除されている
- [ ] 全ページが Tailwind CSS のみでスタイリングされている
- [ ] ナビバードロップダウンが Alpine.js で動作している
- [ ] `python manage.py tailwind build` が成功している
- [ ] `python manage.py collectstatic` が成功している
- [ ] モバイル表示（レスポンシブ）が維持されている