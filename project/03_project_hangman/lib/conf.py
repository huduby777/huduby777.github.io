import streamlit as st
import json
import tensorflow as tf

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageOps
import random

MAX_WRONG_COUNT = 5
# 문제 데이터 가져오기
@st.cache_data
def load_word_data():
    with open("./lib/hangman_words.json","r",encoding="utf-8") as f:
        dict_word_data = json.load(f)
    return dict_word_data

# 모델 가져오기
@st.cache_resource
def load_model():
    return tf.keras.models.load_model("./lib/emnist_balanced_cnn_0811.keras")

label_to_char = ["0","1","2","3","4","5","6","7","8","9",
    "A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S",
    "T","U","V","W","X","Y","Z","a","b","d","e","f","g","h","n","q","r","t"]

IMG_PATH = "/app/static/img/"

def make_session(word):
    if "game_level" not in st.session_state:
        st.session_state.game_level = "1"
    if "wrong_count" not in st.session_state:
        st.session_state.wrong_count = 0
    if "guessed_letters" not in st.session_state:
        st.session_state.guessed_letters = []
    if "problem" not in st.session_state:
        st.session_state.problem = random.choice(word[st.session_state.game_level])
    if "game_over" not in st.session_state:
        st.session_state.game_over = False
    if "letter_input" not in st.session_state:
        st.session_state.letter_input = ""    
    if "letter_warning" not in st.session_state:
        st.session_state.letter_warning = False
    if "corrent_count" not in st.session_state:
        st.session_state.correct_count = 0
        
# 단어 보여주기
def display_word(word, guessed_letters):
    display = []
    for letter in word:
        if letter in guessed_letters:
            display.append(letter)
        else:
            display.append(" _ ")
    return " ".join(display)

def check_letter(problem, letter):
    if letter in problem:
        return True
    else:
        return False
    

def predict_top_k(model, label_names, image_path_or_array, k=3, debug=False):
    """상위 k개 예측 결과를 (문자, 확률) 리스트로 반환. 헷갈리는 예측 디버깅용."""
    x = preprocess_for_emnist(image_path_or_array, debug=debug)
    x = np.expand_dims(x, axis=0)
 
    probs = model.predict(x, verbose=0)[0]
    top_idx = np.argsort(probs)[::-1][:k]
    return [(label_names[i], float(probs[i])) for i in top_idx]
 
def preprocess_for_emnist(image_path_or_array, debug=False):
    """
    실사용 이미지를 EMNIST 스타일(28x28, 흰 글씨/검은 배경, 중앙 정렬)로 변환.
 
    Parameters
    ----------
    image_path_or_array : str | np.ndarray | PIL.Image
        이미지 파일 경로, numpy 배열, 또는 PIL 이미지
    debug : bool
        True면 중간 단계 이미지를 보여줌 (matplotlib 필요)
 
    Returns
    -------
    np.ndarray, shape (28, 28, 1), float32, 0~1 범위
    """
   
    # 1. 이미지 로드 + 그레이스케일 변환
    if isinstance(image_path_or_array, str):
        img = Image.open(image_path_or_array).convert("L")
    elif isinstance(image_path_or_array, np.ndarray):
        img = Image.fromarray(image_path_or_array).convert("L")
    else:
        img = image_path_or_array.convert("L")
 
    arr = np.array(img)
    # print(arr)
 
    # 2. 색상 반전 체크: 배경이 밝으면(평균 밝기가 높으면) 반전
    #    EMNIST는 검은 배경 + 흰 글씨이므로, 배경이 흰색인 입력은 반전 필요
    if arr.mean() > 127:
        arr = 255 - arr
    
    # 3. 이진화(선택) - 노이즈 제거용 threshold. 필요 없으면 주석 처리 가능
    threshold = arr.mean() * 0.5
    binary = np.where(arr > threshold, arr, 0)
 
    # 4. 글씨 영역 bounding box 찾기
    rows = np.any(binary > 20, axis=1)
    cols = np.any(binary > 20, axis=0)
    if not rows.any() or not cols.any():
        raise ValueError("이미지에서 글씨를 찾을 수 없습니다. 입력을 확인하세요.")
 
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    cropped = binary[rmin:rmax + 1, cmin:cmax + 1]
 
    # 5. 정사각형으로 패딩 (여백 20% 정도 추가, EMNIST 특유의 여백 재현)
    h, w = cropped.shape
    size = max(h, w)
    pad = int(size * 0.2)
    size += pad * 2
 
    square = np.zeros((size, size), dtype=np.uint8)
    y_off = (size - h) // 2
    x_off = (size - w) // 2
    square[y_off:y_off + h, x_off:x_off + w] = cropped
 
    # 6. 28x28로 리사이즈
    resized = Image.fromarray(square).resize((28, 28), Image.LANCZOS)
    result = np.array(resized).astype(np.float32) / 255.0
    result = result.reshape(28, 28, 1)
 
    if debug:
        fig, axes = plt.subplots(1, 3, figsize=(9, 3))
        axes[0].imshow(arr, cmap="gray"); axes[0].set_title("반전/원본")
        axes[1].imshow(cropped, cmap="gray"); axes[1].set_title("crop")
        axes[2].imshow(result.squeeze(), cmap="gray"); axes[2].set_title("최종 28x28")
        plt.show()
 
    return result