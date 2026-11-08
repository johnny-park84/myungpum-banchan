"""reference/baemin/menus.tsv 로 '전체 메뉴' 메뉴판 HTML 을 만든다 (A4, 1240×1754 CSS px → 2배 렌더링).
사용: python3 -I menuboard.py <프로젝트 경로> <출력 html>
이미지로 만들기(크롬):
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
    --allow-file-access-from-files --force-device-scale-factor=2 --window-size=1240,1754 \
    --screenshot=menu.png file://<출력 html>
  cp menu.png files/myungpum-menu.png   # JPG 는 주황 바탕 흰 글자 주변에 얼룩이 생겨 PNG 로 둠
"""
import html, os, re, sys

ROOT, OUT = sys.argv[1], sys.argv[2]
NAMES = {'가지나물 (반찬)': '가지나물'}  # 메뉴판에서만 바꿔 쓰는 이름
LABELS = {'국/찌개': '국 · 찌개', '강정/생선': '강정 · 생선', '조림/젓갈': '조림 · 젓갈', '밥/샐러드/기타': '밥 · 샐러드 · 기타'}

groups = {}
for line in open(os.path.join(ROOT, 'reference/baemin/menus.tsv'), encoding='utf-8'):
    group, name, price, _ = line.rstrip('\n').split('\t')
    groups.setdefault(group, []).append((NAMES.get(name, name), int(price)))

def menu_name(name):
    # '(Meal Kit)' 같은 괄호 부분은 작게 써서 한 줄에 들어가게 함
    return re.sub(r'(\(.*?\))', r'<small>\1</small>', html.escape(name))

blocks = []
for group, items in groups.items():
    rows = '\n'.join(
        f'<li><span class="n">{menu_name(n)}</span><span class="p">{p:,}</span></li>' for n, p in items)
    blocks.append(f'<section class="cat"><h2>{LABELS.get(group, group)}</h2><ul>{rows}</ul></section>')

fonts = 'file://' + os.path.join(ROOT, 'fonts')
logo = 'file://' + os.path.join(ROOT, 'images/logo-header.png')
page = f'''<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<style>
@font-face {{ font-family: SUITE; font-weight: 400; src: url({fonts}/SUITE-Regular.woff2) format("woff2"); }}
@font-face {{ font-family: SUITE; font-weight: 800; src: url({fonts}/SUITE-ExtraBold.woff2) format("woff2"); }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
/* 색: 로고의 짙은 갈색·붉은 도장에 맞춘 따뜻한 톤 */
:root {{ --bg: #fbf7f0; --ink: #3a2e25; --muted: #8a7b6d; --accent: #e8622a; --line: #e4d9ca; --card: #fffdf9; }}
html, body {{ width: 1240px; height: 1754px; background: var(--bg); }}
body {{ font-family: SUITE, sans-serif; color: var(--ink); padding: 0 48px; position: relative; }}
.bar {{ position: absolute; left: 0; right: 0; top: 0; height: 14px; background: var(--accent); }}
header {{ padding-top: 58px; text-align: center; }}
header img {{ width: 300px; height: 90px; }}
.sub {{ margin-top: 18px; font-size: 30px; font-weight: 800; letter-spacing: 2px; }}
.sub::after {{ content: ""; display: block; width: 50px; height: 2px; margin: 16px auto 0; background: var(--accent); }}
.contact {{ position: absolute; right: 48px; top: 150px; font-size: 26px; text-align: right; }}
.contact b {{ font-weight: 800; }}
main {{ margin-top: 30px; height: 1190px; column-count: 4; column-gap: 32px; column-fill: balance; }}
.cat {{ margin-bottom: 22px; }}
.cat h2 {{ break-after: avoid; }}
.cat li {{ break-inside: avoid; }}
.cat h2 {{ font-size: 26px; font-weight: 800; color: #fff; background: var(--accent); border-radius: 6px; padding: 6px 12px; margin-bottom: 6px; }}
.cat li {{ list-style: none; display: flex; justify-content: space-between; gap: 8px; font-size: 22px; line-height: 34px; border-bottom: 1px dotted var(--line); }}
.cat .n {{ white-space: nowrap; }}
.cat .n small {{ font-size: .8em; color: var(--muted); }}
.cat .p {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
.note {{ font-size: 15px; color: #777; text-align: right; margin-top: -8px; }}
.more {{ position: absolute; left: 0; right: 0; bottom: 326px; text-align: center; font-size: 22px; line-height: 32px; }}
.more b {{ display: block; font-size: 26px; font-weight: 800; color: var(--accent); }}
.reserve {{ position: absolute; left: 48px; right: 48px; bottom: 128px; border: 2px solid var(--accent); border-radius: 12px; overflow: hidden; text-align: center; background: var(--card); }}
.reserve h3 {{ background: var(--accent); color: #fff; font-size: 26px; font-weight: 800; letter-spacing: 8px; padding: 10px 0; }}
.reserve p {{ font-size: 36px; font-weight: 800; padding: 22px 0 8px; }}
.reserve p + p {{ padding: 0 0 22px; font-size: 28px; }}
.account {{ position: absolute; left: 0; right: 0; bottom: 50px; text-align: center; font-size: 34px; font-weight: 800; }}
</style></head>
<body>
<div class="bar"></div>
<header>
  <img src="{logo}" alt="명품반찬">
  <p class="sub">명품반찬 전체 메뉴</p>
</header>
<p class="contact">문의: <b>02-429-7774</b></p>
<main>
{chr(10).join(blocks)}
</main>
<p class="more"><b>매일 새로 만드는 130여 가지 반찬</b>매장에는 이 밖에도 그날그날 만든 다양한 반찬이 준비되어 있습니다.</p>
<div class="reserve">
  <h3>※ 예약 문의</h3>
  <p>제사음식 / 생일음식상 / 이바지음식 / 집들이음식</p>
  <p>☎ 02-429-7774</p>
</div>
<p class="account">입금계좌번호: 농협 356-1125-7577-83 김민경</p>
</body></html>
'''
open(OUT, 'w', encoding='utf-8').write(page)
