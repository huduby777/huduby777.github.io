/* 공통 도우미 */
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

/* 2. 푸터 연도 자동 설정 */
const yearEl = $('#year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

/* 3. 네비게이션 활성화 감지 */
const navLinks = $$('.nav-links a');
const navSections = navLinks.map(link => $(link.hash)).filter(Boolean);
let pointerY = null;

function updateNav() {
  const y = pointerY ?? window.innerHeight * 0.35;
  const current = navSections.find(section => {
    const rect = section.getBoundingClientRect();
    return rect.top <= y && y < rect.bottom;
  });
  navLinks.forEach((link, i) => link.classList.toggle('is-active', navSections[i] === current));
}

document.addEventListener('pointermove', event => {
  pointerY = event.pointerType === 'mouse' && !event.target.closest('.site-header') ? event.clientY : null;
  if (pointerY !== null) updateNav();
});
document.addEventListener('mouseleave', () => { pointerY = null; updateNav(); });

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