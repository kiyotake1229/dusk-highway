# プレゼン資料（社内説明・8枚）

- 公開URL（Claude Design。閲覧・文字の修正・PNG/PDF書き出し）: https://claude.ai/code/artifact/913a5070-4d04-4c8f-916f-378fbe4a8695
- PDF: `DuskHighway_社内説明.pdf`（このフォルダ。そのまま配れる）
- 話す台本: [../プレゼンの進め方.md](../プレゼンの進め方.md)
- `gen.py` … スライド8枚（`Main.dc.html` = 表紙、`S02`〜）と `canvas.json`、PDF用の `deck.html`、PDF を生成するスクリプト。文言を直すときはここを編集する
- `dusk-title.jpg` / `dusk-play.jpg` … `../../screenshots/` の画面写真を縮小したもの（スライド03で使用）。撮り直したら `sips -Z 560 -s format jpeg` で作り直す
- 見た目はアプリ本体（index.html）と同じ配色（宵闇の紺・アンバー・クリーム）と書体（Chakra Petch / JetBrains Mono）
- 構成：表紙 / ねらい / 画面 / 遊び方 / 続ける仕掛け / 技術 / 現状 / 次のステップと費用

## 作り直す

アプリのフォルダで次を実行する（Chrome があれば PDF も更新される）。

```bash
python3 資料/プレゼン資料/gen.py
```
