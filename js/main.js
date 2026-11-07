// 모바일 메뉴 열기/닫기
const toggle = document.querySelector('.nav-toggle');
const nav = document.getElementById('site-nav');

function setNav(open) {
  nav.classList.toggle('is-open', open);
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? '메뉴 닫기' : '메뉴 열기');
}

toggle.addEventListener('click', () => setNav(!nav.classList.contains('is-open')));
nav.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setNav(false)));

// 현재 보고 있는 섹션의 메뉴 항목을 굵게
const navLinks = [...nav.querySelectorAll('a[href^="#"]')];
const sections = navLinks.map((a) => document.querySelector(a.getAttribute('href')));
const observer = new IntersectionObserver((entries) => {
  entries.forEach((entry) => {
    if (!entry.isIntersecting) return;
    navLinks.forEach((a) => {
      const active = a.getAttribute('href') === `#${entry.target.id}`;
      a.classList.toggle('is-active', active);
      if (active) a.setAttribute('aria-current', 'true');
      else a.removeAttribute('aria-current');
    });
  });
}, { rootMargin: '-45% 0px -50% 0px' });
sections.forEach((s) => s && observer.observe(s));

// 이미지 자리표시자: images/ 에 파일이 아직 없으면 점선 박스로 대체
document.querySelectorAll('img').forEach((img) => {
  const fallback = () => img.closest('.img-frame')?.classList.add('is-placeholder');
  if (img.complete && img.naturalWidth === 0) fallback();
  else img.addEventListener('error', fallback);
});

// 푸터 연도
document.getElementById('year').textContent = new Date().getFullYear();
