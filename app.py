import base64

import streamlit as st
import streamlit.components.v1 as components


BUTTON_STYLE = """
    width: 100%;
    height: 90px;
    border: none;
    border-radius: 18px;
    color: white;
    font-size: 22px;
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


def display_button(key_number, name, style="", height=120, file_path=None):
    if not file_path:
        return

    with open(file_path, "rb") as audio_file:
        audio_bytes = audio_file.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()
    element_id = f"drum-pad-{key_number}"
    label = f"{key_number}. {name}"

    components.html(
        f"""
        <div style="position: relative; height: {height}px;">
            <button id="{element_id}" style="{style}">{label}</button>
            <audio id="{element_id}-audio">
                <source src="data:audio/mp4;base64,{audio_base64}" type="audio/mp4">
            </audio>
        </div>
        <script>
            const button = document.getElementById("{element_id}");
            const audio = document.getElementById("{element_id}-audio");
            const keyNumber = "{key_number}";

            const playSound = () => {{
                audio.currentTime = 0;
                audio.play();
                button.style.transform = "scale(0.97)";
                setTimeout(() => {{
                    button.style.transform = "scale(1)";
                }}, 120);
            }};

            button.addEventListener("click", playSound);

            const parentWindow = window.parent;
            if (!parentWindow.virtualDrumPadKeys) {{
                parentWindow.virtualDrumPadKeys = {{}};
            }}

            parentWindow.virtualDrumPadKeys[keyNumber] = playSound;

            if (!parentWindow.virtualDrumPadKeyboardReady) {{
                parentWindow.addEventListener("keydown", (event) => {{
                    const handler = parentWindow.virtualDrumPadKeys?.[event.key];
                    if (handler) {{
                        handler();
                    }}
                }});
                parentWindow.virtualDrumPadKeyboardReady = true;
            }}
        </script>
        """,
        height=height,
    )


st.set_page_config(layout="wide")
st.title("Band")
st.header("Click a pad or press a number key")

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

st.write("Use keys 1 to 8 on your keyboard, or click the matching pad.")

top_left, top_middle, top_right = st.columns(3)
mid_left, mid_middle_left, mid_middle_right, mid_right = st.columns(4)
bottom_left, bottom_middle, bottom_right = st.columns(3)

with top_left:
    display_button(1, "Hi Hat", style=CYMBAL_STYLE, file_path="crash_symbal.m4a")

with top_middle:
    display_button(2, "Crash", style=CYMBAL_STYLE, file_path="hi_hat.m4a")

with top_right:
    display_button(3, "Ride Cymbal", style=CYMBAL_STYLE, file_path="ride_cymbal.m4a")

with mid_left:
    display_button(4, "Snare Drum", style=DRUM_STYLE, file_path="snare_drum.m4a")

with mid_middle_left:
    display_button(5, "Rack Tom 1", style=DRUM_STYLE, file_path="racktom.m4a")

with mid_middle_right:
    display_button(6, "Rack Tom 2", style=DRUM_STYLE, file_path="racktom.m4a")

with mid_right:
    display_button(7, "Floor Tom", style=DRUM_STYLE, file_path="floor_tom.m4a")

with bottom_middle:
    display_button(8, "Bass Drum", style=BASS_STYLE, file_path="bass_d.m4a")
