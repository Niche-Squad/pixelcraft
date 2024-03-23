import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# local
from widgets import Timer
from images import segmentaion, avg_rgb


def show_canvas(tog_auto, tog_edit):
    cur_i = st.session_state.cur_i
    img_pil = st.session_state.pil_imgs[cur_i]
    state = st.session_state.json_data[cur_i]
    filename = st.session_state.file_imgs[cur_i].name

    # with Timer("Rendering Time"):
    canvas = st_canvas(
        initial_drawing=state,
        fill_color="rgba(255, 90, 0, 0.3)",
        stroke_width=1,
        stroke_color="rgb(255, 0, 0, 1)",
        background_color="#fff",
        background_image=img_pil,
        update_streamlit=tog_auto,
        height=img_pil.height,
        width=img_pil.width,
        drawing_mode="transform" if tog_edit else "rect",
        # point_display_radius=0, # not available in 0.8.0
        key="canvas%d" % cur_i,
    )
    st.write(filename)
    return canvas


def canvas_to_states(canvas):
    cur_i = st.session_state.cur_i
    img_pil = st.session_state.pil_imgs[cur_i]
    filename = st.session_state.file_imgs[cur_i].name
    strength = st.session_state.seg_strength
    try:
        json_objs, cropped_img = extract_canvas(
            canvas.json_data["objects"],
            img_pil,
            strength,
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


def extract_canvas(objects, img_pil, seg_strength=0):
    """
    objects: list
        canvas.json_data["objects"]
    """
    n_objs = len(objects)
    cropped_imgs = [None] * n_objs
    json_objs = [None] * n_objs
    # iterate through each object
    for i, obj in enumerate(objects):
        l, t, w, h = (
            obj["left"],
            obj["top"],
            obj["width"] * obj["scaleX"],
            obj["height"] * obj["scaleY"],
        )
        # cropped image
        cropped_image = img_pil.crop((l, t, l + w, t + h))
        segged_image = segmentaion(cropped_image, seg_strength)
        cropped_imgs[i] = segged_image
        # calculate average channel values
        r, g, b = avg_rgb(segged_image)
        # json
        json_objs[i] = {
            "left": l,
            "top": t,
            "width": w,
            "height": h,
            "red": r,
            "green": g,
            "blue": b,
        }

    # return
    return json_objs, cropped_imgs
