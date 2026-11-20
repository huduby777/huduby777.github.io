import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import random
import lib.conf as lc

st.set_page_config(page_title="행맨", page_icon="⏳")

# 모델이 전치(transpose)된 EMNIST 이미지로 학습되어, 입력도 같은 방향으로 맞춤.
# 노트북에서 transpose를 빼고 다시 학습한 모델을 쓸 때는 False로 바꾸세요.
TRANSPOSE_INPUT = True

# 문제 가져오기
word = lc.load_word_data()

# 페이지 세션 가져오기
lc.make_session(word)

# 캔버스 초기화용 번호 (번호가 바뀌면 새 캔버스가 만들어져 이전 글씨가 지워짐)
if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = 0

# emnist 모델 가져오기
model = lc.load_model()

def predict_char(canvas_result):
    rgba = canvas_result.image_data.astype("uint8")
    rgb = rgba[..., :3].astype("float32")
    alpha = rgba[..., 3:4].astype("float32") / 255.0

    # 투명한 부분은 흰색(255)으로, 불투명한 부분(그린 획)은 원래 RGB(검정)로 합성
    composited = (rgb * alpha + 255 * (1 - alpha)).astype("uint8")
    img_array = np.array(Image.fromarray(composited).convert("L")).astype("float32")

    # 캔버스에 아무것도 안 그렸으면 예측하지 않음
    if img_array.max() == 0:
        return ""

    model_input = lc.preprocess_for_emnist(img_array).reshape(1, 28, 28, 1)
    if TRANSPOSE_INPUT:
        model_input = model_input.transpose(0, 2, 1, 3)   # 가로/세로 축 교환
    prediction = model.predict(model_input, verbose=0)[0]

    # 숫자 클래스를 제외하고 알파벳 클래스 안에서만 가장 높은 확률을 선택
    letter_idx = [i for i, c in enumerate(lc.label_to_char) if c.isalpha()]
    letter_probs = prediction[letter_idx]
    letter_probs = letter_probs / letter_probs.sum()   # 알파벳끼리 합이 1이 되도록 다시 계산
    best = int(np.argmax(letter_probs))
    predicted_char = lc.label_to_char[letter_idx[best]].lower()
    confidence = float(letter_probs[best])

    # # [디버그] 모델이 본 28x28 입력, 알파벳 상위 3개, 숫자 포함 전체 1위 (확인 후 삭제 가능)
    # top3 = np.argsort(letter_probs)[::-1][:3]
    # overall = int(np.argmax(prediction))
    # st.session_state.debug = {
    #     "image": model_input.reshape(28, 28),
    #     "top3": [(lc.label_to_char[letter_idx[i]].lower(), round(float(letter_probs[i]), 2)) for i in top3],
    #     "overall": (lc.label_to_char[overall], round(float(prediction[overall]), 2)),
    # }

    # 확신도가 낮으면 인식하지 않음
    return predicted_char if confidence >= 0.4 else ""

def new_game():   
    st.session_state.problem = random.choice(word[st.session_state.game_level])
    st.session_state.guessed_letters = []
    st.session_state.wrong_count = 0
    st.session_state.game_over = False
    st.session_state.canvas_key += 1

def submit_letter(letter):
    letter = letter.lower()
    # 게임이 끝났거나 이미 제출한 글자는 처리하지 않음
    if st.session_state.game_over or letter in st.session_state.guessed_letters:
        return
    st.session_state.guessed_letters.append(letter)
    problem_word = st.session_state.problem["word"]
    if lc.check_letter(problem_word, letter):
        # 단어의 모든 글자를 맞히면 종료
        if all(c in st.session_state.guessed_letters for c in problem_word):
            st.session_state.game_over = True
    else:
        st.session_state.wrong_count += 1
        if st.session_state.wrong_count >= lc.MAX_WRONG_COUNT:
            st.session_state.game_over = True

# 전체 container
with st.container(key="game-shell", border=True):
    st.header("✨ AI 손글씨 행맨")
    
    left,right = st.columns([0.60,0.40], gap="medium", vertical_alignment="top")
    with left:
        st.markdown(
            f":red-badge[:material/star: 틀린 갯수] : {st.session_state.wrong_count} / {lc.MAX_WRONG_COUNT}"
        )
        st.markdown("✍️ ***알파벳***을 한 글자만 써주세요.")
        display_word = lc.display_word(st.session_state.problem["word"], st.session_state.guessed_letters)

        # 오른쪽 위쪽( canvas 영역 ), 아래쪽 ( 문제 제시 영역 )
        with st.container(key="canvas-panel"):
            canvas_result = st_canvas(
                fill_color="rgba(255, 255, 255, 0)",
                stroke_width=10,
                stroke_color="white",
                background_color="black",
                height= 210,
                width= 210,
                drawing_mode="freedraw",
                update_streamlit=True,

                return_image_data=True,                
                # false로 하면 python으로 새로운 데이터 update하지 않음
                # 이 경우 툴바의 제출버튼을 누르면 데이터가 넘어감
                key=f"hangman_canvas_{st.session_state.canvas_key}"
            )
            st.markdown(
                f"""
                <div style="
                    font-size:50px;
                    font-weight:bold;
                    letter-spacing:5px;
                    text-align:center;
                    padding:10px;
                ">
                {display_word}
                </div>
                """,
                unsafe_allow_html=True
            )
            
            print(canvas_result.image_data)
            st.info(f"""힌트 : {st.session_state.problem["hint"]}""")
            if st.button("제 출", disabled=st.session_state.game_over):
                if canvas_result.image_data is not None:
                    letter = predict_char(canvas_result)
                    print(f"letter:{letter}")
                    if letter.isalpha() and len(letter) == 1:
                        submit_letter(letter)
                        st.session_state.canvas_key += 1   # 다음 글자를 위해 캔버스 비우기
                        st.rerun()
                    else:
                        st.warning("알파벳을 다시 작성해 주세요.")
            
            if st.session_state.game_over:
                problem_word = st.session_state.problem["word"]
                if all(c in st.session_state.guessed_letters for c in problem_word):
                    st.success(f"🎉 정답입니다! {problem_word} ({st.session_state.problem['meaning']})")
                else:
                    st.error(f"😢 실패했습니다. 정답은 {problem_word} ({st.session_state.problem['meaning']}) 입니다.")
                if st.button("재시작"):
                    new_game()
                    st.rerun()
    with right:
        # 행맨 이미지
        st.image(str(lc.IMG_PATH / f"img_{st.session_state.game_level}{st.session_state.wrong_count}.png"), width="content")

# # [디버그] 마지막 인식 결과 확인용 (확인이 끝나면 이 블록을 삭제하세요)
# if "debug" in st.session_state:
#     with st.expander("🛠 인식 디버그 (마지막 제출)", expanded=True):
#         dbg = st.session_state.debug
#         c1, c2 = st.columns([1, 2])
#         with c1:
#             st.image(dbg["image"], width=140, clamp=True, caption="모델 입력 28x28 (전치 적용)" if TRANSPOSE_INPUT else "모델 입력 28x28")
#         with c2:
#             st.write("알파벳 상위 3개:", dbg["top3"])
#             st.write("숫자 포함 전체 1위:", dbg["overall"])
