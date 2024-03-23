import streamlit as st

# local
from images import caching_images


def init_globals():
    # JSON data -----------------------------------------
    if "json_data" not in st.session_state:
        st.session_state.json_data = []
    if "json_data_tmp" not in st.session_state:
        st.session_state.json_data_tmp = None
    if "json_out" not in st.session_state:
        st.session_state.json_out = []

    # Images -----------------------------------------
    if "pil_imgs" not in st.session_state:
        st.session_state.pil_imgs = []
    if "cropped_imgs" not in st.session_state:
        st.session_state.cropped_imgs = []

    # VARIABLES -----------------------------------------
    if "cur_i" not in st.session_state:
        st.session_state.cur_i = 0


def update_globals():
    n_imgs = st.session_state.n_imgs

    if len(st.session_state.json_data) == 0:
        print("First time loading")
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
        caching_images()
    elif len(st.session_state.json_data) < n_imgs:
        print("More images uploaded")
        n_extra = n_imgs - len(st.session_state.json_data)
        st.session_state.json_data += [None for _ in range(n_extra)]
        st.session_state.json_out += [None for _ in range(n_extra)]
        st.session_state.pil_imgs += [None for _ in range(n_extra)]
        st.session_state.cropped_imgs += [None for _ in range(n_extra)]
        caching_images()
