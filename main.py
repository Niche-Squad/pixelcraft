import streamlit as st

# local imports
from sidebar import deploy_sidebar
from globals import init_globals, update_globals
from widgets import (
    drawable_image,
    image_uploader,
    next_prev_buttons,
    slider_selector,
    chart_anns,
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
    file_imgs = image_uploader()
    st.session_state.n_imgs = len(file_imgs)
    update_globals()
    loaded = st.session_state.loaded
    if not loaded:
        st.success("Please upload images to get started")
    else:
        ## --- Image Viewer ---
        st.subheader("Image Viewer")
        edit = st.toggle("Edit Bounding Boxes", False)

        cur_i = st.session_state.cur_i
        canvas, img_pil = drawable_image(
            idx=st.session_state.cur_i,
            img=file_imgs[cur_i],
            state=st.session_state.json_data[cur_i],
            is_transform=edit,
        )
        st.write(file_imgs[cur_i].name)
        # extract canvas
        while not canvas.json_data:
            pass
        json_objs, cropped_img = extract_canvas(
            canvas.json_data["objects"],
            img_pil,
        )
        json_out = dict(
            {
                "filename": file_imgs[cur_i].name,
                "objects": json_objs,
            }
        )
        # update session state
        st.session_state.json_data_tmp = canvas.json_data
        st.session_state.json_out[cur_i] = json_out
        st.session_state.cropped_imgs[cur_i] = cropped_img
        st.session_state.pil_imgs[cur_i] = img_pil

        ## --- Image Selector ---
        st.subheader("Image Selector")
        next_prev_buttons()
        slider_selector()
        chart_anns()

        ## --- Output Dataframe ---
        st.subheader("Output Dataframe")
        result = make_dataframe()
        st.dataframe(result)

    deploy_sidebar()


main()
