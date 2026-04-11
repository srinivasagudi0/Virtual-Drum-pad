# Virtual Drum Pad

Virtual Drum Pad is a small Streamlit app that merges the original drum pad with the `TBD` focus-session idea into one place.

You get:

- a clean drum pad layout with local audio samples
- a simple practice panel with `Focus`, `Chill`, and `Relax` modes
- a built-in countdown timer
- optional Spotify playlist loading when credentials are available

## Run it

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Optional Spotify setup

Set these environment variables only if you want the embedded playlist feature:

```bash
export SPOTIFY_CLIENT_ID="your-client-id"
export SPOTIFY_CLIENT_SECRET="your-client-secret"
```

Without them, the drum pad and timer still work normally.
