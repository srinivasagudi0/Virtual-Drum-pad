import base64
import html
from pathlib import Path
import uuid

import streamlit as st


PAD_THEMES = {
    "cymbal": {
        "background": "linear-gradient(155deg, #f5d46b 0%, #d98522 100%)",
        "shadow": "rgba(217, 133, 34, 0.35)",
        "text": "#2c1705",
    },
    "drum": {
        "background": "linear-gradient(155deg, #5aa0ff 0%, #254bd6 100%)",
        "shadow": "rgba(37, 75, 214, 0.34)",
        "text": "#f7fbff",
    },
    "bass": {
        "background": "linear-gradient(155deg, #3dd2a2 0%, #0d7d67 100%)",
        "shadow": "rgba(13, 125, 103, 0.34)",
        "text": "#f5fffc",
    },
}


@st.cache_data(show_spinner=False)
def _load_audio_base64(file_path):
    audio_path = Path(file_path)
    if not audio_path.is_absolute():
        audio_path = Path(__file__).resolve().parent / audio_path
    return base64.b64encode(audio_path.read_bytes()).decode("utf-8")


def display_pad(name, file_path, tone="drum", hint="", height=150):
    palette = PAD_THEMES.get(tone, PAD_THEMES["drum"])
    if not file_path:
        st.error("Missing audio file path.")
        return

    try:
        audio_base64 = _load_audio_base64(file_path)
    except FileNotFoundError:
        st.error(f"Missing audio file: {file_path}")
        return

    safe_name = html.escape(name)
    safe_hint = html.escape(hint)
    component_height = max(height, 120)
    pad_id = f"pad-{uuid.uuid4().hex}"
    audio_id = f"audio-{uuid.uuid4().hex}"

    st.html(
        f"""
        <div class="pad-shell">
            <button class="pad" id="{pad_id}" type="button">
                <span class="pad-hint">{safe_hint}</span>
                <span class="pad-name">{safe_name}</span>
            </button>
            <audio id="{audio_id}" preload="auto">
                <source src="data:audio/mp4;base64,{audio_base64}" type="audio/mp4">
            </audio>
        </div>

        <style>
            :root {{
                color-scheme: dark;
            }}

            body {{
                margin: 0;
                background: transparent;
                font-family: "Space Grotesk", sans-serif;
            }}

            .pad-shell {{
                height: {component_height}px;
                display: flex;
                align-items: stretch;
            }}

            .pad {{
                width: 100%;
                height: 100%;
                border: 0;
                border-radius: 24px;
                padding: 1rem;
                display: flex;
                flex-direction: column;
                justify-content: space-between;
                text-align: left;
                cursor: pointer;
                color: {palette["text"]};
                background: {palette["background"]};
                box-shadow:
                    inset 0 1px 0 rgba(255, 255, 255, 0.2),
                    0 18px 32px {palette["shadow"]};
                transition: transform 120ms ease, box-shadow 120ms ease, filter 120ms ease;
            }}

            .pad:hover {{
                transform: translateY(-2px);
                filter: saturate(1.03);
            }}

            .pad:active {{
                transform: translateY(2px) scale(0.99);
                box-shadow:
                    inset 0 1px 0 rgba(255, 255, 255, 0.1),
                    0 10px 18px {palette["shadow"]};
            }}

            .pad-hint {{
                font-size: 0.72rem;
                font-weight: 700;
                letter-spacing: 0.12rem;
                text-transform: uppercase;
                opacity: 0.72;
            }}

            .pad-name {{
                font-size: 1.3rem;
                font-weight: 700;
                line-height: 1.05;
            }}
        </style>

        <script>
            const button = document.getElementById("{pad_id}");
            const audio = document.getElementById("{audio_id}");

            button.addEventListener("click", () => {{
                audio.pause();
                audio.currentTime = 0;
                audio.play();
            }});
        </script>
        """,
        unsafe_allow_javascript=True,
    )


def diplay_button(name, style="", height=100, file_path=None):
    tone = "drum"
    style_lower = style.lower()

    if "f59e0b" in style_lower or "d97706" in style_lower:
        tone = "cymbal"
    elif "10b981" in style_lower or "047857" in style_lower:
        tone = "bass"

    display_pad(name, file_path=file_path, tone=tone, height=height)
