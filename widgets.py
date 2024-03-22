from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time

# local imports
from callbacks import next_img, prev_img, slide_i


def image_uploader():
    uploader = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="image_uploader",
        label_visibility="collapsed",
    )
    return uploader


def next_prev_buttons():
    col_b1, col_b2 = st.columns([5, 1])
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
        slider = st.empty()
    else:
        slider = st.select_slider(
            "File Index",
            options=range(n_imgs),
            value=cur_i,
            on_change=slide_i,
            key="slider_index",
            label_visibility="collapsed",
        )
    return slider


def toggle_canvas():
    tg1, tg2 = st.columns(2)
    with tg1:
        edit = st.toggle("Edit Bounding Boxes", False)
    with tg2:
        autorefresh = st.toggle("Refresh on-the-fly (Slower)", False, key="autorefresh")
    if not st.session_state.autorefresh:
        st.success("Right-click on the canvas to refresh the annotations")
    return edit, autorefresh


def chart_anns():
    start = time.time()
    json_out = st.session_state.json_out
    print("get json_out", int(time.time() - start))
    n_anns = [len(json["objects"]) for json in json_out]
    print("get n_anns", int(time.time() - start))
    data = pd.DataFrame(
        {
            "n_bbox": [n_anns],
        }
    )
    # chart = st.area_chart(
    #     n_anns,
    #     color="rgba(255, 90, 0, 0.3)",
    #     height=100,
    # )
    chart = st.dataframe(
        data,
        column_config={
            "n_bbox": st.column_config.LineChartColumn(
                "Number of Bounding Boxes",
                y_min=0,
                y_max=10,
            )
        },
        hide_index=True,
        use_container_width=True,
    )
    print("chart", int(time.time() - start))
    return chart


class Timer:
    def __init__(self, message="Page loaded"):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        st.info(f"{self.message} in {end - self.start:.2f} seconds")
