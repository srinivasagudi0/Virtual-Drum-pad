import streamlit as st
from support import diplay_button as display_button


BUTTON_STYLE = """
    width: 100%;
    height: 70px;
    border: none;
    border-radius: 16px;
    color: white;
    font-size: 20px;
    font-weight: bold;
    cursor: pointer;
"""

CYMBAL_STYLE = BUTTON_STYLE + """
    background: linear-gradient(135deg, #f59e0b, #d97706);
    box-shadow: 0 8px 20px rgba(217, 119, 6, 0.35);
"""

DRUM_STYLE = BUTTON_STYLE + """
    background: linear-gradient(135deg, #3b82f6, #1d4ed8);
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.35);
"""

BASS_STYLE = BUTTON_STYLE + """
    background: linear-gradient(135deg, #10b981, #047857);
    box-shadow: 0 8px 20px rgba(5, 150, 105, 0.35);
"""


st.title("Band")
st.header("Click buttons and see the magic!")
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at top, #1f2937, #0f172a 60%);
    }
    h1, h2, p {
        color: white !important;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


top_left, top_middle, top_right = st.columns(3)
mid_left, mid_middle_left, mid_middle_right, mid_right = st.columns(4)
bottom_left, bottom_middle, bottom_right = st.columns(3)

with top_left:
    display_button("Hi Hat!", style=CYMBAL_STYLE, file_path="crash_symbal.m4a")

with top_middle:
    display_button("Crash!", style=CYMBAL_STYLE, file_path="hi_hat.m4a")

with top_right:
    display_button("Ride Cymbal!", style=CYMBAL_STYLE, file_path="ride_cymbal.m4a")

with mid_left:
    display_button("Snare Drum!", style=DRUM_STYLE, file_path="snare_drum.m4a")

with mid_middle_left:
    display_button("Rack Tom 1!", style=DRUM_STYLE, file_path="racktom.m4a")

with mid_middle_right:
    display_button("Rack Tom 2!", style=DRUM_STYLE, file_path="racktom.m4a")

with mid_right:
    display_button("Floor Tom!", style=DRUM_STYLE, file_path="floor_tom.m4a")

with bottom_middle:
    display_button("Bass Drum!", style=BASS_STYLE, file_path="bass_d.m4a")
