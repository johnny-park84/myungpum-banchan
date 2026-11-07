// 모바일 슬라이드 메뉴: 왼쪽에서 0.3초 동안 밀려 나오고, 배경·X·Esc 로 닫힘
const slideMenu = document.getElementById('slide-menu');
const menuToggle = document.querySelector('.menu-toggle');
const DURATION = 300;

function openMenu() {
  slideMenu.hidden = false;
  document.documentElement.style.overflow = 'hidden';
  requestAnimationFrame(() => requestAnimationFrame(() => slideMenu.classList.add('is-open')));
  menuToggle.setAttribute('aria-expanded', 'true');
}

function closeMenu() {
  if (slideMenu.hidden) return;
  slideMenu.classList.remove('is-open');
  menuToggle.setAttribute('aria-expanded', 'false');
  document.documentElement.style.overflow = '';
  setTimeout(() => { if (!slideMenu.classList.contains('is-open')) slideMenu.hidden = true; }, DURATION);
}

menuToggle.addEventListener('click', openMenu);
slideMenu.querySelectorAll('[data-close]').forEach((el) => el.addEventListener('click', closeMenu));
document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeMenu(); });
matchMedia('(min-width: 992px)').addEventListener('change', (e) => { if (e.matches) closeMenu(); });

// 슬라이드 메뉴의 '메뉴' 하위 항목 펼치기
slideMenu.querySelectorAll('.sub-toggle').forEach((btn) => {
  const sub = document.getElementById(btn.getAttribute('aria-controls'));
  btn.addEventListener('click', () => {
    const open = btn.getAttribute('aria-expanded') !== 'true';
    btn.setAttribute('aria-expanded', String(open));
    btn.setAttribute('aria-label', open ? '메뉴 하위 항목 접기' : '메뉴 하위 항목 펼치기');
    sub.classList.toggle('is-open', open);
  });
});

// 네이버 지도: #map 의 data-ncp-key-id(네이버 클라우드 Maps Client ID)와 좌표로 지도를 띄움.
// 인증 실패(등록되지 않은 도메인 등)나 로드 실패 시에는 '네이버 지도에서 보기' 링크가 그대로 보입니다.
// 설정은 기존 사이트와 동일: 확대/축소 컨트롤, 축척 표시, 마우스 휠 확대, 지도 유형 버튼 없음.
const mapEl = document.getElementById('map');
if (mapEl && mapEl.dataset.ncpKeyId && mapEl.dataset.lat && mapEl.dataset.lng) {
  const fallback = mapEl.innerHTML;
  window.navermap_authFailure = () => { mapEl.innerHTML = fallback; };
  const script = document.createElement('script');
  script.src = `https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${encodeURIComponent(mapEl.dataset.ncpKeyId)}`;
  script.onload = () => {
    const pos = new naver.maps.LatLng(+mapEl.dataset.lat, +mapEl.dataset.lng);
    mapEl.innerHTML = '';
    const map = new naver.maps.Map(mapEl, {
      center: pos,
      zoom: +mapEl.dataset.zoom || 17,
      zoomControl: true,
      zoomControlOptions: { style: naver.maps.ZoomControlStyle.LARGE, position: naver.maps.Position.TOP_LEFT },
      mapTypeControl: false,
      scaleControl: true,
      scrollWheel: true,
    });
    const marker = new naver.maps.Marker({ position: pos, map, title: '명품반찬' });
    const info = new naver.maps.InfoWindow({
      content: '<div style="padding:5px 15px"><p style="margin:0;font-size:15px;font-weight:bold">명품반찬</p></div>',
    });
    info.open(map, marker);
    marker.addListener('click', () => info.open(map, marker));
  };
  document.head.appendChild(script);
}
