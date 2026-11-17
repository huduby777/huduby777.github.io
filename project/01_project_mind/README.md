# 🌱 마음 봄 — AI 감정 기록 · 회고 웹앱

> 하루의 마음을 한 문장으로 기록하면, AI가 감정을 분류하고 따뜻한 회고 메시지를 건네주는 감정 케어 웹앱입니다.

![마음 봄 화면](../../img/mind_img.png)

- **과목**: 라즈베리파이-AI실험 과제 (인공지능 학과)
- **개발자**: 이미경
- **소스 코드**: _(GitHub 주소 입력)_

---

## 📌 프로젝트 소개

학업, 친구 관계, 진로, 가족 갈등 등으로 마음이 힘들어도 자신의 감정을 말로 꺼내거나 정확히 정리하기는 쉽지 않습니다. 고등학생 딸이 감정적으로 힘들어하는 모습을 보며 **"감정을 기록하고 스스로 돌아볼 수 있는 앱"** 의 필요성을 느꼈고 대학 과제로 프로토 타입을 제작하게 되었습니다..

사용자가 오늘의 기분이나 있었던 일을 입력하면 직접 학습한 LoRA 감정 분류 모델이 감정을 분류해서 Google Sheets에 저장하고, 최근 30일의 기록을 바탕으로 OpenAI API가 부드러운 회고 문장과 작은 실천 제안을 만들어 줍니다.

앱은 두 개의 공간으로 구성됩니다.

| 탭             | 설명                                                 |
| -------------------- | -------------------------------------------------- |
| 💭 **마음의 고백** | 오늘의 마음을 문장으로 기록하고, 최근 기록 5개를 날짜·감정·날씨 아이콘과 함께 확인   |
| 🌈 **감정 보듬기** | 최근 30일 감정 분포를 막대로 확인하고, AI가 작성한 공감 레터와 작은 실천 제안 확인 |

## ✨ 주요 기능

1. **마음 기록** - 입력한 문장과 날짜, 감정 분류 결과를 Google Sheets에 저장
2. **AI 감정 분류** - LoRA를 적용한 KLUE RoBERTa 모델이 가장 확률이 높은 감정을 예측
3. **최근 기록 조회** - 최근 5개의 기록을 감정별 날씨 아이콘과 함께 표시
4. **마음 기후 시각화** - 기쁨·당황·분노·불안·상처·슬픔 6가지 감정 분포를 백분율과 막대로 표시
5. **공감 메시지 생성** - 감정 분포와 가장 최근 기록을 바탕으로 제목 · 따뜻한 메시지 · 작은 실천 제안 제공

## 🔄 동작 흐름 (IPO)

```text
[INPUT]   오늘의 감정 문장 입력
   │
[PROCESS] ① LoRA 감정 분류 모델 → emotion1(대분류), emotion2(세부 감정) 분류
   │      ② Google Apps Script(doPost)로 Google Sheet에 저장
   │      ③ Google Apps Script(doGet)로 최근 30일 기록 조회 → 감정 비율 계산 (Pandas)
   │      ④ OpenAI API로 공감 레터 · 실천 제안 생성
   │
[OUTPUT]  감정 분류 결과 / 마음 상태 분포 / 공감 레터 / 작은 실천 제안
```

## 🛠 사용 기술

`Python` · `Streamlit` · `KLUE RoBERTa (klue/roberta-base)` · `LoRA (PEFT)` · `PyTorch / Transformers` · `OpenAI API` · `Pandas` ·  `Google Apps Script` · `HTML·CSS`

## 📁 폴더 구조

```text
01_project_mind/
├── .streamlit/
│   ├── config.toml      # 정적 파일 제공 기능 켜기
│   └── secrets.toml     # Google Apps Script URL, OpenAI API Key (※ 공개 저장소에 올리지 않기)
├── lora_model/          # LoRA 학습 결과 (adapter, tokenizer, label_map)
├── static/              # 감정 아이콘 SVG 파일
├── lib/
│   ├── emotion.py       # LoRA 모델 로드 및 감정 예측 함수
│   └── fun_lib.py       # Google Sheet 연동, GPT 리포트, HTML 컴포넌트 함수
└── main.py              # Streamlit 웹앱 시작 파일
```

