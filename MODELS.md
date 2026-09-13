# 3Dモデルの差し替え手順

## いま入っているもの

**Kenney Car Kit 3.1**（CC0 / 商用可 / クレジット不要）を組み込み済みです。
ライセンス全文は `models/KENNEY-LICENSE.txt` にあります。

| 役割 | モデル |
|---|---|
| 自車 | sedan-sports |
| 対向車 | sedan / suv / van / taxi / truck / police |
| パイロン | cone |

コード生成のモデル（sport / sedan / suv / van の4種）もそのまま残っていて、
`.glb` の読み込みに失敗したときは自動でそちらに戻ります。

## 差し替えの流れ

```bash
node tools/embed-glb.mjs models/car.glb
```

これだけです。`index.html` にモデルが埋め込まれ、自車が入れ替わります。
モデルが外部テクスチャを参照している場合は、画像も自動で探して一緒に埋め込みます。

対向車を追加する場合（何台でも可、順番に使われます）:

```bash
node tools/embed-glb.mjs models/taxi.glb traffic
```

パイロン:

```bash
node tools/embed-glb.mjs models/cone.glb cone
```

確認・取り消し:

```bash
node tools/embed-glb.mjs --list
```

```bash
node tools/embed-glb.mjs --clear
```

差し替え後は必ず動作を見てください。ブラウザのコンソールで `previewCars()` を実行すると、全車種が並んで回転表示されます。

## 守るべき条件

| 項目 | 条件 |
|---|---|
| 形式 | **.glb**（.gltf は複数ファイルに分かれるため不可） |
| サイズ | 1台 **300KB以下**が目安。全部で16MBが上限 |
| ポリゴン数 | 2,000〜8,000 程度 |
| テクスチャ | 512px以下、できればテクスチャ無しの単色マテリアル |
| 圧縮 | **Draco圧縮はオフ**（デコーダを読み込めないため） |
| 向き | 前後どちら向きでも自動補正します。長さも自動で4.45mに揃います |

---

## ルート1：CC0素材を使う（おすすめ・最短）

商用利用可・クレジット不要の素材サイト。

- **Kenney.nl** — https://kenney.nl/assets/car-kit 　今のアートスタイルと相性が良い
- **Quaternius** — https://quaternius.com/ 　車・建物・自然物
- **Poly Pizza** — https://poly.pizza/ 　検索しやすい

ダウンロードした .glb をこのフォルダの `models/` に入れて、上のコマンドを実行するだけです。

## ルート2：AIで生成する

テキストや画像から3Dモデルを作り、.glb で書き出せます。

- **Meshy** — https://www.meshy.ai/ 　無料枠あり。日本語プロンプト可
- **Tripo3D** — https://www.tripo3d.ai/ 　生成が速い

プロンプト例:

```
low poly sports car, flat shaded, simple geometry, no texture, game asset
```

ポリゴン数が多くなりがちなので、書き出し時に「Low poly」「Quad mesh」などの軽量オプションを選んでください。

## ルート3：Blenderで作る・調整する

自由度は最大ですが、時間がかかります。**ルート1か2で取ってきたモデルを微調整する**用途が現実的です。

インストール:

```bash
brew install --cask blender
```

Homebrewが無い場合は https://www.blender.org/download/ から直接どうぞ。

### 書き出し設定

`ファイル > エクスポート > glTF 2.0 (.glb)` を選び、右側のパネルで:

- **形式**: glTF Binary (.glb)
- **含める**: 「選択したオブジェクト」にチェック（不要なカメラ・ライトを出さない）
- **メッシュ > 適用**: モディファイアーを適用する
- **圧縮 (Draco)**: **オフのまま**

### 軽量化のコツ

- モディファイアーの「デシメート」でポリゴンを半分に落とす
- マテリアルはベースカラーだけの単色にする（テクスチャを使わない）
- 内装・エンジンなど、外から見えない部分は削除する

---

## ローカルで動かす

モデルを埋め込むと index.html が大きくなり、ブラウザで直接開けないことがあります。
その場合はローカルサーバ経由で確認してください。

```bash
python3 -m http.server 8765
```

http://localhost:8765/index.html を開きます。

## 車以外を差し替えたい場合

いま対応しているのは **自車・対向車・パイロン** です。
サボテン・岩・デリニエータも差し替えたくなったら言ってください。仕組みを広げます。
