/* 1. 프로젝트 상세 내용  */
const projects = {
  maeum: {
    category: 'AI · STREAMLIT · EMOTION', title: '마음 봄 — AI 감정 기록 앱',
    details: [
      ['', '하루의 마음을 글로 기록하고, AI가 분류한 감정과 공감 메시지를 통해 자신의 감정을 돌아보는 웹앱입니다. ‘마음의 고백’과 ‘감정 보듬기’ 두 공간으로 구성하여, 기록부터 감정 분포 확인까지 자연스럽게 이어지도록 제작했습니다.'],
      ['주요 기능', '■ 마음 기록: 오늘의 경험과 감정을 문장으로 입력하면 작성 날짜, 내용, 감정 분류 결과를 Google Sheets에 저장합니다.\n' +
                   '■ AI 감정 분류: 손질된 감정 분류 모델로 입력 문장을 분석하고, 가장 높은 예측 확률의 감정 결과를 기록에 활용합니다.\n' +
                   '■ 최근 기록 조회: 최근 마음 기록 5개를 날짜, 감정 이름, 날씨 아이콘과 함께 표시합니다.\n' + 
                   '■ 마음 기후 시각화: 기쁨·당황·분노·불안·상처·슬픔의 6가지 주요 감정 분포를 백분율과 막대로 보여줍니다.\n' + 
                   '■ 공감 메시지 생성: 감정 분포와 가장 최근 기록을 바탕으로 마음을 표현하는 제목, 따뜻한 메시지, 일상에서 시도할 작은 실천 제안을 제공합니다.'],  
      ['AI 분석 및 데이터 처리', '입력 문장을 토큰화한 뒤, 학습된 LoRA 어댑터를 적용한 KLUE RoBERTa 모델로 감정을 분류합니다. 분류 결과는 주요 감정과 세부 감정으로 나누어 Google Apps Script를 통해 Google Sheets에 저장합니다.\n저장된 기록은 Pandas로 집계하고, 감정 요약 정보와 최근 작성 문장을 OpenAI API에 전달하여 공감 메시지를 생성합니다.'],
      ['사용 기술','Python, Streamlit, KLUE RoBERTa, OpenAI API, Pandas, Google Sheets, Google Apps Script, HTML·CSS'],
      ['구현 포인트','감정 분류 모델과 공감 문구를 생성하는 AI의 역할을 나누어 구성했습니다. 감정 분포는 날씨 아이콘과 막대로 표현하여 사용자가 자신의 기록을 쉽게 살펴볼 수 있도록 했습니다.' + 
                    '데이터 캐시와 세션 상태를 활용하여 반복 조회와 API 호출을 줄이고, 새 기록을 저장하면 데이터를 다시 불러와 공감 메시지를 갱신하도록 구현했습니다. 메시지 생성 프롬프트에는 의학적 진단이나 단정적인 표현을 피하고, 감정을 좋고 나쁨으로 판단하지 않도록 기준을 명시했습니다.']
    ],
    img:"../img/mind_img.png"
  },
  news: {
    category: 'AI · STREAMLIT · NEWS', title: '오늘의 AI 뉴스 — AI 뉴스 큐레이션',
    details: [
      ['', 'AI 뉴스를 수집하고, GPT API를 활용해서 주요 기사를 선별·요약하여 카드뉴스로 제공하는 웹앱입니다. 복잡한 AI 동향을 빠르게 파악하고, 뉴스와 관련된 용어를 함께 학습할 수 있도록 제작했습니다.'],
      ['주요 기능', '■ 뉴스 수집: AI타임즈 RSS에서 최대 20개의 기사 제목, 요약, 발행일과 원문 링크를 가져옵니다.\n' +
                   '■ 주요 뉴스 선정: 중요도, 최신성, 대중성, 다양성, 교육적 가치, 신뢰성을 기준으로 AI가 TOP 6 뉴스를 선정하도록 구성했습니다.\n' +
                   '■ 카드뉴스 구성: 선정된 뉴스의 짧은 제목, 한 줄 요약, 중요성, 키워드와 카테고리 등을 생성하여 카드뉴스로 제공합니다.\n' + 
                   '■ 오늘의 핵심 흐름: 선정된 뉴스 전체를 아우르는 핵심 메시지와 선정 기준을 안내합니다.\n' + 
                   '■ AI·IT 용어 학습: 뉴스와 관련된 용어 하나를 선정하여 중학생도 이해할 수 있는 짧은 설명을 제공합니다.\n' + 
                   '■ 지난 브리핑 조회: 날짜별로 저장한 결과를 사이드바에서 선택하여 다시 확인할 수 있습니다.'],  
      ['데이터 처리 과정', '앱 실행 시 당일 저장된 브리핑이 없으면 RSS 뉴스를 수집하고 OpenAI API에 선별과 요약을 요청합니다. 생성 결과를 JSON 파일로 저장한 뒤 HTML 템플릿을 통해 화면에 표시하며, 이미 저장된 브리핑은 재사용하여 반복적인 API 호출을 줄입니다.'],
      ['사용 기술','Python, Streamlit, OpenAI API, Feedparser, JSON, HTML·CSS'],
      ['구현 포인트','뉴스 수집, AI 콘텐츠 생성, 날짜별 저장, 화면 출력을 연결했습니다. 데이터 처리 함수와 화면 템플릿을 분리하여 기능과 디자인을 각각 수정하기 쉽도록 구성했습니다.\n'+
                    '또한 기사 제목과 RSS 요약을 근거로 내용을 작성하고, 원문 링크를 유지하며, 특정 주제에 편중되지 않도록 프롬프트에 기준을 명시했습니다. 개인정보, 편향, 저작권 등 뉴스와 관련된 윤리적 고려사항도 함께 생성하도록 설계했습니다.']
    ],
    img:"../img/news_img.png"
  },
  hangman: {
    category: 'AI · PYTHON · GAME', title: 'AI 손글씨 행맨',
    details: [
      ['', '사용자가 직접 쓴 알파벳을 AI가 인식하여 단어를 맞히는 행맨 게임입니다. 영어 단어 학습에 손글씨 입력을 결합하여, 게임을 즐기며 AI의 이미지 인식 기능을 체험할 수 있도록 제작했습니다.'],
      ['주요 기능', '■ 손글씨 입력: 화면의 캔버스에 마우스나 터치로 알파벳 한 글자를 작성합니다.\n' +
                   '■ AI 문자 인식: 제출한 손글씨를 EMNIST 기반 모델로 분석하여 게임에 사용할 문자를 추출합니다.\n' +
                   '■ 단어 맞히기: 힌트를 참고하여 알파벳을 제출하고, 맞힌 글자를 화면에서 확인합니다.\n' + 
                   '■ 진행 상황 표시: 오답 횟수에 따라 행맨 이미지가 단계적으로 변경되며, 제한 횟수에 도달하면 게임이 종료됩니다.\n' + 
                   '■ 새 게임 시작: 게임 종료 후 재시작 버튼을 누르면 현재 난이도의 단어 중 하나를 무작위로 선택하고 진행 상태를 초기화합니다.'],      
      ['AI 인식 과정', '캔버스 이미지를 흑백으로 변환하고, 전처리 함수를 거쳐 28×28 크기의 모델 입력으로 구성합니다.\n' + 
                      '모델이 출력한 예측 확률 중 가장 높은 값이 70% 이상인 경우에만 인식 결과를 사용하며, 조건을 충족하지 못하면 다시 작성하도록 안내합니다.' + 
                      '숫자 0과 5의 인식률이 매우 낮아 각각 알파벳 o와 s로 보정하여 게임 입력에 활용합니다.'],
      ['사용 기술', 'Python, Streamlit, streamlit-drawable-canvas, NumPy, Pillow, EMNIST 기반 손글씨 인식 모델'],
      ['구현 포인트','손글씨 입력, 이미지 전처리, AI 추론, 게임 판정, 화면 갱신을 하나의 흐름으로 연결했습니다. Streamlit의 세션 상태를 활용하여 화면이 재실행되어도 현재 문제, 맞힌 글자, 오답 횟수와 게임 종료 여부가 유지되도록 구현했습니다.']           
    ],
    img:"../img/hang_img.png"
  },
  iot: {
    category: 'PYTHON · ARDUINO · 공공데이터', 
    title: '스마트 버스 정류소 안내 시스템',
    details: [
      ['', '공공데이터 API와 아두이노를 연동한 버스 도착 안내 프로젝트입니다. 큰 글자 모드와 저상버스 구분 표시를 적용하여, 교통약자를 비롯한 다양한 이용자가 버스 정보를 쉽게 확인할 수 있도록 구성했습니다.'],
      ['주요 기능', '◼ 실시간 도착 정보: TAGO API에서 버스 정보를 30초마다 조회하여 노선별 도착 예정 시간과 차량 유형을 표시합니다.\n' +
                   '◼ 도착 임박 안내: 도착까지 1분 이하로 남은 버스를 별도 영역에 강조합니다.\n' +
                   '◼ 큰 글자 모드: 버튼을 누르면 글자 크기와 화면 배치를 변경하여 정보를 크게 보여줍니다.\n' + 
                   '◼ 저상버스 구분: 차량 유형을 색상과 텍스트로 표시하여 저상버스 여부를 쉽게 확인하도록 했습니다.\n'],
      ['데이터 처리 및 기기 연동','동일 노선의 여러 버스 중 가장 먼저 도착하는 차량을 선택하고, 도착 예정 시간이 짧은 순서로 정렬합니다.\n 이 중 상위 2대의 노선번호, 도착까지 남은 시간, 남은 정류장 수를 JSON으로 구성하여 USB 시리얼 통신으로 아두이노에 전송합니다.\n'],                   
      ['아두이노 연동 및 LCD 출력','Python에서 가공한 버스 도착 정보를 USB 시리얼 통신으로 아두이노에 전달하고, 16×2 I2C LCD에 표시합니다.\n' +
                                '■ 데이터 수신: 줄바꿈 문자를 기준으로 JSON 데이터를 수신하고, 노선번호·도착예정시간·남은 정류장 수를 추출합니다.\n' +
                                '■ 도착 시간 변환: 초 단위 도착 시간을 분 단위로 올림 처리하여 표시합니다.\n' +
                                '■ LCD 안내: Python에서 전송한 최대 2대의 버스 정보를 LCD의 각 행에 출력합니다.\n' +
                                '■ 화면 갱신: 새로운 데이터를 수신하면 기존 화면을 지우고 최신 정보로 교체합니다.\n' +
                                '■ 오류 확인: JSON 해석에 실패하면 시리얼로 오류 메시지를 출력합니다.\n'],
      ['사용 기술','Python, Streamlit, Pandas, Requests, TAGO OpenAPI, PySerial, Arduino'],
      ['구현 포인트','공공데이터 조회부터 데이터 가공, 웹 화면 표시, 하드웨어 전송까지 하나의 흐름으로 연결했습니다. \n Streamlit의 주기적 갱신 기능과 세션 상태를 활용하여 도착 정보를 업데이트하고 글자 모드를 전환하도록 구현했습니다.']     
    ],
    img:"../img/bus_img.png"
  }
};

