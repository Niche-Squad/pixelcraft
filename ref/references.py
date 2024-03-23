# https://github.com/adriangalilea/streamlit-shortcuts?tab=readme-ov-file

# Modifiers: 'Control', 'Shift', 'Alt'
# Common Keys: 'Enter', 'Escape', 'Space'
# Arrow Keys: 'ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown'
# Examples of Key Combinations:

# 'Control+Enter'
# 'Shift+ArrowUp'
# 'Alt+Space'


# def delete_callback():
#     st.write("DELETED!")


# st.button("delete", on_click=delete_callback)
# st.button("right", on_click=click_right)
# st.button("left", on_click=click_left)


# https://discuss.streamlit.io/t/display-images-one-by-one-with-a-next-button/21976/3
import streamlit as st
import os

col1, col2 = st.columns(2)

if "counter" not in st.session_state:
    st.session_state.counter = 0


def showPhoto(photo):
    col2.image(photo, caption=photo)
    col1.write(f"Index as a session_state attribute: {st.session_state.counter}")

    ## Increments the counter to get next photo
    st.session_state.counter += 1
    if st.session_state.counter >= len(pathsImages):
        st.session_state.counter = 0


# Get list of images in folder
folderWithImages = r"images"
pathsImages = [os.path.join(folderWithImages, f) for f in os.listdir(folderWithImages)]

col1.subheader("List of images in folder")
col1.write(pathsImages)

# Select photo a send it to button
photo = pathsImages[st.session_state.counter]
show_btn = col1.button("Show next pic ⏭️", on_click=showPhoto, args=([photo]))
