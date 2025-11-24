# BN Pulse Board — Streamlit Demo (Technology & Energy)

This Streamlit app is a synthetic demo of BN Analytics' "Pulse Board" showing trending KPIs for Technology and Energy sectors.
It is designed to be embedded inside the BN Analytics website via an iframe.

## Files
- `app.py` — Streamlit app
- `requirements.txt` — Python deps

## Run locally
1. Create and activate a virtualenv
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Deploy to Streamlit Cloud
1. Push this repo to GitHub (repo name `bn-pulse-board` recommended).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click "New app", select your repo, branch `main`, and main file `app.py`.
4. Deploy — Streamlit Cloud will give you a public URL like:
   `https://bn-pulse-board-YOURNAME.streamlit.app`

## Embedding
Use the `embed-snippet.html` from this package. It includes an auto-resize script so the iframe adapts to the Streamlit content.

## Note
This is **synthetic demo data** for layout and integration testing. Replace the generation logic with real API calls when ready.
