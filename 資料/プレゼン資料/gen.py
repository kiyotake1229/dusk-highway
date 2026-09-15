# Dusk Highway 社内説明資料（8枚）の生成。アプリ index.html の配色・書体をそのまま使う
# Python 3.9 のため f-string を入れ子にしない（部品を先に変数へ）
# 使い方: python3 資料/プレゼン資料/gen.py  → このフォルダに Main.dc.html / S02〜.dc.html / canvas.json / deck.html / PDF
#         画面写真は ../../screenshots/*.png を縮小した dusk-title.jpg / dusk-play.jpg（同じフォルダ）
import json, os
OUT = os.path.dirname(os.path.abspath(__file__))
PDF_NAME = 'DuskHighway_社内説明.pdf'
APP, DATE, N = 'Dusk Highway', '2026-09-15', 8

VOID, DUSK, INKB = '#0B1026', '#1B1B33', '#0A0A14'
EMBER, AMBER, CREAM, SAND, DANGER = '#C4553A', '#FFB648', '#F0E6D2', '#8C7A5E', '#FF5A48'
LINE, GLASS, MUTED = 'rgba(240,230,210,.16)', 'rgba(11,16,38,.62)', '#A89E8C'

HEAD = '''<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Chakra+Petch:wght@500;600;700&family=JetBrains+Mono:wght@400;700&family=Noto+Sans+JP:wght@400;700&display=swap">
  <style>
    body { margin: 0; background: #0B1026; color: #F0E6D2; font-family: "Hiragino Sans", "Noto Sans JP", system-ui, sans-serif; -webkit-font-smoothing: antialiased; }
    a { color: #FFB648; } a:hover { color: #F0E6D2; }
    .fd { font-family: "Chakra Petch", "Hiragino Sans", "Noto Sans JP", system-ui, sans-serif; }
    .fm { font-family: "JetBrains Mono", "SFMono-Regular", Menlo, monospace; font-variant-numeric: tabular-nums; }
    .ico { width: 24px; height: 24px; stroke: currentColor; fill: none; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex: none; }
  </style>
</helmet>
'''
TAIL = '''</x-dc>
</body>
</html>
'''

ICON = {
 'phone': '<svg class="ico" viewBox="0 0 24 24"><rect x="7" y="3" width="10" height="18" rx="2"/><path d="M11 18h2"/></svg>',
 'offline': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12a7 7 0 0 1 14 0"/><path d="M8.5 15a3.5 3.5 0 0 1 7 0"/><path d="M3 3l18 18"/></svg>',
 'clock': '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="13" r="8"/><path d="M12 9v4l3 2M9 3h6"/></svg>',
 'steer': '<svg class="ico" viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/><path d="M3 12h6M15 12h6M12 15v6"/></svg>',
 'cone': '<svg class="ico" viewBox="0 0 24 24"><path d="M9 4h6l4 16H5z"/><path d="M7.5 14h9M8.5 9h7"/></svg>',
 'zap': '<svg class="ico" viewBox="0 0 24 24"><path d="M13 2L4 14h7l-1 8 9-12h-7z"/></svg>',
 'shield': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3l8 3v6c0 5-3.5 8-8 9-4.5-1-8-4-8-9V6z"/></svg>',
 'check': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 12l4 4L19 7"/></svg>',
 'layers': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5"/></svg>',
 'sun': '<svg class="ico" viewBox="0 0 24 24"><path d="M4 16h16M6 12a6 6 0 0 1 12 0M12 3v2M4 8l1.5 1.5M20 8l-1.5 1.5"/></svg>',
 'combo': '<svg class="ico" viewBox="0 0 24 24"><path d="M4 18l5-6 4 4 7-9"/><path d="M16 7h4v4"/></svg>',
 'flag': '<svg class="ico" viewBox="0 0 24 24"><path d="M5 21V4h12l-2 4 2 4H5"/></svg>',
 'car': '<svg class="ico" viewBox="0 0 24 24"><path d="M3 14l2-6h14l2 6v4H3z"/><circle cx="7.5" cy="17" r="1.5"/><circle cx="16.5" cy="17" r="1.5"/><path d="M3 14h18"/></svg>',
 'gift': '<svg class="ico" viewBox="0 0 24 24"><rect x="4" y="9" width="16" height="11" rx="1"/><path d="M4 13h16M12 9v11M12 9c-2 0-4-1-4-3s3-2 4 3c1-5 4-5 4-3s-2 3-4 3"/></svg>',
 'cube': '<svg class="ico" viewBox="0 0 24 24"><path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M12 12l8-4.5M12 12v9M12 12L4 7.5"/></svg>',
 'file': '<svg class="ico" viewBox="0 0 24 24"><path d="M6 3h8l4 4v14H6z"/><path d="M14 3v4h4M9 13h6M9 17h6"/></svg>',
 'image': '<svg class="ico" viewBox="0 0 24 24"><rect x="4" y="5" width="16" height="14" rx="2"/><circle cx="9" cy="10" r="1.5"/><path d="M20 16l-5-5-7 8"/></svg>',
}

