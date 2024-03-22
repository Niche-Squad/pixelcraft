import streamlit as st
from streamlit_drawable_canvas import st_canvas


# local imports
from sidebar import deploy_sidebar
from globals import init_globals, update_globals
from widgets import (
    image_uploader,
    next_prev_buttons,
    slider_selector,
    chart_anns,
    toggle_canvas,
    Timer,
)
from outputs import make_dataframe, extract_canvas
from callbacks import enable_hotkeys


def main():
    st.set_page_config(
        page_title="PixelCraft",
        page_icon=None,
        layout="centered",
        initial_sidebar_state="auto",
        menu_items=None,
    )
    init_globals()
    enable_hotkeys()

    # components
    st.title("PixelCraft")
    ## --- Image Uploader ---
    st.session_state.file_imgs = image_uploader()
    st.session_state.n_imgs = len(st.session_state.file_imgs)
    update_globals()
    loaded = st.session_state.loaded
    if not loaded:
        st.success("Please upload images to get started")
    else:
        ## --- Image Viewer ---
        st.subheader("Image Viewer")
        tog_edit, tog_auto = toggle_canvas()
        cur_i = st.session_state.cur_i
        img_pil = st.session_state.pil_imgs[cur_i]
        state = st.session_state.json_data[cur_i]
        filename = st.session_state.file_imgs[cur_i].name
        # drawing state
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
            key="canvas_%d" % cur_i,
        )
        st.write(filename)
        # extract canvas
        while not canvas.json_data:
            pass

        # update session state
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

        ## --- Image Selector ---
        next_prev_buttons()
        slider_selector()
        chart_anns()

        ## --- Output Dataframe ---
        st.subheader("Output Dataframe")
        result = make_dataframe()
        st.dataframe(result)

    deploy_sidebar()


main()