/* 2. 공통 도우미 */
const $ = selector => document.querySelector(selector);
const $$ = selector => [...document.querySelectorAll(selector)];
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

/* 3. 프로젝트 팝업 */
const dialog = $('#project-dialog');

// 상세 항목 한 줄: 왼쪽 제목 + 오른쪽 내용 ('■ 제목: 설명' 줄은 번호를 붙여 표시)
function makeDetailRow([heading, description]) {
  const body = el('div', 'detail-body');
  let count = 0;
  description.split('\n').map(line => line.trim()).filter(Boolean).forEach(line => {
    if (!/^[■◼]/.test(line)) return body.append(el('p', '', line));

    const text = line.replace(/^[■◼]\s*/, '');
    const [, title, desc] = text.match(/^(.*?):\s*(.*)$/) || [];
    const content = el('span');
    if (title) content.append(el('b', '', title), ` · ${desc}`);
    else content.textContent = text;

    const item = el('div', 'detail-item');
    item.append(el('em', '', String(++count).padStart(2, '0')), content);
    body.append(item);
  });

  const row = el('div', 'detail-row');
  row.append(el('div', 'detail-label', heading || '프로젝트 소개'), body);
  return row;
}

function openProject(project) {
  const image = el('img');
  image.src = project.img;
  image.alt = project.title;

  $('#dialog-category').textContent = project.category;
  $('#dialog-title').textContent = project.title;
  $('#dialog-img').replaceChildren(image);
  $('#dialog-details').replaceChildren(...project.details.map(makeDetailRow));
  dialog.showModal();
}
$('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  if (event.target === dialog) dialog.close();   // 바깥 어두운 영역을 누르면 닫기
});

