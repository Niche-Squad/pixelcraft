import streamlit as st


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
    if n_imgs > 0 and not loaded:
        st.session_state.loaded = True
        st.session_state.json_data = [None for _ in range(n_imgs)]
        st.session_state.json_out = [
            {
                "filename": "unknown",
                "objects": [],
            }
            for _ in range(n_imgs)
        ]
        st.session_state.cropped_imgs = [None for _ in range(n_imgs)]
        st.session_state.pil_imgs = [None for _ in range(n_imgs)]

    # # if uploading more images later
    # if len(st.session_state.json_data) < n_imgs:
    #     n_extra = n_imgs - len(st.session_state.json_data)
    #     st.session_state.json_data += [None for _ in range(n_extra)]
    #     st.session_state.json_out += [None for _ in range(n_extra)]
    #     st.session_state.cropped_imgs += [None for _ in range(n_extra)]
