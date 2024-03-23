import streamlit as st
from streamlit_drawable_canvas import st_canvas
import pandas as pd

# local imports
from globals import init_globals, update_globals, canvas_to_states
from widgets import image_uploader, Timer
from outputs import make_dataframe
from callbacks import next_img, prev_img, slide_i, enable_hotkeys


st.set_page_config(
    page_title="PixelCraft",
    page_icon=None,
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
enable_hotkeys()

# components
st.title("PixelCraft")
## --- Image Uploader ---
st.session_state.loaded = False
st.session_state.file_imgs = image_uploader()
st.session_state.n_imgs = len(st.session_state.file_imgs)
loaded = st.session_state.n_imgs > 0
if not loaded:
    init_globals()
    st.success("Please upload images to get started")
else:
    update_globals()
    ## Image Viewer -------------------------------------------
    st.subheader("Image Viewer")
    ## Toggles ------------------------------------------------
    tg1, tg2 = st.columns(2)
    with tg1:
        tog_edit = st.toggle("Edit Bounding Boxes", False)
    with tg2:
        tog_auto = st.toggle("Refresh on-the-fly (Slower)", True, key="autorefresh")
    if not st.session_state.autorefresh:
        st.success("Right-click on the canvas to refresh the annotations")
    ## Get states ------------------------------------------------
    cur_i = st.session_state.cur_i
    print("current i   ", cur_i)
    n_imgs = st.session_state.n_imgs
    img_pil = st.session_state.pil_imgs[cur_i]
    state = st.session_state.json_data[cur_i]
    filename = st.session_state.file_imgs[cur_i].name
    ## drawable canvas ------------------------------------------------
    with Timer("Canvas"):
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
    canvas_to_states(cur_i, canvas, img_pil, filename)
    # Next/Prev Buttons -------------------------------------------
    col_b1, col_b2 = st.columns([5, 1])
    col_b1.button(
        "Previous Image",
        on_click=prev_img,
    )
    col_b2.button(
        "Next Image",
        on_click=next_img,
    )
    # Slider ------------------------------------------------
    if n_imgs == 1:
        st.empty()
    else:
        st.slider(
            "File Index",
            min_value=0,
            max_value=n_imgs - 1,
            value=cur_i,
            on_change=slide_i,
            key="slider_index",
            label_visibility="collapsed",
        )
    # Chart ------------------------------------------------
    json_out = st.session_state.json_out
    n_anns = [len(json["objects"]) for json in json_out]
    data = pd.DataFrame(
        {
            "n_bbox": [n_anns],
        }
    )
    st.dataframe(
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

    # Output Dataframe -------------------------------------------
    st.subheader("Output Dataframe")
    result = make_dataframe()
    st.dataframe(
        result,
        use_container_width=True,
    )

## Side bar -------------------------------------------
with st.sidebar:
    if loaded:
        ## Cropped Images -------------------------------------------
        st.header("Cropped Images")
        imgs = st.session_state.cropped_imgs[cur_i]
        if imgs:
            for img in imgs:
                st.image(img, use_column_width=True)
        ## Annotations -------------------------------------------
        st.header("Annotations")
        st.json(st.session_state.json_out)
    ## About -------------------------------------------
    st.divider()
    st.subheader("James Chen (<niche@vt.edu>)")
    st.write(
        """
            School of Animal Sciences, Virginia Tech

            Blacksburg, VA, USA
            """
    )
