# スライド生成（社内説明資料 #0001）

社内説明スライド（8枚）の生成元。できあがった文書は `docs/` にある。

- 公開URL（Claude Design。閲覧・文字の修正・PNG/PDF書き出し）: https://claude.ai/code/artifact/913a5070-4d04-4c8f-916f-378fbe4a8695
- PDF: [docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.pdf](../../docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.pdf)
- 説明文書: [docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.md](../../docs/20260915_DOC_0001_ALL_社内説明資料（DuskHighway）.md)
- 話す台本: [docs/20260915_DOC_0002_ALL_プレゼンの進め方（DuskHighway）.md](../../docs/20260915_DOC_0002_ALL_プレゼンの進め方（DuskHighway）.md)
- `gen.py` … スライド8枚（`Main.dc.html` = 表紙、`S02`〜）と `canvas.json`、PDF用の `deck.html` を生成し、PDF を `docs/` に書き出す
- `dusk-title.jpg` / `dusk-play.jpg` … `../../screenshots/` の画面写真を縮小したもの（スライド03で使用）。撮り直したら `sips -Z 560 -s format jpeg` で作り直す
- 見た目はアプリ本体（index.html）と同じ配色（宵闇の紺・アンバー・クリーム）と書体（Chakra Petch / JetBrains Mono）
- 構成：表紙 / ねらい / 画面 / 遊び方 / 続ける仕掛け / 技術 / 現状 / 次のステップと費用

## 作り直す

文言は `gen.py` を直す。アプリのフォルダで:

```bash
python3 tools/slides/gen.py
```

```bash
bash docs/manager/generate_docs_json.sh
```
