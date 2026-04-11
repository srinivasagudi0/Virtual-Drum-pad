import time

import streamlit as st

from agent import (
    convert_to_emotion,
    get_music_for_mode,
    get_practice_tip,
    get_spotify_playlist,
    get_suggestion,
)
from support import display_pad


st.set_page_config(page_title="Virtual Drum Pad", page_icon="🥁", layout="wide")


PAD_LAYOUT = [
    [
        {"label": "Crash", "hint": "Accent", "tone": "cymbal", "file_path": "crash_symbal.m4a"},
        {"label": "Hi-Hat", "hint": "Time", "tone": "cymbal", "file_path": "hi_hat.m4a"},
        {"label": "Ride", "hint": "Lift", "tone": "cymbal", "file_path": "ride_cymbal.m4a"},
    ],
    [
        {"label": "Snare", "hint": "Backbeat", "tone": "drum", "file_path": "snare_drum.m4a"},
        {"label": "Rack Tom", "hint": "Fill", "tone": "drum", "file_path": "racktom.m4a"},
        {"label": "Floor Tom", "hint": "Low End", "tone": "drum", "file_path": "floor_tom.m4a"},
    ],
    [
        {"label": "Kick", "hint": "Pulse", "tone": "bass", "file_path": "bass_d.m4a"},
    ],
]


APP_STYLES = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Space+Grotesk:wght@400;500;700&display=swap');

.stApp {
    background:
        radial-gradient(circle at top left, rgba(243, 196, 91, 0.18), transparent 28%),
        radial-gradient(circle at top right, rgba(77, 124, 255, 0.16), transparent 24%),
        linear-gradient(180deg, #09111f 0%, #101b2d 48%, #0b1421 100%);
    color: #f6f7fb;
}

.main .block-container {
    max-width: 1180px;
    padding-top: 2.4rem;
    padding-bottom: 2rem;
}

h1, h2, h3, [data-testid="stMarkdownContainer"] h1, [data-testid="stMarkdownContainer"] h2 {
    font-family: "DM Serif Display", serif;
    color: #fff8eb;
}

p, label, [data-testid="stCaptionContainer"], [data-testid="stMarkdownContainer"] p {
    font-family: "Space Grotesk", sans-serif;
}

.hero {
    padding: 1.4rem 1.6rem;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 26px;
    background: linear-gradient(145deg, rgba(255, 255, 255, 0.08), rgba(255, 255, 255, 0.03));
    box-shadow: 0 24px 60px rgba(0, 0, 0, 0.22);
    margin-bottom: 1.25rem;
}

.eyebrow {
    margin: 0 0 0.4rem 0;
    font-size: 0.78rem;
    letter-spacing: 0.16rem;
    text-transform: uppercase;
    color: #f2c66d;
    font-family: "Space Grotesk", sans-serif;
}

.hero h1 {
    margin: 0;
    font-size: clamp(2.3rem, 4vw, 4rem);
    line-height: 0.95;
}

.hero p {
    margin: 0.8rem 0 0 0;
    max-width: 42rem;
    color: #d8e0f0;
    font-size: 1rem;
}

.section-title {
    margin: 0.1rem 0 0.8rem 0;
    font-size: 1.75rem;
}

.section-copy {
    margin: 0 0 1rem 0;
    color: #cfd7e6;
}

.session-card {
    padding: 1.1rem 1.15rem;
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(13, 25, 43, 0.88), rgba(24, 39, 63, 0.88));
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 18px 38px rgba(0, 0, 0, 0.22);
    margin-bottom: 1rem;
}

.session-card h3 {
    margin: 0 0 0.55rem 0;
    font-size: 1.6rem;
}

.session-card p {
    margin: 0.35rem 0;
    color: #d8e0f0;
}

.timer-box {
    margin-top: 0.75rem;
    padding: 0.95rem 1rem;
    border-radius: 18px;
    text-align: center;
    background: rgba(255, 255, 255, 0.06);
    border: 1px solid rgba(255, 255, 255, 0.08);
    font-family: "Space Grotesk", sans-serif;
}

.timer-label {
    display: block;
    text-transform: uppercase;
    letter-spacing: 0.12rem;
    font-size: 0.7rem;
    color: #f2c66d;
    margin-bottom: 0.35rem;
}

.timer-value {
    display: block;
    font-size: 2rem;
    font-weight: 700;
    color: #fff8eb;
}

.kit-note {
    margin-top: 0.9rem;
    color: #b8c3d7;
    font-size: 0.92rem;
}