MOTIF = ('<div style="display:flex;align-items:center;gap:6px">'
         '<i style="display:block;width:26px;height:3px;background:%s"></i><i style="display:block;width:26px;height:3px;background:%s"></i>'
         '<i style="display:block;width:26px;height:3px;background:%s"></i><i style="display:block;width:26px;height:3px;background:%s"></i></div>') % (AMBER, AMBER, AMBER, EMBER)

def slide(n, body, eyebrow, title, title_size=44):
    foot = ('<div style="position:absolute;left:64px;bottom:30px;display:flex;align-items:center;gap:14px">'
            '<span class="fm" style="font-size:13px;color:%s;letter-spacing:.08em">No. %02d / %02d</span>'
            '<span style="width:1px;height:14px;background:%s"></span>'
            '<span class="fm" style="font-size:13px;color:%s">%s · 社内説明 · %s</span></div>'
            '<div style="position:absolute;right:64px;bottom:30px">%s</div>') % (MUTED, n, N, LINE, MUTED, APP, DATE, MOTIF)
    head = ''
    if title:
        head = ('<div style="display:flex;flex-direction:column;gap:8px">'
                '<div class="fm" style="font-size:13px;letter-spacing:.14em;color:%s">%s</div>'
                '<h1 class="fd" style="margin:0;font-size:%dpx;font-weight:700;line-height:1.2;letter-spacing:-.01em;color:%s;text-wrap:balance">%s</h1></div>') % (AMBER, eyebrow, title_size, CREAM, title)
    return HEAD + ('<div style="width:1280px;height:720px;position:relative;overflow:hidden;background:%s;padding:56px 64px 72px;box-sizing:border-box;display:flex;flex-direction:column;gap:28px">'
                   '%s%s%s</div>\n') % (VOID, head, body, foot) + TAIL

def paper(inner, extra=''):
    return '<div style="background:%s;color:%s;border-radius:12px;padding:24px 26px;display:flex;flex-direction:column;gap:10px;box-shadow:0 14px 34px rgba(0,0,0,.45);%s">%s</div>' % (CREAM, INKB, extra, inner)

def card(inner, extra=''):
    return '<div style="background:%s;border:1px solid %s;border-radius:12px;padding:22px 24px;display:flex;flex-direction:column;gap:10px;%s">%s</div>' % (DUSK, LINE, extra, inner)

def tag(text, color=AMBER, bg='rgba(255,182,72,.14)'):
    return '<span class="fm" style="display:inline-flex;font-size:13px;padding:5px 9px;border-radius:4px;background:%s;color:%s">%s</span>' % (bg, color, text)

def head_row(icon, text, size=22, color=CREAM, icolor=AMBER):
    return '<div style="display:flex;align-items:center;gap:10px;color:%s">%s<span class="fd" style="font-size:%dpx;font-weight:700;color:%s">%s</span></div>' % (icolor, icon, size, color, text)

