# ✍️ AI 손글씨 행맨 - 손으로 쓴 영어 단어 게임

> Streamlit 캔버스에 알파벳을 쓰면 AI가 글자를 인식하고, 그 글자로 영어 단어를 맞히는 행맨 게임이다.

![AI 손글씨 행맨 화면](../../img/hang_img.png)

---

## 📌 프로젝트 개요

영어 단어를 외울 때 키보드로 알파벳을 고르는 대신 **직접 손으로 글자를 쓰고, 그 글자를 AI가 읽어 주는** 행맨 게임이다. 영어 단어 학습에 손글씨 입력을 결합해, 게임을 즐기면서 AI의 이미지 인식 기능도 체험할 수 있도록 했다.

글자 인식 모델은 EMNIST(손글씨 알파벳·숫자 데이터셋)로 직접 학습한 CNN이다. 중학생·고등학생 수준의 영어 단어 100개와 힌트를 준비했고, 오답 횟수에 따라 행맨 그림이 단계적으로 바뀐다.

## 🎯 프로젝트 목표

- EMNIST로 **CNN 손글씨 인식 모델을 직접 학습**하고 웹앱에 적용
- 캔버스 입력과 학습 데이터의 형태 차이를 **이미지 전처리**로 맞추는 방법 익히기
- 게임 상태(문제 · 맞힌 글자 · 오답 횟수)를 **`st.session_state`로 관리**
- 손글씨 입력을 결합해 영어 단어 학습을 **재미있게** 만들기

## 🛠 사용 기술

| 구분     | 기술                                                   |
| ------ | ---------------------------------------------------- |
| 언어 / 웹 | `Python` · `Streamlit` · `streamlit-drawable-canvas` |
| 딥러닝    | `TensorFlow / Keras` (CNN) · `EMNIST balanced`       |
| 이미지 처리 | `NumPy` · `Pillow`                                   |
| 데이터    | `JSON` (단어 100개 · 힌트 · 뜻)                            |

## ✨ 주요 기능

1. **손글씨 입력** - 캔버스에 마우스나 터치로 알파벳 한 글자를 작성
2. **AI 문자 인식** - 28×28 이미지로 변환해 CNN 모델이 알파벳을 예측 (확신도가 낮으면 다시 쓰도록 안내)
3. **단어 맞히기** - 힌트를 보고 글자를 제출하면 맞힌 글자가 단어에 표시
4. **진행 상황 표시** - 틀린 횟수(최대 5회)에 따라 행맨 이미지가 단계적으로 변경
5. **결과 안내** - 성공 또는 실패 메시지와 정답 단어·뜻을 표시
6. **새 게임** - 재시작하면 단어를 무작위로 다시 뽑고 진행 상태와 캔버스를 초기화

## 🔄 동작 흐름 (IPO)

```text
[INPUT]   캔버스에 손으로 쓴 알파벳 한 글자
   │
[PROCESS] ① 캔버스 이미지를 흑백으로 변환 → 글씨 영역을 잘라 정사각형으로 맞춤
   │      ② 28×28 리사이즈 (EMNIST 형식: 검은 배경 / 흰 글씨, 0~1 범위)
   │      ③ CNN 모델로 예측 → 알파벳 클래스 안에서 가장 높은 글자 선택
   │      ④ 확신도 확인 (낮으면 재입력 요청)
   │      ⑤ 정답 여부 판정 → 맞힌 글자 표시 / 틀린 횟수 증가
   │
[OUTPUT]  단어 진행 상황 / 틀린 횟수 / 행맨 이미지 / 성공·실패 메시지
```

## ⭐ 주요 함수 

* 중요한 함수들은 생성형 AI의 도움을 받아서 작성하였다.

