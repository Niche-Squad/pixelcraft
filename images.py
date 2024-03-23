import streamlit as st
from PIL import Image


def load_image(img, tgt_width=640):
    pil_in = Image.open(img)
    w, h = pil_in.size
    ratio = h / w
    height = int(tgt_width * ratio)
    pil_out = pil_in.resize((tgt_width, height))
    return pil_out


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