def p(text, size=16, color=MUTED, lh=1.8):
    return '<p style="margin:0;font-size:%spx;line-height:%s;color:%s">%s</p>' % (size, lh, color, text)

def grid(cols, items, gap=18):
    return '<div style="display:grid;grid-template-columns:repeat(%d,minmax(0,1fr));gap:%dpx;flex:1;align-content:start">%s</div>' % (cols, gap, ''.join(items))

def check_line(text, size=16):
    return '<div style="display:flex;gap:10px;align-items:flex-start;font-size:%dpx;line-height:1.7;color:%s"><span style="color:%s;margin-top:2px">%s</span><span>%s</span></div>' % (size, CREAM, AMBER, ICON['check'], text)

files = {}

# ---------- 01 表紙 ----------
horizon = ('<div style="position:absolute;inset:0;background:linear-gradient(180deg,#0B1026 0%%,#1B1B33 45%%,#C4553A 78%%,#FFB648 100%%)"></div>'
           '<div style="position:absolute;left:0;right:0;bottom:0;height:150px;background:%s"></div>'
           '<div style="position:absolute;left:50%%;bottom:0;width:6px;height:150px;background:repeating-linear-gradient(180deg,%s 0 18px,transparent 18px 34px);transform:translateX(-50%%)"></div>'
           '<div style="position:absolute;left:0;right:0;bottom:150px;height:1px;background:%s"></div>') % (INKB, AMBER, LINE)
cover_text = ('<div style="position:relative;padding:44px 52px;display:flex;flex-direction:column;gap:12px;height:100%%;box-sizing:border-box">'
              '<div class="fm" style="font-size:14px;letter-spacing:.14em;color:%s">社内説明 · アプリ開発 · %s</div>'
              '<div class="fd" style="font-size:104px;font-weight:700;line-height:.95;letter-spacing:.02em;color:%s;text-shadow:0 6px 30px rgba(0,0,0,.5)">DUSK<br>HIGHWAY</div>'
              '<div style="font-size:24px;font-weight:700;line-height:1.5;color:%s;margin-top:6px">日没後の砂漠ハイウェイを走る、スマホ向け3Dエンドレスレース</div>'
              '<div class="fm" style="display:flex;gap:28px;font-size:14px;color:%s;margin-top:auto"><span>THREE.JS</span><span>SINGLE HTML · OFFLINE</span><span>PWA</span><span>kiyotake1229.github.io/dusk-highway</span></div></div>') % (CREAM, DATE, CREAM, CREAM, CREAM)
cover = ('<div style="display:flex;align-items:center;justify-content:center;flex:1">'
         '<div style="position:relative;width:1080px;height:480px;border-radius:16px;overflow:hidden;box-shadow:0 30px 70px rgba(0,0,0,.6);border:1px solid %s">%s%s</div></div>') % (LINE, horizon, cover_text)
files['Main.dc.html'] = slide(1, cover, '', '')

# ---------- 02 ねらい ----------
aims = [
 ('phone', 'スマホで動く3D', 'ブラウザだけで3Dゲームが成立するかの実証。Three.js を使い、縦持ち・片手で遊べる形にした。'),
 ('offline', '通信なしで動く', '3Dモデルもテクスチャも1つのHTMLに内包。電波のない場所でも、サーバーが落ちても遊べる。'),
 ('clock', '数十秒で1回遊べる', '起動して左右に動かすだけ。信号待ちの時間で1回走れる手軽さを最優先にした。'),
]
items = [paper(head_row(ICON[i], t, 26, INKB, EMBER) + p(d, 17, '#3d3830', 1.85), 'min-height:250px') for i, t, d in aims]
body = grid(3, items, 22) + '<div style="font-size:18px;color:%s;line-height:1.7">単一HTML・通信なしという「うちの作り方」で、3Dゲームまで作れることを示す1本。</div>' % MUTED
files['S02.dc.html'] = slide(2, body, '01 · ねらい', '単一HTMLで、3Dゲームは成立するか')