## 🚀 실행 방법

```bash
# 1. 아나콘다 가상환경 생성 및 활성화
conda create -n mind_env python=3.11
conda activate mind_env

# 2. 패키지 설치
pip install streamlit pandas numpy torch transformers peft accelerate safetensors openai requests torchvision

# 3. 실행
streamlit run main.py
```

`.streamlit/secrets.toml`에 아래 값을 설정해야 합니다. (키 이름은 `lib/fun_lib.py` 기준)

```toml
[openai]
api_key = "YOUR_OPENAI_API_KEY"

[google_sheet]
app_script_url = "YOUR_GOOGLE_APPS_SCRIPT_WEB_APP_URL"
```

---

## 🧠 핵심 구현 설명

### 💡 LoRA란?

**LoRA(Low-Rank Adaptation)** 는 이미 만들어진 모델을 적은 비용으로 내 데이터에 맞게 학습시키는 **파인튜닝 방식**입니다. 모델 전체를 바꾸지 않고 작은 어댑터만 학습합니다. 이처럼 일부 파라미터만 학습하는 파인튜닝을 **PEFT(Parameter-Efficient Fine-Tuning, 파라미터 효율적 미세조정)** 라고 하며, LoRA는 대표적인 PEFT 방법입니다. 이 프로젝트에서는 Hugging Face의 `peft` 라이브러리로 LoRA를 적용했습니다.

| 구분 | 이 프로젝트에서의 대상 |
|----------|----------|
| **기반 모델** | `klue/roberta-base` — 한국어를 미리 학습한 언어 모델 (수억 개 규모의 파라미터) |
| **학습 방법** | **LoRA** — 기반 모델을 60개 감정 분류용으로 맞추는 미세조정(fine-tuning) 기법 |
| **학습 결과물** | LoRA 어댑터 (`lora_model/adapter_model.safetensors`, 약 3.7MB) |

**일반 미세조정과의 차이**

```text
[전체 미세조정]  모델의 모든 가중치를 다시 학습   → GPU 메모리·시간 많이 필요, 결과 파일도 모델 크기
[LoRA]          기존 가중치는 고정(freeze)
                + 옆에 붙인 작은 행렬(어댑터)만 학습 → 학습 대상 파라미터가 훨씬 적고, 결과 파일도 작음
```

학습할 파라미터가 크게 줄어 Colab T4 같은 일반 GPU에서도 학습할 수 있습니다.

**이 프로젝트의 LoRA 설정 (`adapter_config.json`)**

| 설정 | 값 | 의미 |
|----------|---|----------|
| `r` | 8 | 어댑터 행렬의 크기(rank). 작을수록 가볍지만 표현력은 낮아짐 |
| `lora_alpha` | 16 | 어댑터가 모델에 미치는 영향의 크기를 조절 |
| `lora_dropout` | 0.1 | 과적합을 줄이기 위한 드롭아웃 |
| `target_modules` | `query`, `value` | 어댑터를 붙인 곳 — 문장 속 단어 관계를 파악하는 어텐션 층 |
| `modules_to_save` | `classifier` | 60개 감정을 고르는 마지막 분류층은 어댑터 없이 직접 학습 |
### 1. LoRA 감정 분류 모델 학습

