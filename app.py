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

CYMBAL_STYLE = BUTTON_STYLE + "background: #d97706;"
DRUM_STYLE = BUTTON_STYLE + "background: #2563eb;"
BASS_STYLE = BUTTON_STYLE + "background: #059669;"

st.title("Band")
st.header("Click buttons and see the magic!")

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
