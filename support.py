import streamlit.components.v1 as components
import base64

def diplay_button(name):
    with open("s.m4a", "rb") as audio_file:
        audio_bytes = audio_file.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()

    components.html(
        f"""
        <div>
            <button id="play-btn">{name}</button>
            <audio id="drum-audio">
                <source src="data:audio/mp4;base64,{audio_base64}" type="audio/mp4">
            </audio>
        </div>
        <script>
            const button = document.getElementById("play-btn");
            const audio = document.getElementById("drum-audio");
            button.addEventListener("click", () => {{
                audio.currentTime = 0;
                audio.play();
            }});
        </script>
        """,
        height=100,
    )