| 함수 | 파일 | 역할 |
|---|---|---|
| **`preprocess_for_emnist(img_array)`** | `lib/conf.py` | 캔버스 이미지를 EMNIST 형식(28×28, 검은 배경·흰 글씨, 0~1)으로 변환 |
| **`predict_char(canvas_result)`** | `app.py` | 전처리 → 모델 예측 → 알파벳 클래스 안에서 선택 → 확신도 판단 |
| **`submit_letter(letter)`** | `app.py` | 중복·종료 후 제출 차단, 정답 여부 판정, 오답 횟수 · 게임 종료 처리 |
| **`new_game()`** | `app.py` | 단어를 다시 뽑고 진행 상태와 캔버스 초기화 |
| **`make_session(word)`** | `lib/conf.py` | `st.session_state`에 문제 · 오답 횟수 · 맞힌 글자 · 종료 여부 초기화 |
| **`load_model()`** / **`load_word_data()`** | `lib/conf.py` | `@st.cache_resource` / `@st.cache_data`로 모델과 단어 데이터를 한 번만 로드 |
| **`display_word(word, guessed_letters)`** | `lib/conf.py` | 맞힌 글자만 보이고 나머지는 `_`로 표시 |

## 💻 코드 스니펫

### 1. 이미지 전처리 — `preprocess_for_emnist()`

캔버스 이미지는 EMNIST와 모양이 달라서, 모델이 학습한 형태에 맞춰 변환한다.

```python
# 1. 배경이 밝으면 색 반전 (EMNIST는 검은 배경 + 흰 글씨)
if arr.mean() > 127:
    arr = 255 - arr

# 2. 이진화: 노이즈 제거
binary = np.where(arr > arr.mean() * 0.5, arr, 0)

# 3. 글씨 영역(bounding box)만 잘라내기
rows, cols = np.any(binary > 20, axis=1), np.any(binary > 20, axis=0)
rmin, rmax = np.where(rows)[0][[0, -1]]
cmin, cmax = np.where(cols)[0][[0, -1]]
cropped = binary[rmin:rmax + 1, cmin:cmax + 1]

# 4. 정사각형으로 패딩 (여백 20%, EMNIST 특유의 여백 재현)
size = max(cropped.shape)
pad = int(size * 0.2)
size += pad * 2

# 5. 28x28 리사이즈 → 0~1 범위
resized = Image.fromarray(square).resize((28, 28), Image.LANCZOS)
return (np.array(resized).astype(np.float32) / 255.0).reshape(28, 28, 1)
```

### 2. 알파벳만 선택 — `predict_char()`

모델은 숫자까지 47개 클래스를 출력하므로, 손글씨가 숫자로 인식되면 게임에 쓸 수 없다. **숫자 클래스를 제외한 알파벳 클래스 안에서만** 가장 높은 확률을 고르고, 확률 합이 1이 되도록 다시 계산해 확신도(0.4 이상)를 판단한다.

```python
prediction = model.predict(model_input, verbose=0)[0]

# 숫자 클래스를 제외하고 알파벳 클래스 안에서만 선택
letter_idx = [i for i, c in enumerate(lc.label_to_char) if c.isalpha()]
letter_probs = prediction[letter_idx]
letter_probs = letter_probs / letter_probs.sum()   # 알파벳끼리 합이 1이 되도록

best = int(np.argmax(letter_probs))
predicted_char = lc.label_to_char[letter_idx[best]].lower()
confidence = float(letter_probs[best])

return predicted_char if confidence >= 0.4 else ""   # 확신도가 낮으면 인식하지 않음
```

### 3. 입력 방향 보정 — `TRANSPOSE_INPUT`

학습 노트북이 EMNIST 이미지를 가로/세로 축을 바꿔(`tf.image.transpose`) 학습시켰기 때문에, 똑바로 쓴 글씨를 그대로 넣으면 인식되지 않았다. 그래서 모델 입력도 같은 방향으로 전치한다.

