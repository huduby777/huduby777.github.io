import streamlit as st
import json
import tensorflow as tf

import numpy as np
from PIL import Image
import random
from pathlib import Path


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

BASE_DIR = Path(".")
IMG_PATH = BASE_DIR / "static" / "img"

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
    return letter in problem

def preprocess_for_emnist(img_array):
    """
    캔버스 이미지를 EMNIST 스타일(28x28, 흰 글씨/검은 배경, 중앙 정렬)로 변환.

    Parameters
    ----------
    img_array : np.ndarray
        그레이스케일 이미지 배열 (0~255)

    Returns
    -------
    np.ndarray, shape (28, 28, 1), float32, 0~1 범위
    """
    arr = np.array(Image.fromarray(img_array).convert("L"))

    # 1. 색상 반전 체크: EMNIST는 검은 배경 + 흰 글씨이므로, 배경이 밝으면 반전
    if arr.mean() > 127:
        arr = 255 - arr

    # 2. 이진화: 노이즈 제거용 threshold
    threshold = arr.mean() * 0.5
    binary = np.where(arr > threshold, arr, 0)

    # 3. 글씨 영역 bounding box 찾기
    rows = np.any(binary > 20, axis=1)
    cols = np.any(binary > 20, axis=0)
    if not rows.any() or not cols.any():
        raise ValueError("이미지에서 글씨를 찾을 수 없습니다. 입력을 확인하세요.")

    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    cropped = binary[rmin:rmax + 1, cmin:cmax + 1]

    # 4. 정사각형으로 패딩 (여백 20% 정도 추가, EMNIST 특유의 여백 재현)
    h, w = cropped.shape
    size = max(h, w)
    pad = int(size * 0.2)
    size += pad * 2

    square = np.zeros((size, size), dtype=np.uint8)
    y_off = (size - h) // 2
    x_off = (size - w) // 2
    square[y_off:y_off + h, x_off:x_off + w] = cropped

    # 5. 28x28로 리사이즈
    resized = Image.fromarray(square).resize((28, 28), Image.LANCZOS)
    result = np.array(resized).astype(np.float32) / 255.0
    return result.reshape(28, 28, 1)