# ---------- 03 画面 ----------
shots = ('<div style="display:flex;gap:40px;justify-content:center;align-items:flex-start;flex:1">'
         '<div style="display:flex;flex-direction:column;gap:10px;align-items:center"><img src="dusk-title.jpg" style="width:220px;border-radius:18px;box-shadow:0 20px 50px rgba(0,0,0,.6);border:1px solid %s"><span class="fm" style="font-size:13px;color:%s">タイトル · 難易度と車種を選ぶ</span></div>'
         '<div style="display:flex;flex-direction:column;gap:10px;align-items:center"><img src="dusk-play.jpg" style="width:220px;border-radius:18px;box-shadow:0 20px 50px rgba(0,0,0,.6);border:1px solid %s"><span class="fm" style="font-size:13px;color:%s">走行中 · スコア・コンボ・ニトロ</span></div>'
         '<div style="display:flex;flex-direction:column;gap:14px;max-width:420px;padding-top:20px">%s%s%s</div></div>') % (
    LINE, MUTED, LINE, MUTED,
    card(head_row(ICON['sun'], '時間帯が移り変わる', 20) + p('1,300mごとに 日没 → 薄暮 → 深夜 → 夜明け。空と光が変わり、走るほど景色が進む。', 15, MUTED, 1.7)),
    card(head_row(ICON['car'], '6車種', 20) + p('ロードスター・SUV・タクシー・バン・トラック・パトカー。速度・旋回・耐久が違い、コインを貯めて解放する。', 15, MUTED, 1.7)),
    card(head_row(ICON['cube'], '3Dモデルは商用可の素材', 20) + p('Kenney Car Kit（CC0・クレジット不要）。差し替えの手順も文書化済み。', 15, MUTED, 1.7)))
files['S03.dc.html'] = slide(3, shots, '02 · 画面', '縦持ち・片手で、砂漠のハイウェイを走る')

# ---------- 04 遊び方 ----------
steps = [
 ('steer', '左右にドラッグ', '画面をなぞるだけでステアリング。PCは矢印キー。操作はこれだけ。'),
 ('cone', '避ける', '対向車とパイロンをかわす。ぶつかると車体が減る。ギリギリで抜けるとコンボ。'),
 ('zap', 'コインでニトロ', 'コインを10枚集めるとニトロが充填。右下のボタンで一気に加速。'),
 ('shield', '車体が0で終了', '車体は難易度と車種で決まる。修理キットで回復。ハイスコアは難易度ごとに記録。'),
]
items = []
for k, (i, t, d) in enumerate(steps):
    items.append(card('<div class="fm" style="font-size:13px;letter-spacing:.14em;color:%s">STEP %d</div>' % (AMBER, k + 1) + head_row(ICON[i], t) + p(d), 'min-height:250px'))
body = grid(4, items) + ('<div style="display:flex;align-items:center;gap:16px;background:%s;color:%s;border-radius:12px;padding:18px 26px">'
                         '<span class="fd" style="font-size:24px;font-weight:700">操作は左右だけ。</span>'
                         '<span style="font-size:17px;color:#5e564a">説明を読まなくても走り出せる。難しさは「どこまで行けるか」で作る。</span></div>') % (CREAM, INKB)
files['S04.dc.html'] = slide(4, body, '03 · 遊び方', '触れば分かる、4つのルール')

# ---------- 05 続ける仕掛け ----------
hooks = [
 ('layers', '難易度3段階', 'ツーリング／スポーツ／エキスパート。障害物の密度・速度・車体数・スコア倍率が変わる'),
 ('combo', 'コンボ最大 ×8', 'コイン取得とギリギリ通過でコンボが伸びる。スコアが跳ねる瞬間を作る'),
 ('flag', 'ミッション', '毎回3つ提示。達成で +1,500点。「今回はこれを狙う」という目的ができる'),
 ('car', '車種の解放', 'コインを貯めて6車種。次の車のために、もう1回走る理由になる'),
 ('gift', 'ギミック', '加速板・ジャンプ台・修理キット。コースに変化とご褒美を置く'),
 ('sun', '時間帯と景色', '走った距離で夜が明ける。長く走るほど見たことのない景色になる'),
]
items = [card(head_row(ICON[i], t, 21) + p(d, 15, MUTED, 1.7), 'min-height:170px') for i, t, d in hooks]
files['S05.dc.html'] = slide(5, grid(3, items), '04 · 続ける仕掛け', '「もう1回」を作る6つの要素')

