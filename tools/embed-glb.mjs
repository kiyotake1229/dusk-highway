#!/usr/bin/env node
/*
 * .glb を index.html に埋め込むツール
 *
 *   node tools/embed-glb.mjs models/car.glb          自車として埋め込む
 *   node tools/embed-glb.mjs models/taxi.glb traffic 対向車として追加（複数可）
 *   node tools/embed-glb.mjs --list                  埋め込み済みを表示
 *   node tools/embed-glb.mjs --clear                 全部消す
 *
 * Artifact は外部ファイルを読めないため、モデルは base64 で HTML に直接埋め込む。
 * base64 化するとファイルサイズは約 1.33 倍になる。ページ全体で 16MB が上限。
 */
import fs from "node:fs";
import path from "node:path";

const START = "/* GLB_DATA_START */";
const END = "/* GLB_DATA_END */";
const HTML = path.resolve(process.cwd(), "index.html");

const args = process.argv.slice(2);
if (!args.length || args[0] === "-h" || args[0] === "--help") {
  console.log(fs.readFileSync(new URL(import.meta.url), "utf8").split("*/")[0].replace(/^\/\*\n?/, ""));
  process.exit(0);
}

if (!fs.existsSync(HTML)) {
  console.error("index.html が見つかりません。プロジェクトのフォルダで実行してください。");
  process.exit(1);
}

let html = fs.readFileSync(HTML, "utf8");
const i = html.indexOf(START);
const j = html.indexOf(END);
if (i < 0 || j < 0) {
  console.error("index.html に GLB_DATA の目印がありません。");
  process.exit(1);
}

let data = {};
const block = html.slice(i + START.length, j).trim();
if (block.startsWith("window.__GLB")) {
  // data URI に ";" が含まれるので、正規表現ではなく末尾から切る
  let json = block.slice(block.indexOf("=") + 1).trim();
  if (json.endsWith(";")) json = json.slice(0, -1);
  try { data = JSON.parse(json); } catch { data = {}; }
}

const kb = (n) => (n / 1024).toFixed(0) + " KB";
const uriBytes = (u) => Math.floor((u.length - u.indexOf(",") - 1) * 3 / 4);

/* 外部参照しているテクスチャを glb 本体（BINチャンク）に取り込む。
   これで URL 解決が一切不要になり、どの環境でも同じように読める。 */
function inlineTextures(buf, glbPath) {
  if (buf.readUInt32LE(0) !== 0x46546c67) return buf;          // 'glTF' でなければ触らない
  const jsonLen = buf.readUInt32LE(12);
  const j = JSON.parse(buf.slice(20, 20 + jsonLen).toString("utf8"));
  const needs = (j.images || []).filter((im) => im.uri && !im.uri.startsWith("data:"));
  if (!needs.length) return buf;

  let bin = Buffer.alloc(0);
  const binPos = 20 + jsonLen;
  if (binPos + 8 <= buf.length && buf.readUInt32LE(binPos + 4) === 0x004e4942) {
    bin = buf.slice(binPos + 8, binPos + 8 + buf.readUInt32LE(binPos));
  }

  const dir = path.dirname(glbPath);
  const parts = [bin];
  let offset = bin.length;
  j.bufferViews = j.bufferViews || [];

  for (const im of j.images) {
    if (!im.uri || im.uri.startsWith("data:")) continue;
    const base = path.basename(im.uri);
    const hit = [path.join(dir, im.uri), path.join(dir, base), path.join(dir, "Textures", base)]
      .find((p) => fs.existsSync(p));
    if (!hit) { console.log("  テクスチャが見つかりません: " + im.uri); continue; }

    const pad = (4 - (offset % 4)) % 4;
    if (pad) { parts.push(Buffer.alloc(pad)); offset += pad; }
    const img = fs.readFileSync(hit);
    parts.push(img);
    const ext = path.extname(hit).slice(1).toLowerCase();
    j.bufferViews.push({ buffer: 0, byteOffset: offset, byteLength: img.length });
    im.bufferView = j.bufferViews.length - 1;
    im.mimeType = ext === "jpg" ? "image/jpeg" : "image/" + ext;
    delete im.uri;
    offset += img.length;
    console.log("  テクスチャを glb に取り込み: " + base + " (" + kb(img.length) + ")");
  }

  let nb = Buffer.concat(parts);
  const bp = (4 - (nb.length % 4)) % 4;
  if (bp) nb = Buffer.concat([nb, Buffer.alloc(bp)]);
  j.buffers = [{ byteLength: nb.length }];

  let nj = Buffer.from(JSON.stringify(j), "utf8");
  const jp = (4 - (nj.length % 4)) % 4;
  if (jp) nj = Buffer.concat([nj, Buffer.alloc(jp, 0x20)]);

  const total = 12 + 8 + nj.length + 8 + nb.length;
  const out = Buffer.alloc(total);
  out.writeUInt32LE(0x46546c67, 0); out.writeUInt32LE(2, 4); out.writeUInt32LE(total, 8);
  out.writeUInt32LE(nj.length, 12); out.writeUInt32LE(0x4e4f534a, 16);
  nj.copy(out, 20);
  const b = 20 + nj.length;
  out.writeUInt32LE(nb.length, b); out.writeUInt32LE(0x004e4942, b + 4);
  nb.copy(out, b + 8);
  return out;
}

