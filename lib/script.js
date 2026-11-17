const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];

/* 1. 프로젝트 탭 전환 */
const projectTabs = $$('.project-tab');
const projectPanes = $$('.project-pane');

function selectProject(index) {
  projectTabs.forEach((tab, i) => {
    tab.classList.toggle('is-active', i === index);
    tab.setAttribute('aria-current', i === index);
  });
  projectPanes.forEach((pane, i) => {
    pane.hidden = i !== index;
  });
}

projectTabs.forEach((tab, i) => {
  ['click', 'mouseenter', 'focus'].forEach(type => {
    tab.addEventListener(type, () => selectProject(i));
  });
});


/* 3. 네비게이션 활성화 감지 (현재 보고 있는 섹션 표시) */
const navLinks = $$('.nav-links a');
const navSections = navLinks.map(link => $(link.hash)).filter(Boolean);

function updateNav() {
  const y = window.innerHeight * 0.35;
  const current = navSections.find(section => {
    const rect = section.getBoundingClientRect();
    return rect.top <= y && y < rect.bottom;
  });
  navLinks.forEach((link, i) => link.classList.toggle('is-active', navSections[i] === current));
}

/* 4. 스크롤 & TOP 버튼 */
const topButton = $('#back-to-top');
function onScroll() {
  if (topButton) topButton.classList.toggle('is-visible', window.scrollY > 280);
  updateNav();
}
window.addEventListener('scroll', onScroll, { passive: true });
window.addEventListener('resize', updateNav);
if (topButton) {
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
}
onScroll();

/* 5. 스크롤하면 살짝 떠오르는 효과 + 제목 밑줄 그리기 */
(function () {
  if (!('IntersectionObserver' in window)) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  const groups = [
    '.hero-copy > *', '.hero-art', '.number-grid > div',
    '.section-label', 'h2', '.section-lead',
    '.soft-card', '.skill-card', '.project-list', '.project-preview',
    '.career-photos img', '.career-year-group', '.background', '.cert-card'
  ];
  const targets = [];
  groups.forEach(sel => {
    $$(sel).forEach(el => {
      if (targets.includes(el) || el.closest('dialog')) return;
      const order = el.parentElement ? [...el.parentElement.children].indexOf(el) : 0;
      el.classList.add('rv');
      el.style.setProperty('--d', (Math.min(order, 5) * 0.09).toFixed(2) + 's');
      targets.push(el);
    });
  });
  document.documentElement.classList.add('fx');

  /* 5-1. 요소 떠오르기: 화면에 처음 들어올 때 한 번 */
  const reveal = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const el = e.target;
      reveal.unobserve(el);
      el.classList.add('is-in');
      /* 등장이 끝나면 효과 클래스를 걷어내 카드의 hover 동작을 되돌림 */
      setTimeout(() => el.classList.remove('rv', 'is-in'), 1500);
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  targets.forEach(el => reveal.observe(el));

  /* 5-2. 제목 밑줄: 제목이 보일 때마다 다시 그려짐 (벗어나면 초기화) */
  const underline = new IntersectionObserver(entries => {
    entries.forEach(e => e.target.classList.toggle('drawn', e.isIntersecting));
  }, { threshold: 0.6, rootMargin: '0px 0px -8% 0px' });
  $$('h2').filter(h => !h.closest('dialog')).forEach(h => underline.observe(h));
})();