| 항목      | 내용                                                                                                                              |
| ------- | ------------------------------------------------------------------------------------------------------------------------------- |
| 기반 모델   | `klue/roberta-base`                                                                                                             |
| 학습 데이터  | AI Hub의 [감성대화말뭉치](https://www.aihub.or.kr/aihubdata/data/view.do?currMenu=115&topMenu=100&aihubDataSe=data&dataSetSn=86) 데이터 사용 |
| 레이블 수   | 60개 (`대분류_세부감정` 형태, 예: `기쁨_감사하는`)                                                                                               |
| LoRA 설정 | `r=8`, `lora_alpha=16`, `lora_dropout=0.1`, 대상 모듈 `query`·`value`, `task_type=SEQ_CLS`                                          |
| 학습 환경   | Google Colab (GPT·Claude로 생성한 코드를 활용해 완성)                                                                                       |

학습 결과로 `adapter_model.safetensors`, `adapter_config.json`, `label_map.json`, `tokenizer.json`, `tokenizer_config.json`이 생성되며 `lora_model/`에 저장됩니다.

#### 학습 데이터 정제 

이 데이터는 상담 대화 형태라서 그대로 분류 모델 학습에 쓰기 어렵습니다. 노트북(Google Colab)에서 **사용자(사람)의 발화만 하나의 문장으로 합치고**, **감정 라벨을 `대분류_소분류` 하나로 합쳐** 학습용 CSV로 만들었습니다.

**① 원본 데이터 형태** (13개 컬럼, 한 행이 상담 대화 한 건)

| 연령 | 성별 | 상황키워드 | 신체질환 | 감정_대분류 | 감정_소분류 | 사람문장1 | 시스템문장1 | 사람문장2 | 시스템문장2 | 사람문장3 | 시스템문장3 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 청년 | 여성 | 진로,취업,직장 | 해당없음 | 분노 | 노여워하는 | 일은 왜 해도 해도 끝이 없을까? 화가 난다. | 많이 힘드시겠어요. 주위에 의논할 상대가 있나요? | 그냥 내가 해결하는 게 나아. 남들한테 부담 주고 싶지도 않고. | 혼자 해결하기로 했군요. … | NaN | NaN |

- 사람 발화는 최대 3턴(`사람문장1~3`)이며, 3번째 턴이 없는 대화는 `NaN`입니다.
- 시스템(챗봇) 응답, 신체질환 등 감정 분류에 필요 없는 컬럼이 포함되어 있습니다.
- 필요한 컬럼 ( 연령, 성별, 상황키워드, 사람문장, emotion )만 남겨 CSV로 저장하였습니다.

**② 정제 결과 (`emotion_final.csv`)**

| 연령 | 성별 | 상황키워드 | 사람문장 | emotion |
|---|---|---|---|---|
| 청년 | 여성 | 진로,취업,직장 | 일은 왜 해도 해도 끝이 없을까? 화가 난다. 그냥 내가 해결하는 게 나아. 남들한… | 분노_노여워하는 |
| 청년 | 여성 | 진로,취업,직장 | 이번 달에 또 급여가 깎였어! 물가는 오르는데 월급만 자꾸 깎이니까 너무 화가 나. 최대한 지출을… | 분노_노여워하는 |
| 청년 | 여성 | 진로,취업,직장 | 회사에 신입이 들어왔는데 말투가 거슬려. 그런 애를 매일 봐야 한다고 생각하니까 스… | 분노_노여워하는 |

| 구분 | 정제 전 | 정제 후 |
|---|---|---|
| 컬럼 수 | 13개 | 5개 |
| 학습 문장 | 사람 발화가 1~3개 컬럼에 분산 | `사람문장` 1개 컬럼 |
| 감정 라벨 | `감정_대분류`, `감정_소분류` 2개 | `emotion` 1개 (60종, 대분류 6종: 기쁨·당황·분노·불안·상처·슬픔) |
| 데이터 크기 | 51,630행 (노트북 실행 기준) | 51,630행 × 5컬럼 |

**③ 데이터의 한계**

- **데이터 양**: 약 5만 건(51,630건)으로 60개 레이블을 학습해야 해서, 레이블당 평균 약 860건에 불과합니다. 이 정도 규모로는 좋은 성능의 분류 모델을 만들기 어려웠습니다.
- **라벨의 모호함**: 감정 소분류(예: `당황_외로운`, `불안_두려운`)는 사람이 봐도 구분하기 미묘하고, 한 문장에 여러 감정이 섞여 있는 경우가 많습니다. 정제 과정에서 두세 번의 발화를 하나로 합쳤지만 라벨 자체가 가진 모호함은 해소되지 않았습니다.
- 그래서 정확한 감정 진단 모델이 아니라, 사용자가 자신의 감정을 돌아보도록 돕는 **참고용 분류 결과**로 활용했습니다.

### 2. 감정 예측 

기반 모델 위에 학습된 LoRA 어댑터를 붙여 추론합니다. 입력 문장을 토큰화한 뒤 확률이 가장 높은 `top_k`개의 감정을 반환합니다.

```python
# 기본 분류 모델 위에 학습된 LoRA adapter를 붙입니다.
base_model = AutoModelForSequenceClassification.from_pretrained(
    BASE_MODEL_NAME, num_labels=num_labels, id2label=id2label, label2id=label2id
)
model = PeftModel.from_pretrained(base_model, MODEL_DIR)
model.to(device)
model.eval()

def predict_emotion(text: str, top_k: int = 3):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)

    probs = torch.softmax(outputs.logits, dim=-1)[0]          # logits → 확률
    top_probs, top_indices = torch.topk(probs, k=top_k)       # 상위 k개 추출

    return [{"emotion": id2label[int(i)], "score": float(p)}
            for p, i in zip(top_probs, top_indices)]
```

- 예측 라벨은 `기쁨_감사하는`처럼 **대분류_세부감정** 형태입니다.
- GPU가 있으면 `cuda`, 없으면 `cpu`에서 자동으로 실행됩니다.

### 3. Google Sheets 저장 · 조회

Google Apps Script를 웹앱으로 배포해 Streamlit과 데이터를 주고받습니다.

- `doPost(e)` : 전달받은 데이터를 시트(`Sheet1`)에 입력
- `doGet(e)` : 시트에서 최근 30일 데이터를 읽어 JSON으로 반환

```python
def save_emotion_log(txt, lora_data, weather=""):
    url = st.secrets["google_sheet"]["app_script_url"]
    emotion_text = lora_data[0]["emotion"]          # 예: "슬픔_우울한"
    emotion1, emotion2 = emotion_text.split("_")    # 대분류 / 세부 감정 분리

    data = {
        "regist_dt": datetime.now().strftime("%Y-%m-%d"),
        "text": txt,
        "emotion1": emotion1,
        "emotion2": emotion2,
    }
    response = requests.post(url, json=data, timeout=10)
    return response.status_code == 200
```

### 4. OpenAI 공감 레터 생성 

감정 분류(LoRA)와 문장 생성(GPT)의 역할을 나누었습니다. 모델에는 **감정 요약과 가장 최근 문장**만 전달하며, 프롬프트에 안전 기준을 명시했습니다.

```python
response = client.responses.create(model="gpt-5-mini", input=prompt)
return response.output_text   # {"title", "message", "suggestion"} JSON
```

프롬프트의 주요 작성 규칙은 다음과 같습니다.

- 청소년 감정 기록 앱에 어울리게 **따뜻하고 다정하게** 작성
- 의학적 진단·치료·우울증 판정처럼 말하지 않기, "너는 ~ 상태야" 식으로 **단정하지 않기**
- "보여요", "느껴질 수 있어요" 같은 **부드러운 표현** 사용
- 숫자·퍼센트·기록 개수를 문장에 직접 쓰지 않기, 감정을 **좋고 나쁨으로 판단하지 않기**
- 감정 흐름을 날씨·계절 같은 이미지로 표현해도 좋음
- 결과는 아래 **JSON 형식**으로 출력

```json
{
  "title": "짧은 제목",
  "message": "최근 감정 흐름에 대한 따뜻한 해석. 2문장 이내.",
  "suggestion": "오늘 바로 해볼 수 있는 작은 실천 제안. 1문장."
}
```

### 5. 캐시와 세션 상태로 API 호출 줄이기

Streamlit은 화면이 갱신될 때마다 코드를 처음부터 다시 실행하기 때문에, 그대로 두면 Google Sheet 조회와 GPT 호출이 반복됩니다. 이를 `cache_data`와 `session_state`로 해결했습니다.

```python
# GPT 호출 여부 / 결과를 세션에 저장
if "init_report_done" not in st.session_state:
    st.session_state.init_report_done = False
if "report" not in st.session_state:
    st.session_state.report = None

# 구글 시트 데이터를 60초 동안 캐시
@st.cache_data(ttl=60)
def load_emotion_log_cached():
    return fl.load_emotion_log()
```

```python
# 새 마음을 기록하면 캐시를 비우고, GPT 리포트를 다시 만들도록 표시
success = fl.save_emotion_log(mind_text, em.predict_emotion(mind_text, top_k=1))
if success:
    st.cache_data.clear()                      # 시트에서 데이터를 다시 가져오도록
    st.session_state.init_report_done = False  # GPT 리포트 재생성
```

```python
# 아직 리포트를 만들지 않았을 때만 GPT API 호출
if not st.session_state.init_report_done:
    data = fl.generate_emotion_report_with_gpt(summary, recent_text, 30)
    st.session_state.report = data
    st.session_state.init_report_done = True
```

→ 최초 호출은 다소 느리지만, 이후에는 API 호출 횟수와 응답 시간을 줄일 수 있습니다.

### 6. 감정 분포 계산 및 시각화

저장된 기록을 Pandas로 집계해 6가지 주요 감정의 비율을 구하고, HTML/CSS 막대로 렌더링합니다.

```python
df_emotion = df.groupby("emotion1")["emotion2"].count()
max_emotion = df_emotion.idxmax()               # 가장 많이 나타난 감정

for key, item in fl.emotion.items():            # {"기쁨": "🌞", ...}
    cnt = df_emotion[key] if key in df_emotion.index else 0
    percent = int((cnt / total_cnt) * 100)
    # ... 감정 이름 + 퍼센트 + 막대(width:{percent}%) HTML 생성
st.markdown(str_html, unsafe_allow_html=True)   # Streamlit 안에 HTML 삽입
```

화면 구성에는 `st.tabs(["💭 마음의 고백", "🌈 감정 보듬기"])`와 `st.markdown(..., unsafe_allow_html=True)`를 사용했습니다.

---

## 🧗 어려웠던 점과 해결

| 문제                                                                  | 해결                                                              |
| ------------------------------------------------------------------- | --------------------------------------------------------------- |
| 학습 데이터 감정 표현의 다양성이 부족하고 하드웨어 사양 부족으로 충분한 학습 데이터를 사용하지 못해 모델 정확도에 한계 | 완벽한 분류보다 **스스로 돌아보도록 돕는 방향**으로 목표를 조정하고, 결과를 진단이 아닌 "참고 정보"로 제시 |
| Streamlit 재실행으로 불필요한 API 호출 발생                                      | `st.session_state`로 상태 유지, `st.cache_data`로 시트 조회 횟수 감소         |
| OpenAI API 사용량 제한으로 오류 가능성                                          | 꼭 필요한 시점(최초 접속 · 새 기록 저장)에만 GPT를 호출하도록 로직 수정                    |

## 🔭 향후 개선점

- 기회가 된다면 더 많은 데이터를 모아서 모델을 성능 향상
- 감정 털어내기, 위로 받기, 마음 돌보기 기능 추가.
- 안정적인 오류 처리와 사용자 경험 개선

## 📝 한계 및 유의 사항

- 감정 분류 모델은 학습 데이터(약 5만 건)가 60개 레이블을 학습하기에 부족하고, 감정 소분류 자체가 구분하기 미묘하며 하드웨어 한계도 있어 항상 정확하지 않습니다. 결과는 **진단이 아닌 참고용**입니다.
- 이 앱은 의료·상담 서비스를 대체하지 않습니다.
- `secrets.toml`에는 API 키가 포함되므로 GitHub에 올리지 마세요 (`.gitignore`에 추가 권장).
