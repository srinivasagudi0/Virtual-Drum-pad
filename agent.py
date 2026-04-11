import base64
import os

import requests


DEFAULT_MODE = "Focus"
SPOTIFY_SEARCH_LIMIT = 10

MODE_TEXT = {
    "Focus": {
        "mood": "Good for work that needs a steady pace and tighter timing practice.",
        "music": "lo-fi, light electronic, or quiet instrumental tracks",
        "fallback": "Try something with no lyrics and a steady beat.",
        "tip": "Loop short grooves and keep the snare and kick landing in the same pocket every pass.",
        "search": "focus instrumental playlist",
    },
    "Chill": {
        "mood": "Good for a lighter mood when you still want some movement and relaxed groove work.",
        "music": "indie pop, mellow R&B, or easy weekend playlists",
        "fallback": "Try something warm and easy that does not ask too much from you.",
        "tip": "Use the hi-hat and ride to sketch looser patterns, then fill around them with tom accents.",
        "search": "chill mix playlist",
    },
    "Relax": {
        "mood": "Good for slowing down, resetting your hands, and clearing your head.",
        "music": "ambient, soft piano, or calm acoustic tracks",
        "fallback": "Try something slow, soft, and quiet.",
        "tip": "Play soft ghost notes, space things out, and focus on smooth touch instead of speed.",
        "search": "relax ambient playlist",
    },
}


def get_mode_details(mode):
    return MODE_TEXT.get(mode, MODE_TEXT[DEFAULT_MODE])


def get_music_for_mode(mode):
    return get_mode_details(mode)["music"]


def get_suggestion(mode):
    return get_mode_details(mode)["fallback"]


def get_practice_tip(mode):
    return get_mode_details(mode)["tip"]


def convert_to_emotion(user_input):
    return get_mode_details(user_input)["mood"]


def _read_secret(name):
    return os.getenv(name) or None


def _get_spotify_token():
    client_id = _read_secret("SPOTIFY_CLIENT_ID")
    client_secret = _read_secret("SPOTIFY_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None, "Missing SPOTIFY_CLIENT_ID or SPOTIFY_CLIENT_SECRET."

    raw = f"{client_id}:{client_secret}".encode("utf-8")
    basic_token = base64.b64encode(raw).decode("utf-8")

    try:
        response = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {basic_token}"},
            data={"grant_type": "client_credentials"},
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as error:
        return None, f"Spotify auth failed: {error}"

    access_token = payload.get("access_token")
    if not access_token:
        return None, "Spotify did not return an access token."

    return access_token, None


def get_spotify_playlist(mode, offset=0):
    details = get_mode_details(mode)
    token, error = _get_spotify_token()

    if error:
        return {"error": error}

    try:
        response = requests.get(
            "https://api.spotify.com/v1/search",
            headers={"Authorization": f"Bearer {token}"},
            params={
                "q": details["search"],
                "type": "playlist",
                "limit": SPOTIFY_SEARCH_LIMIT,
            },
            timeout=15,
        )
        response.raise_for_status()
        payload = response.json()
    except requests.RequestException as error:
        return {"error": f"Spotify search failed: {error}"}

    items = payload.get("playlists", {}).get("items", [])
    valid_items = [item for item in items if isinstance(item, dict) and item.get("id")]

    if not valid_items:
        return {"error": "No Spotify playlist found for this mode."}

    playlist = valid_items[offset % len(valid_items)]

    return {
        "name": playlist.get("name") or "Spotify playlist",
        "url": playlist.get("external_urls", {}).get("spotify", ""),
        "embed_url": f"https://open.spotify.com/embed/playlist/{playlist['id']}",
    }
