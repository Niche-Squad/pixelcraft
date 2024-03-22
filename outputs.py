import pandas as pd
import numpy as np
import streamlit as st


def extract_canvas(objects, img_pil):
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
        if cropped_image.mode != "RGB":
            cropped_image = cropped_image.convert("RGB")
        cropped_imgs[i] = cropped_image
        # calculate average channel values
        r, g, b = np.mean(cropped_image, axis=(0, 1), dtype=int)
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


def make_dataframe():
    result = pd.DataFrame(
        columns=["filename", "x", "y", "w", "h", "red", "green", "blue"]
    )
    for json_out in st.session_state.json_out:
        for obj in json_out["objects"]:
            data_tmp = pd.DataFrame(
                {
                    "filename": json_out["filename"],
                    "x": obj["left"],
                    "y": obj["top"],
                    "w": obj["width"],
                    "h": obj["height"],
                    "red": obj["red"],
                    "green": obj["green"],
                    "blue": obj["blue"],
                },
                index=[0],
            )
            result = pd.concat(
                [result, data_tmp],
                ignore_index=True,
            )
    return result