```python
TRANSPOSE_INPUT = True   # 방향 보정 없이 다시 학습한 모델이면 False

model_input = lc.preprocess_for_emnist(img_array).reshape(1, 28, 28, 1)
if TRANSPOSE_INPUT:
    model_input = model_input.transpose(0, 2, 1, 3)   # 가로/세로 축 교환
```

### 4. 게임 로직 — `submit_letter()`

```python
def submit_letter(letter):
    # 게임이 끝났거나 이미 제출한 글자는 처리하지 않음
    if st.session_state.game_over or letter in st.session_state.guessed_letters:
        return
    st.session_state.guessed_letters.append(letter)
    problem_word = st.session_state.problem["word"]

    if lc.check_letter(problem_word, letter):
        # 단어의 모든 글자를 맞히면 성공 종료
        if all(c in st.session_state.guessed_letters for c in problem_word):
            st.session_state.game_over = True
    else:
        st.session_state.wrong_count += 1
        if st.session_state.wrong_count >= lc.MAX_WRONG_COUNT:   # 오답 5회 → 실패 종료
            st.session_state.game_over = True
```

### 5. 캔버스 초기화 — `canvas_key`

제출 · 재시작 할 때마다 캔버스의 이전 글씨를 지우기 위해 st.session_state.canvas_key 번호를 바꿔서 새 캔버스를 만든다.

```python
canvas_result = st_canvas(
    stroke_width=10, stroke_color="white", background_color="black",
    height=210, width=210, drawing_mode="freedraw",
    key=f"hangman_canvas_{st.session_state.canvas_key}",
)
...
submit_letter(letter)
st.session_state.canvas_key += 1   # 다음 글자를 위해 캔버스 비우기
st.rerun()
```

## 🧠 손글씨 인식 모델 학습 — `emnist.ipynb`

| 항목 | 내용 |
|---|---|
| 데이터 | EMNIST balanced (47개 클래스: 숫자 10 + 알파벳 대문자 26 + 대소문자가 헷갈리는 소문자 11) |
| 데이터 크기 | 학습 112,800장 / 테스트 18,800장 |
| 모델 | Conv2D(32, 32, 64, 64, 128) + BatchNorm + Dropout + Dense(256) → softmax 47 (약 176만 파라미터) |
| 증강 | RandomRotation · RandomTranslation · RandomZoom |
| 학습 설정 | Adam, 최대 30 에포크, EarlyStopping · ReduceLROnPlateau · ModelCheckpoint |
| 결과 | 테스트 정확도 **85.96%** |

## 📁 폴더 구조

```text
03_project_hangman/
├── lib/
│   ├── conf.py                         # 문제·모델 불러오기, 세션 관리, 이미지 전처리 함수
│   ├── hangman_words.json              # 단어 데이터
│   └── emnist_balanced_cnn_0811.keras  # 학습한 손글씨 인식 모델
├── static/img/                         # 행맨 단계별 이미지 (img_{난이도}{오답횟수}.png)
├── emnist.ipynb                        # 모델 학습 노트북
├── app.py                              # Streamlit 웹앱 시작 파일
└── requirements.txt
```

## 🚀 실행 방법

```bash
conda create -n hangman_env python=3.11
conda activate hangman_env
pip install -r requirements.txt
streamlit run app.py
```

## ⚠️ 한계 · 🔭 향후 계획

- EMNIST(가는 획의 필기체)로 학습했고 캔버스는 굵은 획이라, 글자를 작게 쓰거나 획이 겹치면 인식률이 떨어진다. `b/h`, `n/h`, `u/v` 등 비슷한 글자를 혼동하기도 한다.
- 테스트 정확도(85.96%)는 EMNIST 데이터 기준이며, 실제 마우스 입력 정확도는 별도로 측정하지 않았다.
- 향후: 난이도 선택(중학생 / 고등학생) / 방향 변환 제거 후 재학습 · 굵은 획 증강 · 직접 쓴 글씨로 미세조정 / 글자별 인식 성공률 측정