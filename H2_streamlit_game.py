streamlit
streamlit-drawable-canvas

import streamlit as st
from streamlit_drawable_canvas import st_canvas
import math

st.set_page_config(page_title="H₂ Builder", layout="wide")

st.title("🧪 Build an H₂ Molecule")
st.write("Drag the two **H** atoms and the **–** bond to assemble **H–H**.")

# Canvas settings
canvas_width = 800
canvas_height = 400

# Initial positions for the pieces
if "pieces" not in st.session_state:
    st.session_state.pieces = {
        "H1": {"x": 100, "y": 150},
        "H2": {"x": 600, "y": 150},
        "bond": {"x": 350, "y": 150},
    }

# Draw the canvas
canvas_result = st_canvas(
    fill_color="rgba(0, 0, 0, 0)",
    stroke_width=2,
    stroke_color="#000000",
    background_color="#FFFFFF",
    height=canvas_height,
    width=canvas_width,
    drawing_mode="transform",  # enables dragging
    key="canvas",
    initial_drawing={
        "version": "4.4.0",
        "objects": [
            {
                "type": "text",
                "left": st.session_state.pieces["H1"]["x"],
                "top": st.session_state.pieces["H1"]["y"],
                "text": "H",
                "fontSize": 80,
            },
            {
                "type": "text",
                "left": st.session_state.pieces["H2"]["x"],
                "top": st.session_state.pieces["H2"]["y"],
                "text": "H",
                "fontSize": 80,
            },
            {
                "type": "text",
                "left": st.session_state.pieces["bond"]["x"],
                "top": st.session_state.pieces["bond"]["y"],
                "text": "-",
                "fontSize": 80,
            },
        ],
    },
)

# Update positions after dragging
if canvas_result.json_data is not None:
    objs = canvas_result.json_data["objects"]
    st.session_state.pieces["H1"]["x"] = objs[0]["left"]
    st.session_state.pieces["H1"]["y"] = objs[0]["top"]
    st.session_state.pieces["H2"]["x"] = objs[1]["left"]
    st.session_state.pieces["H2"]["y"] = objs[1]["top"]
    st.session_state.pieces["bond"]["x"] = objs[2]["left"]
    st.session_state.pieces["bond"]["y"] = objs[2]["top"]

# Check if the pieces form H–H
def is_aligned():
    H1 = st.session_state.pieces["H1"]
    H2 = st.session_state.pieces["H2"]
    bond = st.session_state.pieces["bond"]

    # Horizontal alignment tolerance
    y_tol = 40
    if abs(H1["y"] - bond["y"]) > y_tol:
        return False
    if abs(H2["y"] - bond["y"]) > y_tol:
        return False

    # Bond should be between H1 and H2
    return H1["x"] < bond["x"] < H2["x"] or H2["x"] < bond["x"] < H1["x"]

if is_aligned():
    st.success("🎉 You built an H₂ molecule!  **H–H**")