# ---------- 06 技術 ----------
tech = [
 ('cube', 'Three.js r128', 'ブラウザの3D描画ライブラリ。車・道路・空・ライトをすべてこれで描く。'),
 ('file', '約1.9MBの単一HTML', '3Dモデル（.glb）とテクスチャを data URI で内包。外部ファイルの読み込みは0。'),
 ('image', 'Artifact の制約を回避', 'Claude Artifact ではテクスチャの読み込みが遮断される。読み込み方法を差し替えて解決済み。'),
]
items = [paper(head_row(ICON[i], t, 26, INKB, EMBER) + p(d, 16.5, '#3d3830', 1.85), 'min-height:250px') for i, t, d in tech]
body = grid(3, items, 20) + ('<div style="display:flex;gap:24px;align-items:center">'
    '<div style="flex:1;font-size:18px;color:%s;line-height:1.7">モデルは <b style="color:%s">コマンド1つで差し替え</b> できる。CC0素材・AI生成・Blender の3ルートを MODELS.md に文書化。</div>'
    '<div style="font-size:14px;color:%s;line-height:1.7;max-width:420px;border-left:1px solid %s;padding-left:20px">ファイルが大きいため、初回の読み込みに15〜20秒かかる。起動画面は出るが、ここは実機で要確認。</div></div>') % (MUTED, CREAM, MUTED, LINE)
files['S06.dc.html'] = slide(6, body, '05 · 技術', '3Dモデルごと、1つのHTMLに入れた')

# ---------- 07 現状 ----------
done = ['Web版 完成・公開中（GitHub Pages）', 'PWA対応。ホーム画面に追加すればアプリとして起動、オフラインで動く', '通信なし。ハイスコア・所持コイン・解放した車は端末内のみ', '難易度3段階・6車種・ミッション・コンボ・時間帯の変化・ギミック', '3Dモデルは商用利用可（CC0）。ライセンス全文を同梱', '縦持ち固定。ブラウザで横にした場合はHUDを縮小して対応', '開発用の監査コマンドで「3車線すべて塞がる」配置が出ないことを確認済み']
left = '<div style="display:flex;flex-direction:column;gap:9px">' + ''.join(check_line(d) for d in done) + '</div>'
right = paper('<div class="fm" style="font-size:13px;letter-spacing:.12em;color:#5e564a">いま触れる</div>'
              '<div class="fd" style="font-size:22px;font-weight:700;line-height:1.3">kiyotake1229.github.io/dusk-highway/</div>'
              '<div style="font-size:15px;line-height:1.8;color:#3d3830">iPhone の Safari で開き、共有メニューから「ホーム画面に追加」。初回だけ読み込みに時間がかかる。</div>'
              '<div class="fm" style="display:flex;flex-wrap:wrap;gap:8px;border-top:1px dashed #cfc4ad;padding-top:14px;font-size:13px;color:#5e564a"><span>単一 HTML</span><span>·</span><span>通信なし</span><span>·</span><span>端末内保存</span><span>·</span><span>約 1.9MB</span></div>', 'min-height:300px;justify-content:center')
body = '<div style="display:grid;grid-template-columns:minmax(0,1fr) 440px;gap:40px;flex:1;align-content:start">%s%s</div>' % (left, right)
files['S07.dc.html'] = slide(7, body, '06 · 現状', 'Web版は完成。いま触れる')

