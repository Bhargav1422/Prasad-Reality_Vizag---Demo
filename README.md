# Prasad Realty – Vizag (Instagram-native Streamlit Prototype)

A clean, modern, interactive prototype to showcase properties for Instagram audiences.

## Features
- Featured stories & card carousels
- Explore with filters (Neighborhood, Type, BHK, Budget, Status)
- Map view with pins (pydeck)
- Save favorites & Compare
- Enquiry hub with **Instagram DM** and **WhatsApp** deep links

## Quick Start (Local)
1. Ensure Python 3.9+
2. `pip install -r requirements.txt`
3. `streamlit run app.py`

## Deploy on Streamlit Cloud
1. Push this folder to a GitHub repo (e.g., `prasad-realty-vizag`).
2. Go to [Streamlit Cloud](https://share.streamlit.io) and deploy `app.py`.
3. Optional: set `st.secrets` for future integrations.

## Personalization
- Instagram handle is set to `prasad.reality_vizag` in `utils/config.py`.
- Update `WHATSAPP_NUMBER` in `utils/config.py` to your real number.
- Add real images to `assets/` and update `data/properties.csv`.

## Deep Link Examples
- `...?neighborhood=Rushikonda&type=Apartment&bhk=3` will pre-filter Explore.

## Data
Edit `data/properties.csv` to manage inventory. Images follow the convention `assets/<id>_1.jpg ...` with `image_count` set accordingly.