/* 取り込めなかった場合の保険：画像を data URI として別に持っておく */
function collectTextures(glbPath, buf) {
  const out = {};
  try {
    const jsonLen = buf.readUInt32LE(12);
    const j = JSON.parse(buf.slice(20, 20 + jsonLen).toString("utf8"));
    const dir = path.dirname(glbPath);
    for (const im of j.images || []) {
      if (!im.uri || im.uri.startsWith("data:")) continue;
      const base = path.basename(im.uri);
      const cands = [path.join(dir, im.uri), path.join(dir, base), path.join(dir, "Textures", base)];
      const hit = cands.find((p) => fs.existsSync(p));
      if (!hit) { console.log("  テクスチャが見つかりません: " + im.uri); continue; }
      const ext = path.extname(hit).slice(1).toLowerCase();
      const mime = ext === "jpg" ? "image/jpeg" : "image/" + ext;
      out[base] = "data:" + mime + ";base64," + fs.readFileSync(hit).toString("base64");
      console.log("  テクスチャを同梱: " + base + " (" + kb(fs.statSync(hit).size) + ")");
    }
  } catch { /* JSON が読めなくてもモデル自体は埋め込む */ }
  return out;
}

function report() {
  const rows = [];
  if (data.player) rows.push(["自車", kb(uriBytes(data.player))]);
  (data.traffic || []).forEach((u, n) => rows.push(["対向車 " + (n + 1), kb(uriBytes(u))]));
  if (data.cone) rows.push(["パイロン", kb(uriBytes(data.cone))]);
  Object.keys(data.tex || {}).forEach((k) => rows.push(["texture", kb(uriBytes(data.tex[k]))]));
  if (!rows.length) { console.log("埋め込み済みのモデルはありません（コード生成の車が使われます）。"); return; }
  rows.forEach(([k, v]) => console.log("  " + k.padEnd(10) + v));
  const total = JSON.stringify(data).length;
  console.log("  " + "合計(base64)".padEnd(10) + kb(total));
  if (total > 12 * 1024 * 1024) console.log("\n  警告: 16MB の上限に近づいています。モデルを軽くしてください。");
}

function save() {
  const out = "\nwindow.__GLB = " + JSON.stringify(data) + ";\n";
  html = html.slice(0, i + START.length) + out + html.slice(j);
  fs.writeFileSync(HTML, html);
}

if (args[0] === "--list") { report(); process.exit(0); }

if (args[0] === "--clear") {
  data = {};
  save();
  console.log("埋め込みモデルを全て削除しました。コード生成の車に戻ります。");
  process.exit(0);
}

const file = path.resolve(args[0]);
const SLOTS = { traffic: "対向車", cone: "パイロン", player: "自車" };
const slot = SLOTS[args[1]] ? args[1] : "player";

if (!fs.existsSync(file)) { console.error("ファイルがありません: " + file); process.exit(1); }
if (!file.toLowerCase().endsWith(".glb")) {
  console.error(".glb を指定してください（.gltf は複数ファイルに分かれるため非対応）。");
  process.exit(1);
}

/* テクスチャは glb に取り込まず、data URI として別に持つ。
   取り込むと blob URL 経由になり、CSP の厳しい環境で読めなくなるため。 */
const buf = fs.readFileSync(file);
if (buf.length > 3 * 1024 * 1024) {
  console.log("注意: " + kb(buf.length) + " は大きすぎます。ポリゴンとテクスチャを削ってください。");
}

const uri = "data:model/gltf-binary;base64," + buf.toString("base64");
if (slot === "traffic") { data.traffic = data.traffic || []; data.traffic.push(uri); }
else data[slot] = uri;

data.tex = Object.assign(data.tex || {}, collectTextures(file, buf));   // 取り込み漏れ用の保険

save();
console.log(path.basename(file) + " を " + SLOTS[slot] + " として埋め込みました（" + kb(buf.length) + "）\n");
report();