# ---------- 08 次のステップ ----------
road = [
 ('1', 'iOS 化', 'Capacitor で包む。コツコツの ios-app を雛形に、アイコンは icon-1024.png を使う。触覚を Capacitor Haptics に置き換え', '半日'),
 ('2', '実機検証', '初回読み込みの体感（15〜20秒）、フレームレート、発熱、縦固定の挙動。ここに時間がかかる', '2〜3日'),
 ('3', '申請', '年齢制限 4+、カテゴリ「ゲーム／レース」、「データを収集しません」、スクリーンショット3サイズ', '—'),
]
items = [card('<div class="fd" style="font-size:44px;font-weight:700;line-height:1;color:%s">%s</div><div class="fd" style="font-size:22px;font-weight:700">%s</div>%s<div class="fm" style="font-size:13px;color:%s;border-top:1px solid %s;padding-top:10px">目安 %s</div>' % (AMBER, n, t, p(d, 15, MUTED, 1.75).replace('<p style="', '<p style="flex:1;'), MUTED, LINE, w), 'min-height:270px') for n, t, d, w in road]
cost = paper('<div class="fm" style="font-size:12px;letter-spacing:.12em;color:#5e564a">費用</div><div style="display:flex;align-items:baseline;gap:10px"><span class="fd" style="font-size:36px;font-weight:700">¥12,800</span><span style="font-size:15px;color:#5e564a">/ 年 · Apple Developer Program のみ</span></div><div style="font-size:14px;color:#3d3830">3Dモデルは CC0。ライセンス料・サーバー費は0</div>', 'flex:1;padding:18px 24px;gap:6px')
decide = card('<div class="fm" style="font-size:12px;letter-spacing:.12em;color:%s">今日決めたいこと</div><div style="font-size:18px;font-weight:700;line-height:1.6">iOS化の順番。麻雀・語彙道場より実機検証に時間がかかるので、後ろに回すのが現実的。</div>' % AMBER, 'flex:1;padding:18px 24px;gap:6px;justify-content:center')
body = grid(3, items) + '<div style="display:flex;gap:20px">%s%s</div>' % (cost, decide)
files['S08.dc.html'] = slide(8, body, '07 · 次のステップ', 'iOS 化の道と、今日決めたいこと')

# ---------- 書き出し ----------
for name, src in files.items():
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(src)

names = ['Main.dc.html'] + ['S%02d.dc.html' % i for i in range(2, N + 1)]
W, H, GX, GY = 1280, 720, 80, 140
boards = []
for i, f in enumerate(names):
    r, c = divmod(i, 5)
    boards.append({'file': f, 'x': c * (W + GX), 'y': r * (H + GY), 'w': W, 'h': H, 'title': '%02d' % (i + 1)})
json.dump({'artboards': boards, 'launch': {'view': 'focused', 'file': 'Main.dc.html'}}, open(os.path.join(OUT, 'canvas.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

# PDF 用（全スライドを1ページずつ並べたHTML。Chrome で印刷して PDF にする）
helmet = HEAD.split('<helmet>')[1].split('</helmet>')[0]
pages = ''.join('<div style="width:1280px;height:720px;page-break-after:always;overflow:hidden">%s</div>' % files[f].split('</helmet>\n')[1].split('</x-dc>')[0] for f in names)
deck = '<!doctype html><html><head><meta charset="utf-8"><title>%s 社内説明</title>%s<style>@page{size:1280px 720px;margin:0}html,body{margin:0}</style></head><body>%s</body></html>' % (APP, helmet, pages)
open(os.path.join(OUT, 'deck.html'), 'w', encoding='utf-8').write(deck)
print('written', len(files))

# PDF（このフォルダに書き出す。Chrome が無い環境ではスキップ）
import subprocess
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
PDF = os.path.join(OUT, PDF_NAME)
if os.path.exists(CHROME):
    subprocess.run([CHROME, '--headless=new', '--disable-gpu', '--no-pdf-header-footer', '--virtual-time-budget=8000',
                    '--print-to-pdf=' + PDF, 'file://' + os.path.join(OUT, 'deck.html')],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False)
    print('pdf', PDF)
else:
    print('Chrome が見つからないため PDF は作っていません')
