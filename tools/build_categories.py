"""배민 메뉴(reference/baemin/menus.tsv)로 카테고리 페이지·사진·내비게이션을 다시 만든다.
사용: python3 -I build.py <프로젝트 경로> <작업 폴더>
"""
import html, os, re, shutil, subprocess, sys, urllib.request

ROOT, WORK = sys.argv[1], sys.argv[2]
PREFIX = 'http://imagefarm.baemin.com/smartmenuimage/upload/image/'

CATS = [  # 배민 그룹명, 표시명, 영문 slug
    ('국/찌개', '국 · 찌개', 'soup'),
    ('마른반찬', '마른반찬', 'dried'),
    ('장아찌', '장아찌', 'pickled'),
    ('나물', '나물', 'namul'),
    ('볶음', '볶음', 'stir-fried'),
    ('강정/생선', '강정 · 생선', 'fish'),
    ('조림/젓갈', '조림 · 젓갈', 'braised'),
    ('김치', '김치', 'kimchi'),
    ('전', '전', 'jeon'),
    ('밥/샐러드/기타', '밥 · 샐러드 · 기타', 'rice-etc'),
]
OVERLAY = {'rice-etc'}
NAMES = {'가지나물 (반찬)': '가지나물'}  # 홈페이지에 바꿔 쓰는 이름

SLUGS = {
    '닭볶음탕': 'dakbokkeumtang', '묵은지김치찜': 'mukeunji-kimchijjim', '청국장': 'cheonggukjang',
    '우거지된장국': 'ugeoji-doenjangguk', '소고기무국': 'sogogi-mutguk', '소고기미역국': 'sogogi-miyeokguk',
    '동태찌개': 'dongtae-jjigae', '된장찌개': 'doenjang-jjigae', '콩비지찌개': 'kongbiji-jjigae',
    '부대찌개(Meal Kit)': 'budae-jjigae-mealkit', '우렁된장찌개(Meal Kit)': 'ureong-doenjang-jjigae-mealkit',
    '계란찜': 'gyeranjjim',
    '오징어실채': 'ojingeo-silchae', '진미채': 'jinmichae', '아몬드멸치볶음': 'almond-myeolchi-bokkeum',
    '고추장멸치볶음': 'gochujang-myeolchi-bokkeum', '호두멸치볶음': 'hodu-myeolchi-bokkeum',
    '꽈리고추멸치볶음': 'kkwarigochu-myeolchi-bokkeum', '건새우볶음': 'geonsaeu-bokkeum', '콩자반': 'kongjaban',
    '황태채무침': 'hwangtaechae-muchim', '견과류볶음': 'gyeongwaryu-bokkeum',
    '양념생깻잎': 'yangnyeom-saengkkaennip', '양념깻잎절임': 'yangnyeom-kkaennip-jeorim',
    '간장깻잎절임': 'ganjang-kkaennip-jeorim', '양념고추장아찌': 'yangnyeom-gochu-jangajji',
    '고들빼기무침': 'godeulppaegi-muchim', '무말랭이': 'mumallaengi', '우엉채볶음': 'ueongchae-bokkeum',
    '명이나물': 'myeongi-namul', '마늘초절임': 'maneul-chojeorim', '간장고추장아찌': 'ganjang-gochu-jangajji',
    '연근조림': 'yeongeun-jorim',
    '참치김치볶음': 'chamchi-kimchi-bokkeum', '무생채무침': 'musaengchae-muchim', '도라지오이무침': 'doraji-oi-muchim',
    '흰도라지볶음': 'huin-doraji-bokkeum', '고사리볶음': 'gosari-bokkeum', '느타리버섯볶음': 'neutari-beoseot-bokkeum',
    '마늘쫑건새우볶음': 'maneuljjong-geonsaeu-bokkeum', '애호박볶음': 'aehobak-bokkeum',
    '감자채볶음': 'gamjachae-bokkeum', '콩나물무침': 'kongnamul-muchim', '숙주나물': 'sukju-namul',
    '시금치': 'sigeumchi', '취나물': 'chwinamul', '파래초무침': 'parae-chomuchim', '무나물': 'munamul',
    '고구마줄기볶음': 'goguma-julgi-bokkeum', '건파래무침': 'geonparae-muchim', '가지나물 (반찬)': 'gaji-namul',
    '우거지된장무침': 'ugeoji-doenjang-muchim', '꽈리고추찜': 'kkwarigochu-jjim', '달래무침장': 'dallae-muchimjang',
    '미역줄기볶음': 'miyeok-julgi-bokkeum', '짠무무침': 'jjanmu-muchim', '깻잎순나물': 'kkaennipsun-namul',
    '잡채': 'japchae', '소불고기볶음': 'so-bulgogi-bokkeum', '제육볶음': 'jeyuk-bokkeum',
    '오징어볶음': 'ojingeo-bokkeum', '쭈꾸미볶음': 'jjukkumi-bokkeum', '소세지야채볶음': 'sausage-yachae-bokkeum',
    '어묵채볶음': 'eomukchae-bokkeum', '메추리알어묵볶음': 'mechurial-eomuk-bokkeum',
    '고추장어묵볶음': 'gochujang-eomuk-bokkeum',
    '고등어구이': 'godeungeo-gui', '가자미구이': 'gajami-gui', '오징어숙회': 'ojingeo-sukhoe',
    '고등어조림': 'godeungeo-jorim', '갈치조림': 'galchi-jorim', '표고탕수육': 'pyogo-tangsuyuk',
    '두부탕수육': 'dubu-tangsuyuk', '코다리강정(고추장)': 'kodari-gangjeong-gochujang',
    '코다리강정(간장)': 'kodari-gangjeong-ganjang',
    '두부양념조림': 'dubu-yangnyeom-jorim', '두부간장조림': 'dubu-ganjang-jorim',
    '꽈리고추계란조림': 'kkwarigochu-gyeran-jorim', '소고기장조림': 'sogogi-jangjorim',
    '메추리알조림': 'mechurial-jorim', '조개젓': 'jogaejeot', '낙지젓': 'nakjijeot', '오징어젓': 'ojingeojeot',
    '창란젓': 'changnanjeot', '갈치속젓': 'galchisokjeot',
    '배추겉절이': 'baechu-geotjeori', '총각김치': 'chonggak-kimchi', '깍두기': 'kkakdugi',
    '나박김치': 'nabak-kimchi', '오이소박이': 'oi-sobagi', '파김치': 'pa-kimchi',
    '김치전': 'kimchijeon', '부추전': 'buchujeon', '동태전': 'dongtaejeon',
    '짜장': 'jjajang', '카레': 'curry', '오므라이스': 'omurice', '계란말이': 'gyeranmari', '김부각': 'gimbugak',
    '도토리묵': 'dotorimuk', '구운계란': 'guun-gyeran', '양배추쌈': 'yangbaechu-ssam',
    '김치볶음밥': 'kimchi-bokkeumbap', '샐러드': 'salad',
}


