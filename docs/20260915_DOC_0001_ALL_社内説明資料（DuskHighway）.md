# 社内説明資料（Dusk Highway）

- 管理番号: #0001
- 種類: DOC（ドキュメント作成）
- 対象: 全体（ALL）
- 作成日: 2026-09-15
- 関連: #0002（プレゼンの進め方）

## 概要

「Dusk Highway」（スマホ向け3Dエンドレスレース）を岩崎さんに説明するためのスライド（8枚）。ねらい（単一HTMLで3Dが成立するか）、画面、遊び方、続ける仕掛け、技術と素材、現状、iOS化の手順と費用をまとめている。

## 対象ファイル

- `docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.pdf`（配布用）
- `tools/slides/gen.py`（スライドの生成元。文言はここ）
- `tools/slides/Main.dc.html` / `tools/slides/S02〜S08.dc.html` / `tools/slides/canvas.json`（生成物。Claude Design に載せる）
- `tools/slides/deck.html`（PDF 用の生成物）
- `tools/slides/dusk-title.jpg`（スライドの画面写真）
- `tools/slides/dusk-play.jpg`（スライドの画面写真）
- `index.html`（説明対象）
- `manifest.json`（説明対象）
- `sw.js`（説明対象）
- `models/`（説明対象）
- `MODELS.md`（説明対象）
- `screenshots/01-title.png`（説明対象）
- `screenshots/02-play.png`（説明対象）
- `README.md`（アプリの状態・残作業）

## 変更内容

### 1. 資料の置き場所を docs/ に移した

`資料/プレゼン資料/` にあったスライド一式を、project-docs の管理方式に合わせて移した。

- PDF → `docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.pdf`
- 生成元（`gen.py`・`*.dc.html`・`canvas.json`・`deck.html`） → `tools/slides/`
- 話す台本 → `docs/20260915_DOC_0002_ALL_プレゼンの進め方（DuskHighway）.md`（#0002）

### 2. スライドの構成

| No. | 見出し | タイトル |
|---|---|---|
| 01 | 表紙 | Dusk Highway |
| 02 | ねらい | 単一HTMLで、3Dゲームは成立するか |
| 03 | 画面 | 縦持ち・片手で、砂漠のハイウェイを走る |
| 04 | 遊び方 | 触れば分かる、4つのルール |
| 05 | 続ける仕掛け | 「もう1回」を作る6つの要素 |
| 06 | 技術 | 3Dモデルごと、1つのHTMLに入れた |
| 07 | 現状 | Web版は完成。いま触れる |
| 08 | 次のステップ | iOS 化の道と、今日決めたいこと |

### 3. 作り直す方法

`tools/slides/gen.py` の文言を直して、アプリのフォルダで次を実行する。スライド・PDF の両方が更新される。

```bash
python3 tools/slides/gen.py
```

```bash
bash docs/manager/generate_docs_json.sh
```

Claude Design（公開URL）も同じ内容にするときは、生成された `tools/slides/*.dc.html` と `canvas.json` で再公開する。

## 確認URL

| 環境 | URL |
|------|-----|
| ローカル | `index.html` をブラウザで開く |
| 本番（Web版） | https://kiyotake1229.github.io/dusk-highway/ |
| スライド（Claude Design） | https://claude.ai/code/artifact/913a5070-4d04-4c8f-916f-378fbe4a8695 |

## 作業概要と概算費用

最後のスライド「次のステップ」で示した「iOS化から申請まで」の見積もり。

| 項目 | 内容 | 工数 |
|------|------|------|
| 調査 | —（仕様は README.md / MODELS.md にまとまっている） | 0h |
| 実装 | iOS化（Capacitor 構築、アイコンは `icon-1024.png`、触覚を Capacitor Haptics に置き換え） | 4h |
| テスト | 実機検証（初回読み込み15〜20秒の体感、フレームレート、発熱、縦固定の挙動） | 16〜24h |
| 申請準備 | スクリーンショット3サイズ、申請文面の下書き（目安） | 4h |
| 合計 | | 24〜32h（3〜4人日） |

概算費用: 人日単価が未設定のため金額は未記載（工数は上表の合計）

外部費用: Apple Developer Program 年12,800円（全アプリで1契約）。3Dモデルは CC0 のためライセンス料なし
