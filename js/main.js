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

// 네이버 지도 (NAVER Maps API v3, https://navermaps.github.io/maps.js.ncp/docs/tutorial-2-Getting-Started.html)
// index.html 맨 아래의 maps.js?ncpClientId=…&callback=initNaverMap 스크립트가 준비되면 initNaverMap 에서 지도를 그림.
// 인증 실패(등록되지 않은 서비스 URL 등) 시 navermap_authFailure 가 불려 '네이버 지도에서 보기' 링크로 되돌림.
// 설정은 기존 사이트와 동일: 확대/축소 컨트롤, 축척 표시, 마우스 휠 확대, 지도 유형 버튼 없음.
const mapEl = document.getElementById('map');
if (mapEl && mapEl.dataset.lat && mapEl.dataset.lng) {
  const fallback = mapEl.innerHTML;

  // 지도가 이미 붙인 스타일·'인증 실패' 타일까지 지우도록 #map 을 새 요소로 바꿈
  window.navermap_authFailure = () => {
    const clean = document.createElement('div');
    clean.className = mapEl.className;
    clean.id = mapEl.id;
    clean.innerHTML = fallback;
    mapEl.replaceWith(clean);
  };

  // maps.js(3.10.5)는 callback 을 naver.maps 를 만들기 직전에 부르므로, 스크립트 실행이 끝난 뒤 그리도록 한 박자 미룸
  window.initNaverMap = () => setTimeout(drawNaverMap);

  function drawNaverMap() {
    const position = new naver.maps.LatLng(+mapEl.dataset.lat, +mapEl.dataset.lng);
    mapEl.innerHTML = '';
    const map = new naver.maps.Map(mapEl, {
      center: position,
      zoom: +mapEl.dataset.zoom || 17,
      zoomControl: true,
      zoomControlOptions: { style: naver.maps.ZoomControlStyle.LARGE, position: naver.maps.Position.TOP_LEFT },
      mapTypeControl: false,
      scaleControl: true,
      scrollWheel: true,
    });
    const marker = new naver.maps.Marker({ position, map, title: '명품반찬' });
    const info = new naver.maps.InfoWindow({
      content: '<div style="padding:5px 15px"><p style="margin:0;font-size:15px;font-weight:bold">명품반찬</p></div>',
    });
    info.open(map, marker);
    naver.maps.Event.addListener(marker, 'click', () => info.open(map, marker));
  }

}

