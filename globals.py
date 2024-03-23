import streamlit as st
from PIL import Image

# local
from outputs import extract_canvas


def init_globals():
    # JSON data -----------------------------------------
    if "json_data" not in st.session_state:
        print("json_data not in session state")
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
        print("initializing cur_i")
        st.session_state.cur_i = 0
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "canvas" not in st.session_state:
        st.session_state.canvas = None


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


def canvas_to_states(cur_i, canvas, img_pil, filename):
    # update session state
    try:
        json_objs, cropped_img = extract_canvas(
            canvas.json_data["objects"],
            img_pil,
        )
        json_out = dict(
            {
                "filename": filename,
                "objects": json_objs,
            }
        )
        st.session_state.json_data_tmp = canvas.json_data
        st.session_state.json_out[cur_i] = json_out
        st.session_state.cropped_imgs[cur_i] = cropped_img
    except Exception as e:
        st.spinner("Buffering...")


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
