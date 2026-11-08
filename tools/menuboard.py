"""reference/baemin/menus.tsv 로 '전체 메뉴' 메뉴판 HTML 을 만든다 (A4, 1240×1754 CSS px → 2배 렌더링).
사용: python3 -I menuboard.py <프로젝트 경로> <출력 html>
이미지로 만들기(크롬):
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless=new --hide-scrollbars \
    --allow-file-access-from-files --force-device-scale-factor=2 --window-size=1240,1754 \
    --screenshot=menu.png file://<출력 html>
  sips -s format jpeg -s formatOptions 85 menu.png --out files/myungpum-menu.jpg
"""
import html, os, re, sys

ROOT, OUT = sys.argv[1], sys.argv[2]
LABELS = {'국/찌개': '국 · 찌개', '강정/생선': '강정 · 생선', '조림/젓갈': '조림 · 젓갈', '밥/샐러드/기타': '밥 · 샐러드 · 기타'}

groups = {}
for line in open(os.path.join(ROOT, 'reference/baemin/menus.tsv'), encoding='utf-8'):
    group, name, price, _ = line.rstrip('\n').split('\t')
    groups.setdefault(group, []).append((name, int(price)))

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
html, body {{ width: 1240px; height: 1754px; background: #fff; }}
body {{ font-family: SUITE, sans-serif; color: #212121; padding: 0 60px; position: relative; }}
.bar {{ position: absolute; left: 0; right: 0; top: 0; height: 14px; background: #ff5700; }}
header {{ padding-top: 58px; text-align: center; }}
header img {{ width: 300px; height: 90px; }}
.sub {{ margin-top: 18px; font-size: 30px; font-weight: 800; letter-spacing: 2px; }}
.sub::after {{ content: ""; display: block; width: 50px; height: 2px; margin: 16px auto 0; background: #212121; }}
.contact {{ position: absolute; right: 60px; top: 150px; font-size: 26px; text-align: right; }}
.contact b {{ font-weight: 800; }}
main {{ margin-top: 36px; height: 1130px; column-count: 4; column-gap: 36px; column-fill: balance; }}
.cat {{ margin-bottom: 26px; }}
.cat h2 {{ break-after: avoid; }}
.cat li {{ break-inside: avoid; }}
.cat h2 {{ font-size: 24px; font-weight: 800; color: #fff; background: #ff5700; border-radius: 6px; padding: 6px 12px; margin-bottom: 6px; }}
.cat li {{ list-style: none; display: flex; justify-content: space-between; gap: 8px; font-size: 20px; line-height: 32px; border-bottom: 1px dotted #ddd; }}
.cat .n {{ white-space: nowrap; }}
.cat .n small {{ font-size: .8em; }}
.cat .p {{ font-variant-numeric: tabular-nums; white-space: nowrap; }}
.note {{ font-size: 15px; color: #777; text-align: right; margin-top: -8px; }}
.reserve {{ position: absolute; left: 60px; right: 60px; bottom: 150px; border: 2px solid #ff5700; border-radius: 12px; overflow: hidden; text-align: center; }}
.reserve h3 {{ background: #ff5700; color: #fff; font-size: 26px; font-weight: 800; letter-spacing: 8px; padding: 10px 0; }}
.reserve p {{ font-size: 24px; padding: 22px 0 6px; }}
.reserve p + p {{ padding: 0 0 22px; font-size: 26px; font-weight: 800; }}
.account {{ position: absolute; left: 0; right: 0; bottom: 58px; text-align: center; font-size: 34px; font-weight: 800; }}
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
<div class="reserve">
  <h3>※ 예약 문의</h3>
  <p>제사음식 / 생일음식상 / 이바지음식 / 집들이음식</p>
  <p>☎ 02-429-7774</p>
</div>
<p class="account">입금계좌번호: 농협 356-1125-7577-83 김민경</p>
</body></html>
'''
open(OUT, 'w', encoding='utf-8').write(page)