// 카테고리 사진 크게 보기: 사진을 누르면 검정 배경 위에 큰 사진·이름·순번이 뜸.
// 화살표 버튼·좌우 방향키·밀기로 넘기고, 돋보기 버튼·더블클릭으로 확대, 확대 중엔 끌어서 이동.
// 바깥(사진 아닌 곳)·X·Esc 로 닫힘. 마지막 사진 다음은 첫 사진으로 돌아감.
const galleryLinks = [...document.querySelectorAll('.gallery a')];
if (galleryLinks.length) {
  const svg = (size, body, extra = '') => `<svg viewBox="0 0 24 24" width="${size}" height="${size}" fill="none" stroke="currentColor" stroke-width="2" ${extra} aria-hidden="true">${body}</svg>`;
  const lb = document.createElement('div');
  lb.className = 'lightbox';
  lb.hidden = true;
  lb.setAttribute('role', 'dialog');
  lb.setAttribute('aria-modal', 'true');
  lb.setAttribute('aria-label', '사진 크게 보기');
  lb.innerHTML = `
    <div class="lb-stage"><img class="lb-image" alt=""></div>
    <div class="lb-toolbar">
      <p class="lb-counter"><span class="lb-current">1</span> / ${galleryLinks.length}</p>
      <button type="button" class="lb-actual" aria-label="원래 크기로 보기">${svg(20, '<rect x="4" y="4" width="16" height="16" rx="3"/>')}</button>
      <button type="button" class="lb-zoom-out" aria-label="축소">${svg(22, '<circle cx="10" cy="10" r="6.5"/><path d="M15 15l5.5 5.5M7 10h6"/>')}</button>
      <button type="button" class="lb-zoom-in" aria-label="확대">${svg(22, '<circle cx="10" cy="10" r="6.5"/><path d="M15 15l5.5 5.5M7 10h6M10 7v6"/>')}</button>
      <button type="button" class="lb-close" aria-label="닫기">${svg(18, '<path d="M3 3l18 18M21 3L3 21"/>')}</button>
    </div>
    <button type="button" class="lb-prev" aria-label="이전 사진">${svg(22, '<path d="M21 12H3M10 5l-7 7 7 7"/>', 'stroke-width="1.6"')}</button>
    <button type="button" class="lb-next" aria-label="다음 사진">${svg(22, '<path d="M3 12h18M14 5l7 7-7 7"/>', 'stroke-width="1.6"')}</button>
    <p class="lb-caption" aria-live="polite"></p>`;
  document.body.append(lb);

  const $ = (sel) => lb.querySelector(sel);
  const stage = $('.lb-stage');
  const img = $('.lb-image');
  const zoomOut = $('.lb-zoom-out');
  let index = 0;
  let scale = 1;
  let x = 0;
  let y = 0;

  // 확대한 사진이 화면 밖으로 너무 밀려나지 않게 이동 범위를 제한
  function clampPan() {
    const maxX = Math.max(0, (img.clientWidth * scale - stage.clientWidth) / 2);
    const maxY = Math.max(0, (img.clientHeight * scale - stage.clientHeight) / 2);
    x = Math.min(maxX, Math.max(-maxX, x));
    y = Math.min(maxY, Math.max(-maxY, y));
  }

  function setScale(next) {
    scale = Math.max(1, next);
    if (scale === 1) x = y = 0;
    clampPan();
    img.style.transform = scale === 1 ? '' : `translate(${x}px, ${y}px) scale(${scale})`;
    zoomOut.disabled = scale === 1;
    lb.classList.toggle('is-zoomed', scale > 1);
  }

  // 원래 크기: 화면에 줄여 보이는 사진을 실제 픽셀 크기로 (이미 실제 크기면 2배)
  function toggleActualSize() {
    const ratio = img.naturalWidth / img.clientWidth;
    setScale(scale > 1 ? 1 : (ratio > 1 ? ratio : 2));
  }

  function show(i) {
    index = (i + galleryLinks.length) % galleryLinks.length;
    const link = galleryLinks[index];
    setScale(1);
    img.classList.add('is-loading');
    img.onload = () => img.classList.remove('is-loading');
    img.src = link.href;
    $('.lb-current').textContent = index + 1;
    $('.lb-caption').textContent = link.textContent.trim();
  }

  function openLightbox(i) {
    show(i);
    lb.hidden = false;
    document.documentElement.style.overflow = 'hidden';
    requestAnimationFrame(() => requestAnimationFrame(() => lb.classList.add('is-open')));
    $('.lb-close').focus({ preventScroll: true });
  }

  function closeLightbox() {
    if (lb.hidden) return;
    lb.classList.remove('is-open');
    document.documentElement.style.overflow = '';
    galleryLinks[index].focus({ preventScroll: true });
    setTimeout(() => { if (!lb.classList.contains('is-open')) lb.hidden = true; }, 150);
  }

  galleryLinks.forEach((link, i) => link.addEventListener('click', (e) => {
    e.preventDefault();
    openLightbox(i);
  }));
  $('.lb-close').addEventListener('click', closeLightbox);
  $('.lb-prev').addEventListener('click', () => show(index - 1));
  $('.lb-next').addEventListener('click', () => show(index + 1));
  $('.lb-zoom-in').addEventListener('click', () => setScale(scale + 0.5));
  zoomOut.addEventListener('click', () => setScale(scale - 0.5));
  $('.lb-actual').addEventListener('click', toggleActualSize);
  img.addEventListener('dblclick', toggleActualSize);

  document.addEventListener('keydown', (e) => {
    if (lb.hidden) return;
    if (e.key === 'Escape') closeLightbox();
    else if (e.key === 'ArrowLeft') show(index - 1);
    else if (e.key === 'ArrowRight') show(index + 1);
  });

  // 끌기: 확대 중이면 사진 이동, 아니면 50px 이상 밀었을 때 이전/다음 사진
  let drag = null;
  stage.addEventListener('pointerdown', (e) => {
    if (e.button !== 0) return;
    // setPointerCapture 이후엔 e.target 이 항상 stage 가 되므로 사진 바깥을 눌렀는지는 여기서 기억
    drag = { id: e.pointerId, sx: e.clientX, sy: e.clientY, x, y, moved: false, outside: e.target === stage };
    stage.setPointerCapture(e.pointerId);
  });
  stage.addEventListener('pointermove', (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = e.clientX - drag.sx;
    const dy = e.clientY - drag.sy;
    if (Math.abs(dx) + Math.abs(dy) > 5) drag.moved = true;
    if (scale > 1 && drag.moved) {
      lb.classList.add('is-dragging');
      x = drag.x + dx;
      y = drag.y + dy;
      clampPan();
      img.style.transform = `translate(${x}px, ${y}px) scale(${scale})`;
    }
  });
  stage.addEventListener('pointerup', (e) => {
    if (!drag || e.pointerId !== drag.id) return;
    const dx = e.clientX - drag.sx;
    const { moved, outside } = drag;
    drag = null;
    lb.classList.remove('is-dragging');
    if (scale === 1 && Math.abs(dx) > 50) show(index + (dx < 0 ? 1 : -1));
    else if (!moved && outside) closeLightbox();
  });
  stage.addEventListener('pointercancel', () => {
    drag = null;
    lb.classList.remove('is-dragging');
  });
}