def sips(*args):
    subprocess.run(['sips', *args], check=True, capture_output=True)


def size(path):
    out = subprocess.run(['sips', '-g', 'pixelWidth', '-g', 'pixelHeight', path],
                         check=True, capture_output=True, text=True).stdout
    return int(re.search(r'pixelWidth: (\d+)', out)[1]), int(re.search(r'pixelHeight: (\d+)', out)[1])


# ----- 메뉴 목록 읽기
menus = {g: [] for g, _, _ in CATS}
for line in open(os.path.join(ROOT, 'reference/baemin/menus.tsv'), encoding='utf-8'):
    group, name, _price, url = line.rstrip('\n').split('\t')
    url = None if url == '-' else url.replace('~', PREFIX, 1) if url.startswith('~') else url
    menus[group].append({'name': NAMES.get(name, name), 'slug': SLUGS[name], 'url': url})

# ----- 사진: 원본 → <slug>-large.jpg(최대 1280), <slug>.jpg(가로 700), 카테고리 대표 cat-<slug>.jpg(700×525)
img_root = os.path.join(ROOT, 'images/menu')
for group, _, cslug in CATS:
    folder = os.path.join(img_root, cslug)
    os.makedirs(folder, exist_ok=True)
    for m in menus[group]:
        if not m['url']:
            continue
        src = os.path.join(WORK, f"{cslug}-{m['slug']}.orig.jpg")
        if not os.path.exists(src):
            urllib.request.urlretrieve(m['url'], src)
        large = os.path.join(folder, f"{m['slug']}-large.jpg")
        thumb = os.path.join(folder, f"{m['slug']}.jpg")
        shutil.copyfile(src, large)
        w, h = size(large)
        if w > 1280:
            sips('--resampleWidth', '1280', large)
        shutil.copyfile(src, thumb)
        if w > 700:
            sips('--resampleWidth', '700', '-s', 'formatOptions', '80', thumb)
        m['w'], m['h'] = size(thumb)

    first = next(m for m in menus[group] if m['url'])
    cat = os.path.join(img_root, f'cat-{cslug}.jpg')
    shutil.copyfile(os.path.join(img_root, cslug, f"{first['slug']}-large.jpg"), cat)
    w, h = size(cat)
    if w * 3 > h * 4:   # 가로가 길면 가운데를 4:3 으로 자름
        sips('-c', str(h), str(h * 4 // 3), cat)
    elif w * 3 < h * 4:
        sips('-c', str(w * 3 // 4), str(w), cat)
    sips('-z', '525', '700', '-s', 'formatOptions', '80', cat)

# ----- 내비게이션(헤더 하위 메뉴·모바일 슬라이드 메뉴)
def nav_items(indent):
    return '\n'.join(f'{indent}<li><a href="{s}">{label}</a></li>' for _, label, s in CATS)

def replace_nav(text):
    text = re.sub(r'(<ul class="sub-menu">\n)(.*?)(\n(\s*)</ul>)',
                  lambda m: m[1] + nav_items(m[4] + '  ') + m[3], text, flags=re.S)
    text = re.sub(r'(<ul class="slide-sub" id="slide-sub-menu">\n)(.*?)(\n(\s*)</ul>)',
                  lambda m: m[1] + nav_items(m[4] + '  ') + m[3], text, flags=re.S)
    return text

# ----- 카테고리 페이지 (기존 soup.html 을 틀로 사용)
template = open(os.path.join(ROOT, 'soup.html'), encoding='utf-8').read()
for group, label, cslug in CATS:
    names = ', '.join(m['name'] for m in menus[group])
    desc = html.escape(f'명품반찬 {label}: {names}', quote=True)
    items = []
    for i, m in enumerate(menus[group]):
        lazy = ' loading="lazy"' if i >= 8 else ''
        name = html.escape(m['name'])
        if m['url']:
            big, small = f"images/menu/{cslug}/{m['slug']}-large.jpg", f"images/menu/{cslug}/{m['slug']}.jpg"
            wh = f'width="{m["w"]}" height="{m["h"]}"'
        else:
            big = small = 'images/menu/no-image.gif'
            wh = 'width="600" height="400"'
        items.append(f'        <li><a href="{big}"><img src="{small}" alt="" {wh}{lazy}><span>{name}</span></a></li>')
    gallery_class = 'gallery gallery--overlay' if cslug in OVERLAY else 'gallery'

    page = template
    page = re.sub(r'<title>.*?</title>', f'<title>{label} | 명품반찬</title>', page)
    page = re.sub(r'(<meta name="description" content=")[^"]*', lambda m: m[1] + desc, page)
    page = re.sub(r'(<meta property="og:title" content=")[^"]*', lambda m: m[1] + f'{label} | 명품반찬', page)
    page = re.sub(r'(<meta property="og:description" content=")[^"]*', lambda m: m[1] + desc, page)
    page = re.sub(r'(<meta property="og:url" content="[^"]*/)[^/"]*"', lambda m: m[1] + cslug + '"', page)
    page = re.sub(r'<h1 class="page-title">.*?</h1>', f'<h1 class="page-title">| {label}</h1>', page)
    page = re.sub(r'<ul class="gallery[^"]*">\n.*?\n(\s*)</ul>',
                  lambda m: f'<ul class="{gallery_class}">\n' + '\n'.join(items) + '\n' + m[1] + '</ul>',
                  page, flags=re.S)
    page = replace_nav(page)
    open(os.path.join(ROOT, f'{cslug}.html'), 'w', encoding='utf-8').write(page)

# ----- 메뉴 페이지 타일
tiles = '\n'.join(
    f'        <li><a href="{s}"><img src="images/menu/cat-{s}.jpg" alt="" width="700" height="525"><span>{label}</span></a></li>'
    for _, label, s in CATS)
for fname in ['index.html', 'menu.html', 'bulk.html']:
    path = os.path.join(ROOT, fname)
    text = replace_nav(open(path, encoding='utf-8').read())
    if fname == 'menu.html':
        text = re.sub(r'(<ul class="category-grid">\n).*?(\n\s*</ul>)', lambda m: m[1] + tiles + m[2], text, flags=re.S)
    open(path, 'w', encoding='utf-8').write(text)

print({c[2]: len(menus[c[0]]) for c in CATS})
