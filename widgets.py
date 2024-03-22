from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

# local imports
from callbacks import next_img, prev_img, slide_i


def image_uploader():
    return st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="image_uploader",
        label_visibility="collapsed",
    )


def drawable_image(
    idx,
    img,
    state,
    width=640,
    is_transform=False,
):
    img_pil = Image.open(img)
    w, h = img_pil.size
    ratio = h / w
    height = int(width * ratio)
    img_pil = img_pil.resize((width, height))
    # drawing state
    canvas = st_canvas(
        initial_drawing=state,
        fill_color="rgba(255, 90, 0, 0.3)",  # Fixed fill color with some opacity
        stroke_width=1,
        stroke_color="rgb(255, 0, 0, 1)",
        background_color="#fff",
        background_image=img_pil,
        update_streamlit=True,
        height=height,
        width=width,
        drawing_mode="transform" if is_transform else "rect",
        point_display_radius=0,
        key="canvas_%d" % idx,
    )
    time.sleep(0.5)
    return canvas, img_pil


def next_prev_buttons():
    col_b1, col_b2 = st.columns(2)
    col_b1.button(
        "Previous Image",
        on_click=prev_img,
    )
    col_b2.button(
        "Next Image",
        on_click=next_img,
    )


def slider_selector():
    cur_i = st.session_state.cur_i
    n_imgs = st.session_state.n_imgs
    if n_imgs == 1:
        return st.empty()
    else:
        return st.select_slider(
            "File Index",
            options=range(n_imgs),
            value=cur_i,
            on_change=slide_i,
            key="slider_index",
        )


def chart_anns():
    n_anns = [len(json["objects"]) for json in st.session_state.json_out]
    return st.area_chart(
        n_anns,
        color="rgba(255, 90, 0, 0.3)",
        height=100,
    )
