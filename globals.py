import streamlit as st
from PIL import Image


def load_image(img, tgt_width=640):
    pil_in = Image.open(img)
    w, h = pil_in.size
    ratio = h / w
    height = int(tgt_width * ratio)
    pil_out = pil_in.resize((tgt_width, height))
    return pil_out


def init_globals():
    if "n_imgs" not in st.session_state:
        st.session_state.n_imgs = 0

    if "cur_i" not in st.session_state:
        st.session_state.cur_i = 0

    if "loaded" not in st.session_state:
        st.session_state.loaded = False

    if "json_data" not in st.session_state:
        st.session_state.json_data = []

    if "json_data_tmp" not in st.session_state:
        st.session_state.json_data_tmp = None

    if "json_out" not in st.session_state:
        st.session_state.json_out = []

    if "cropped_imgs" not in st.session_state:
        st.session_state.cropped_imgs = []

    if "pil_imgs" not in st.session_state:
        st.session_state.pil_imgs = []


def update_globals():
    n_imgs = st.session_state.n_imgs
    loaded = st.session_state.loaded
    if n_imgs > 0:
        if not loaded:
            st.session_state.loaded = True
            st.session_state.json_data = [None for _ in range(n_imgs)]
            st.session_state.json_out = [
                {
                    "filename": "unknown",
                    "objects": [],
                }
                for _ in range(n_imgs)
            ]
            st.session_state.pil_imgs = [None for _ in range(n_imgs)]
            st.session_state.cropped_imgs = [None for _ in range(n_imgs)]
        else:
            # if uploading more images later
            if len(st.session_state.json_data) < n_imgs:
                n_extra = n_imgs - len(st.session_state.json_data)
                st.session_state.json_data += [None for _ in range(n_extra)]
                st.session_state.json_out += [None for _ in range(n_extra)]
                st.session_state.pil_imgs += [None for _ in range(n_extra)]
                st.session_state.cropped_imgs += [None for _ in range(n_extra)]
        caching_images()


def caching_images():
    text_bar = "Caching images..."
    bar = st.progress(0, text=text_bar)
    n_imgs = st.session_state.n_imgs
    file_imgs = st.session_state.file_imgs
    pil_imgs = st.session_state.pil_imgs
    portion = int(100 / n_imgs)
    # showing progress bar of caching images
    for i in range(n_imgs):
        pil = pil_imgs[i]
        if pil is None:
            pil = load_image(file_imgs[i])
            st.session_state.pil_imgs[i] = pil
        bar.progress((i + 1) * portion, text=text_bar)
    bar.empty()
