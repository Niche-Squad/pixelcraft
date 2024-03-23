import streamlit as st

# local imports
from callbacks import enable_hotkeys
from canvas import show_canvas, canvas_to_states
from globals import init_globals, update_globals
from outputs import show_ann_count, show_output_df
from sidebar import show_sidebar
from widgets import (
    image_uploader,
    show_image_slider,
    show_next_prev_buttons,
    show_toggles,
)


st.set_page_config(
    page_title="PixelCraft",
    page_icon="🎨",
    layout="centered",
    initial_sidebar_state="auto",
    menu_items=None,
)
enable_hotkeys()

# components
st.title("PixelCraft 🎨")
st.session_state.file_imgs = image_uploader()
st.session_state.n_imgs = len(st.session_state.file_imgs)
loaded = st.session_state.n_imgs > 0
if not loaded:
    init_globals()
    st.success("Please upload images to get started")
else:
    update_globals()
    st.subheader("Image Viewer")

    tog_auto, tog_edit = show_toggles()
    canvas = show_canvas(tog_auto, tog_edit)
    canvas_to_states(canvas)

    show_next_prev_buttons()
    show_image_slider()
    show_ann_count()
    show_output_df()

show_sidebar(loaded)
