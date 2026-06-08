# Bootstrap → Tailwind CSS 移行 設計書

**作成日**: 2026-06-08  
**プロジェクト**: JournaLog（Django ジャーナリングアプリ）  
**対象ブランチ**: 移行用ブランチ（main への直接プッシュ禁止）

---

## 1. 目的と背景

JournaLog は現在 Bootstrap 5.3.0（CDN）を使用してスタイリングしている。  
本移行の目的は以下の2点：

1. **Tailwind CSS への完全移行**（Bootstrap の削除）
2. **UIの刷新**：モダン・カード型のデザインへ再構築（SaaS アプリ風）

---

## 2. 技術構成

### 追加

| パッケージ | 用途 |
|-----------|------|
| `django-tailwind` | Tailwind CSS v3 の Django ラッパー（`manage.py tailwind start/build`） |
| Alpine.js（CDN） | Bootstrap JS の代替。ナビバードロップダウンのインタラクションを担当 |
| `django-browser-reload` | 開発中のホットリロード（django-tailwind に付属） |

### 削除

- Bootstrap CSS / JS（CDN リンク × 3箇所: `base.html`, `login.html`, `signup.html`）
- `static/css/` 以下の全カスタム CSS ファイル（20ファイル）

### ファイル構成の変化

```
journalog_project/
├── theme/                    ← django-tailwind が自動生成するアプリ
│   └── static_src/
│       ├── src/
│       │   └── styles.css    ← Tailwind のエントリポイント（@tailwind ディレクティブ）
│       └── package.json
└── static/
    └── css/                  ← 移行完了後に全削除
```

---

## 3. デザインシステム

### カラーパレット

| 役割 | カラー | Tailwind クラス |
|------|--------|----------------|
| プライマリ | インディゴ | `indigo-600` / `indigo-700` |
| 背景 | ライトグレー | `slate-50` |
| カード背景 | ホワイト | `white` |
| テキスト（本文） | ダークグレー | `slate-700` |
| テキスト（補助） | ミドルグレー | `slate-400` |
| 成功・記録あり | エメラルド | `emerald-500` |
| 危険（削除・ログアウト） | レッド | `red-500` |

### コンポーネント方針

**ナビバー**
- `sticky top-0 backdrop-blur-sm bg-white/90 border-b border-slate-200 shadow-sm`
- ドロップダウン: Alpine.js で `x-data="{ open: false }"` / `x-show="open"` を使用

**カード**
- `rounded-2xl shadow-md hover:shadow-lg transition-shadow duration-200`
- 週表示・記録カードに適用

**ボタン（プライマリ）**
- `bg-indigo-600 hover:bg-indigo-700 text-white font-medium rounded-xl px-4 py-2 transition-colors`

**ボタン（セカンダリ）**
- `border border-slate-300 hover:bg-slate-100 text-slate-700 rounded-xl px-4 py-2 transition-colors`

**フォーム入力**
- `w-full border border-slate-300 rounded-xl px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:outline-none`

**バッジ**
- `bg-emerald-100 text-emerald-700 rounded-full text-xs px-2 py-0.5 font-medium`

---

## 4. 移行順序（段階的）

Bootstrap と Tailwind が共存する期間を最小化するため、**外側（共通部分）から内側（個別ページ）** へ進める。

### Phase 1: 環境セットアップ
- `django-tailwind` インストール（`pip install django-tailwind`）
- `python manage.py tailwind init theme` で theme アプリ生成
- `settings.py` に `theme` / `django_browser_reload` を追加
- Alpine.js を `base.html` の `<script>` に追加
- `python manage.py tailwind install` で npm パッケージをインストール
- **Bootstrap はこの時点ではまだ残す**

### Phase 2: `base.html` の移行
- Bootstrap の CDN リンクを削除
- Tailwind ビルド済み CSS へ切り替え
- ナビバーを Alpine.js + Tailwind で再実装
- 全ページの共通レイアウト（sticky header, main container）を刷新

### Phase 3: 認証ページ（ログイン・サインアップ）
- `login.html` / `signup.html` は Bootstrap を直接読み込んでいるため個別対応
- ナビバー不要なため `base.html` は継承せず、Tailwind を直接読み込む独立テンプレートとして維持
- フォームデザインを刷新（カード型レイアウト、インディゴ系ボタン）

### Phase 4: ホームページ（カレンダー）
- `home.html` の月表示・週表示カレンダーを Tailwind で再構築
- カード型の週表示に shadow / rounded を適用

### Phase 5: ジャーナルページ
- `journal_init.html` / `journal_over.html` を移行

### Phase 6: 共通フォームページ
- `templates/common/create_base.html` / `update_base.html` / `delete_base.html`
- `journal/templates/journal/` 以下の create / update / delete テンプレート（10ファイル）

### Phase 7: 旧 CSS 削除・最終確認
- `static/css/` 以下を全削除
- `python manage.py tailwind build` で本番用 CSS を生成
- `python manage.py collectstatic` で静的ファイルを収集

---

## 5. 既知の考慮事項

| 項目 | 対応方針 |
|------|---------|
| Bootstrap JS（dropdown） | Alpine.js に置き換え |
| `widget_tweaks` | 継続使用（フォームフィールドのレンダリングに必要） |
| `whitenoise` | 変更なし（`collectstatic` + `CompressedManifestStaticFilesStorage` をそのまま使用） |
| 既存の `static/js/*.js` | 移行とは独立。Bootstrap 依存はないため変更不要 |
| 認証ページ（`login.html` / `signup.html`） | `base.html` を継承していないため個別対応が必要 |

---

## 6. 完了条件

- [ ] Bootstrap の CDN リンクがすべてのテンプレートから削除されている
- [ ] `static/css/` 以下のカスタム CSS が全削除されている
- [ ] 全ページが Tailwind CSS のみでスタイリングされている
- [ ] ナビバードロップダウンが Alpine.js で動作している
- [ ] `python manage.py tailwind build` が成功し、`collectstatic` が通る
- [ ] モバイル表示（レスポンシブ）が維持されている