div[data-baseweb="select"] > div,
div[data-testid="stSlider"] > div {
    background: rgba(255, 255, 255, 0.03);
}

button[kind="primary"],
button[kind="secondary"] {
    border-radius: 999px;
    font-family: "Space Grotesk", sans-serif;
}
</style>
"""


def render_timer(minutes, timer_box):
    total_seconds = minutes * 60
    progress_bar = st.progress(0, text="Practice timer ready")

    for remaining in range(total_seconds, -1, -1):
        elapsed = total_seconds - remaining
        progress = int((elapsed / total_seconds) * 100) if total_seconds else 100
        mins, secs = divmod(remaining, 60)
        timer_box.markdown(
            f"""
            <div class="timer-box">
                <span class="timer-label">Session Clock</span>
                <span class="timer-value">{mins:02d}:{secs:02d}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )
        progress_bar.progress(progress, text="Practice timer running")
        time.sleep(1)

    progress_bar.progress(100, text="Practice timer complete")
    st.success("Session complete. Reset your hands and run it back if you want another round.")


if "playlist" not in st.session_state:
    st.session_state.playlist = None
if "playlist_offset" not in st.session_state:
    st.session_state.playlist_offset = 0


st.markdown(APP_STYLES, unsafe_allow_html=True)

st.markdown(
    """
    <div class="hero">
        <p class="eyebrow">Merged Project</p>
        <h1>Virtual Drum Pad</h1>
        <p>
            A clean playable kit with a built-in practice lane. Tap the pads, pick a session mood,
            spin up a timer, and optionally pull a Spotify playlist when you want extra momentum.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


kit_col, session_col = st.columns([1.7, 1], gap="large")

with kit_col:
    st.markdown('<p class="eyebrow">Kit</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Simple layout, quick response</h2>', unsafe_allow_html=True)
    st.markdown(
        '<p class="section-copy">Cymbals up top, drums in the middle, kick at the bottom. It stays simple and feels familiar.</p>',
        unsafe_allow_html=True,
    )

    for row in PAD_LAYOUT:
        row_columns = st.columns(len(row), gap="small")
        for column, pad in zip(row_columns, row):
            with column:
                display_pad(
                    pad["label"],
                    file_path=pad["file_path"],
                    tone=pad["tone"],
                    hint=pad["hint"],
                    height=150,
                )

    st.markdown(
        '<p class="kit-note">Best used like a sketchpad: tap ideas fast, lock the groove, then move on.</p>',
        unsafe_allow_html=True,
    )

with session_col:
    st.markdown('<p class="eyebrow">Session</p>', unsafe_allow_html=True)
    st.markdown('<h2 class="section-title">Practice lane</h2>', unsafe_allow_html=True)

    mode = st.selectbox("Mode", ("Focus", "Chill", "Relax"))
    minutes = st.slider("Minutes", min_value=5, max_value=45, value=15, step=5)

    st.markdown(
        f"""
        <div class="session-card">
            <h3>{mode}</h3>
            <p>{convert_to_emotion(mode)}</p>
            <p><strong>Music fit:</strong> {get_music_for_mode(mode)}</p>
            <p><strong>Practice idea:</strong> {get_practice_tip(mode)}</p>
            <p><strong>Fallback:</strong> {get_suggestion(mode)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    timer_preview = st.empty()
    timer_preview.markdown(
        f"""
        <div class="timer-box">
            <span class="timer-label">Session Clock</span>
            <span class="timer-value">{minutes:02d}:00</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Start timer", use_container_width=True, type="primary"):
        render_timer(minutes, timer_preview)

    st.markdown('<div style="height: 0.6rem;"></div>', unsafe_allow_html=True)
    st.caption("Spotify is optional. Add credentials only if you want embedded playlists.")

    play_col, refresh_col = st.columns(2)
    if play_col.button("Load playlist", use_container_width=True):
        st.session_state.playlist_offset = 0
        st.session_state.playlist = get_spotify_playlist(mode, st.session_state.playlist_offset)

    if refresh_col.button("Next playlist", use_container_width=True):
        st.session_state.playlist_offset += 1
        st.session_state.playlist = get_spotify_playlist(mode, st.session_state.playlist_offset)

    playlist = st.session_state.playlist
    if playlist:
        if "error" in playlist:
            st.error(playlist["error"])
        else:
            st.success(f"Loaded: {playlist['name']}")
            st.components.v1.iframe(playlist["embed_url"], height=360)
            if playlist["url"]:
                st.link_button("Open in Spotify", playlist["url"], use_container_width=True)
