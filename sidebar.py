import streamlit as st


def deploy_sidebar():
    with st.sidebar:
        if st.session_state.loaded:
            show_cropped_images()
            show_annotations()
        show_author()


def show_cropped_images():
    st.header("Cropped Images")
    if st.session_state.loaded:
        cur_i = st.session_state.cur_i
        imgs = st.session_state.cropped_imgs[cur_i]
        if imgs:
            for img in imgs:
                st.image(img, use_column_width=True)


def show_annotations():
    st.header("Annotations")
    st.json(st.session_state.json_out)


def show_author():
    st.divider()
    st.subheader("James Chen (<niche@vt.edu>)")
    st.write(
        """
            School of Animal Sciences, Virginia Tech

            Blacksburg, VA, USA
            """
    )
