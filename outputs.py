import pandas as pd
import numpy as np
import streamlit as st


def show_ann_count():
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


def show_output_df():
    st.subheader("Output Dataframe")
    result = make_dataframe()
    st.dataframe(
        result,
        use_container_width=True,
    )


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
