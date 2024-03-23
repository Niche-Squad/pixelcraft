import streamlit as st


def show_sidebar(loaded):
    with st.sidebar:
        if loaded:
            show_cropped_images()
            show_annotations()
        show_about()


def show_cropped_images():
    st.header("Cropped Images")
    cur_i = st.session_state.cur_i
    imgs = st.session_state.cropped_imgs[cur_i]
    if imgs:
        for img in imgs:
            st.image(img, use_column_width=True)


def show_annotations():
    st.header("Annotations")
    st.json(st.session_state.json_out)


def show_about():
    st.divider()
    st.subheader("James Chen (<niche@vt.edu>)")
    st.write(
        """
            School of Animal Sciences, Virginia Tech

            Blacksburg, VA, USA
            """
    )