/* 4. 프로젝트 목록(탭) ↔ 미리보기 ↔ 자세히 보기
      HTML의 순서(탭 1~4, 미리보기 1~4)가 projects의 순서와 같다는 점을 이용합니다. */
const projectTabs = $$('.project-tab');
const projectPanes = $$('.project-pane');
const projectList = Object.values(projects);

function selectProject(index) {
  projectTabs.forEach((tab, i) => {
    tab.classList.toggle('is-active', i === index);
    tab.setAttribute('aria-current', i === index);
  });
  projectPanes.forEach((pane, i) => { pane.hidden = i !== index; });
}
projectTabs.forEach((tab, i) => {
  ['click', 'mouseenter', 'focus'].forEach(type => tab.addEventListener(type, () => selectProject(i)));
});
projectPanes.forEach((pane, i) => {
  pane.querySelector('.project-more').addEventListener('click', () => openProject(projectList[i]));
});

/* 5. 푸터 연도 */
$('#year').textContent = new Date().getFullYear();

/* 6. 왼쪽 메뉴: 마우스가 올라간 섹션(마우스가 없으면 화면 위쪽 35% 지점의 섹션)을 표시 */
const navLinks = $$('.nav-links a');
const navSections = navLinks.map(link => $(link.hash));
let pointerY = null;   // 마우스가 본문 위에 있을 때의 세로 위치

function updateNav() {
  const y = pointerY ?? window.innerHeight * 0.35;
  const current = navSections.find(section => {
    const rect = section.getBoundingClientRect();
    return rect.top <= y && y < rect.bottom;
  });
  navLinks.forEach((link, i) => link.classList.toggle('is-active', navSections[i] === current));
}

// 마우스 이동: 본문 위에서는 그 위치를 기준으로, 왼쪽 메뉴 위에서는 현재 표시를 유지
document.addEventListener('pointermove', event => {
  pointerY = event.pointerType === 'mouse' && !event.target.closest('.site-header') ? event.clientY : null;
  if (pointerY !== null) updateNav();
});
document.addEventListener('mouseleave', () => { pointerY = null; updateNav(); });

/* 7. 스크롤: TOP 버튼 표시 + 왼쪽 메뉴 갱신 */
const topButton = $('#back-to-top');
function onScroll() {
  topButton.classList.toggle('is-visible', window.scrollY > 280);
  updateNav();
}
window.addEventListener('scroll', onScroll, { passive: true });
window.addEventListener('resize', updateNav);
topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
onScroll();
