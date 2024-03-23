from PIL import Image
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import time


# local imports
def image_uploader():
    uploader = st.file_uploader(
        "Upload Image",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True,
        key="image_uploader",
        label_visibility="collapsed",
    )
    return uploader


class Timer:
    def __init__(self, message="Page loaded"):
        self.message = message

    def __enter__(self):
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.time()
        st.info(f"{self.message} in {end - self.start:.2f} seconds")
