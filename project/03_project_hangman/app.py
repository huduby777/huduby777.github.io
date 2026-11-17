# streamlit 서버는 일반 웹 서버처럼 /img 폴더를 자동 공개하지 않아서 config.toml에
# app/static/img 폴더 경로로 옮겨서 작업해야 한다.
# 즉 streamlit에서는 공식적으로 정적 파일은 /static 폴더에 넣어서 제공해야 한다.
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import random
import lib.conf as lc

st.set_page_config(page_title="행맨", page_icon="⏳")

# 문제 가져오기
word = lc.load_word_data()

# 페이지 세션 가져오기
lc.make_session(word)

# emnist 모델 가져오기
model = lc.load_model()

def predict_char(canvas_result):
    guess = ""
    rgba = canvas_result.image_data.astype("uint8")
    rgb = rgba[..., :3].astype("float32")
    alpha = rgba[..., 3:4].astype("float32") / 255.0

    # 투명한 부분은 흰색(255)으로, 불투명한 부분(그린 획)은 원래 RGB(검정)로 합성
    composited = rgb * alpha + 255 * (1 - alpha)
    composited = composited.astype("uint8")

    img = Image.fromarray(composited).convert("L")
    img_array = np.array(img).astype("float32")
    # print(img_array.min(),img_array.max())  # 이제 0~255 범위로 제대로 나오는지 확인

    # 캔버스에 아무것도 안 그렸으면 예측하지 않음 
    if img_array.max() > 0:
        model_input = lc.preprocess_for_emnist(img_array, debug=False)
        model_input = model_input.reshape(1, 28, 28, 1)
        prediction = model.predict(model_input, verbose=0)[0]   

        predicted_char = lc.label_to_char[np.argmax(prediction)]
        confidence = float(np.max(prediction))
        
        # O와 S는 0 과 5로 인식하는 경우가 많음..
        if predicted_char == "0":
            predicted_char = "o"
        if predicted_char == "5":
            predicted_char = "s"
        
        print(predicted_char, confidence)
        
        if confidence >= 0.7:
            print("예측된 문자",  predicted_char.lower())
            print(f"확신도: {confidence * 100:.1f}%")
            guess = predicted_char
        else:
            print("=== 입력해 주세요.===")
    else:
        print("=== 문자를 입력해 주세요.===")
    return guess

def new_game():   
    st.session_state.problem = random.choice(word[st.session_state.game_level])
    st.session_state.guessed_letters = []
    st.session_state.wrong_count = 0
    st.session_state.game_over = False
    # st.session_state.letter_input = ""
    # st.session_state.letter_warning = False

def submit_letter(letter):
    letter = letter.lower()
    if lc.check_letter(st.session_state.problem["word"], letter):
        st.session_state.guessed_letters.append(letter)
        if "".join(st.session_state.guessed_letters) == st.session_state.problem["word"]:
            st.session_state.game_over = True
    else:
        st.session_state.wrong_count += 1   
        if st.session_state.wrong_count >= lc.MAX_WRONG_COUNT:
            st.session_state.game_over = True


print(st.session_state.problem["word"])
###########
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
                stroke_width=16,
                stroke_color="white",
                background_color="black",
                height= 210,
                width= 210,
                drawing_mode="freedraw",
                # display_toolbar=False,
                update_streamlit=True,

                return_image_data=True,                
                # false로 하면 python으로 새로운 데이터 update하지 않음
                # 이 경우 툴바의 제출버튼을 누르면 데이터가 넘어감
                key="hangman_canvas"
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
            
            st.info(f"""힌트 : {st.session_state.problem["hint"]}""")
            if st.button("제 출"):
                if canvas_result.image_data is not None:
                    letter = predict_char(canvas_result)
                    if letter.isalpha() and len(letter) == 1:
                        submit_letter(letter)
                        st.rerun()
                    else:
                        st.warning("알파벳을 다시 작성해 주세요.")
            
            if st.session_state.game_over:
                if st.button("재시작"):
                    new_game()
                    st.rerun()
    with right:
        # 행맨 이미지
        st.image(f"{lc.IMG_PATH}/img_{st.session_state.game_level}{st.session_state.wrong_count}.png", width="content")