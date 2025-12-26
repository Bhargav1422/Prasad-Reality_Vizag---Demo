# app.py — Prasad Reality Vizag
# Streamlit-native, Instagram-first real estate catalogue
import os
from datetime import datetime
from urllib.parse import quote_plus
import pandas as pd
import streamlit as st
from streamlit.components.v1 import html as st_html
# -------------------------------------------------
# App config
# -------------------------------------------------
st.set_page_config(
   page_title="Prasad Reality Vizag",
   page_icon="🏡",
   layout="centered"  # mobile-first
)
# -------------------------------------------------
# Constants
# -------------------------------------------------
IG_HANDLE = "prasad.reality_vizag"
WA_INDIA_NUM = "916309729493"
DATA_DIR = "."
LEADS_FILE = os.path.join(DATA_DIR, "leads.csv")
# -------------------------------------------------
# Mock property data (replace later with Sheets/DB)
# -------------------------------------------------
PROPERTIES = [
   {
       "id": "VRV-101",
       "title": "3BHK Premium Apartment",
       "locality": "Seethammadhara",
       "property_type": "Apartment",
       "condition": "New",
       "price_lakhs": 205,
       "size_sqft": 2050,
       "bed": 3,
       "bath": 3,
       "img": "https://images.unsplash.com/photo-1582582429416-d1e9b7a8479f?w=1200",
       "desc": "One flat per floor, Vastu compliant, power backup, premium interiors.",
       "reel_url": "https://www.instagram.com/reel/C_demo_1/"
   },
   {
       "id": "VRV-102",
       "title": "Commercial Space",
       "locality": "Maddilapalem",
       "property_type": "Commercial",
       "condition": "New",
       "price_lakhs": 0,
       "size_sqft": 10800,
       "bed": 0,
       "bath": 0,
       "img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200",
       "desc": "High visibility commercial property suitable for offices and showrooms.",
       "reel_url": "https://www.instagram.com/reel/C_demo_2/"
   },
   {
       "id": "VRV-103",
       "title": "2BHK Group House",
       "locality": "Chinnamushidiwada",
       "property_type": "Apartment",
       "condition": "New",
       "price_lakhs": 0,
       "size_sqft": 850,
       "bed": 2,
       "bath": 2,
       "img": "https://images.unsplash.com/photo-1507089943778-0d63b1f95b42?w=1200",
       "desc": "Family-friendly group house near schools and main road.",
       "reel_url": "https://www.instagram.com/reel/C_demo_3/"
   },
]
# -------------------------------------------------
# Session state
# -------------------------------------------------
if "favourites" not in st.session_state:
   st.session_state.favourites = []
if "compare" not in st.session_state:
   st.session_state.compare = []
# -------------------------------------------------
# Helpers
# -------------------------------------------------
def format_price(price):
   return "Price on request" if not price else f"₹{price:.1f} Lakhs"
def whatsapp_link(text):
   return f"https://wa.me/{WA_INDIA_NUM}?text={quote_plus(text)}"
def ensure_leads_csv():
   if not os.path.exists(LEADS_FILE):
       pd.DataFrame(columns=["timestamp", "name", "phone", "property_id"]).to_csv(
           LEADS_FILE, index=False
       )
# -------------------------------------------------
# Header
# -------------------------------------------------
st.title("🏡 Prasad Reality Vizag")
st.caption("Discover verified Vizag properties • Watch reels • Save & compare • Contact instantly")
cta_cols = st.columns(2)
with cta_cols[0]:
   st.link_button(
       "📲 WhatsApp Now",
       whatsapp_link("Hi, I’m browsing properties on your app."),
       type="primary",
   )
with cta_cols[1]:
   st.link_button(
       "📸 Instagram",
       f"https://www.instagram.com/{IG_HANDLE}/"
   )
st.divider()
# -------------------------------------------------
# Filters
# -------------------------------------------------
df = pd.DataFrame(PROPERTIES)
areas = sorted(df["locality"].unique())
types = sorted(df["property_type"].unique())
area_sel = st.multiselect("📍 Area", areas, default=areas)
type_sel = st.multiselect("🏢 Property Type", types, default=types)
cond_sel = st.selectbox("🏗️ Condition", ["All", "New", "Old"], index=0)
filtered = df[
   df["locality"].isin(area_sel)
& df["property_type"].isin(type_sel)
]
if cond_sel != "All":
   filtered = filtered[filtered["condition"] == cond_sel]
st.caption(f"🔎 Showing {len(filtered)} properties")
st.divider()
# -------------------------------------------------
# Property Cards
# -------------------------------------------------
for _, p in filtered.iterrows():
   with st.container():
       st.image(p["img"], use_column_width=True)
       st.subheader(p["title"])
       st.caption(f"{p['locality']} • {p['property_type']} • {p['condition']}")
       st.write(f"**Price:** {format_price(p['price_lakhs'])}")
       st.write(f"**Size:** {p['size_sqft']} sqft")
       # Primary CTA
       st.link_button(
           "📲 Enquire on WhatsApp",
           whatsapp_link(
               f"Hello, I’m interested in {p['title']} ({p['id']}) in {p['locality']}."
           ),
           type="primary",
       )
       # Actions row
       act1, act2 = st.columns(2)
       with act1:
           fav = p["id"] in st.session_state.favourites
           if st.button("❤️ Saved" if fav else "🤍 Save", key=f"fav_{p['id']}"):
               if fav:
                   st.session_state.favourites.remove(p["id"])
               else:
                   st.session_state.favourites.append(p["id"])
       with act2:
           cmp = p["id"] in st.session_state.compare
           if st.button("⚖️ Compare" if not cmp else "✅ Added", key=f"cmp_{p['id']}"):
               if not cmp and len(st.session_state.compare) < 3:
                   st.session_state.compare.append(p["id"])
       # Details
       with st.expander("📄 View details"):
           st.write(p["desc"])
           if p["reel_url"]:
               st.markdown("**🎬 Instagram Reel**")
               st_html(
                   f"""
<blockquote class="instagram-media"
                       data-instgrm-permalink="{p['reel_url']}"
                       data-instgrm-version="14"
                       style="background:#FFF; border:0; margin:1px; max-width:540px;">
</blockquote>
<script async src="//www.instagram.com/embed.js"></script>
                   """,
                   height=620,
               )
   st.divider()
# -------------------------------------------------
# ❤️ Favourites
# -------------------------------------------------
if st.session_state.favourites:
   st.subheader("❤️ Your Favourites")
   fav_df = df[df["id"].isin(st.session_state.favourites)]
   for _, f in fav_df.iterrows():
       st.write(f"• **{f['title']}** — {format_price(f['price_lakhs'])}")
   msg = "My favourite properties:\n" + "\n".join(
       f"{f['title']} ({f['locality']})"
       for _, f in fav_df.iterrows()
   )
   st.link_button("📲 Share favourites", whatsapp_link(msg), type="primary")
   st.divider()
# -------------------------------------------------
# ⚖️ Comparison
# -------------------------------------------------
if len(st.session_state.compare) >= 2:
   st.subheader("⚖️ Compare Properties")
   cmp_df = df[df["id"].isin(st.session_state.compare)][
       ["title", "locality", "property_type", "condition", "size_sqft", "price_lakhs"]
   ]
   st.dataframe(cmp_df, use_container_width=True)
   if st.button("❌ Clear comparison"):
       st.session_state.compare.clear()
   st.divider()
# -------------------------------------------------
# Lead capture
# -------------------------------------------------
st.subheader("📞 Request a Call Back")
with st.form("lead_form"):
   name = st.text_input("Name")
   phone = st.text_input("Phone (WhatsApp)")
   pid = st.selectbox(
       "Property of interest",
       ["General enquiry"] + df["id"].tolist(),
   )
   submitted = st.form_submit_button("Submit")
   if submitted and name and phone:
       ensure_leads_csv()
       row = {
           "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
           "name": name,
           "phone": phone,
           "property_id": pid,
       }
       pd.read_csv(LEADS_FILE).append(row, ignore_index=True).to_csv(
           LEADS_FILE, index=False
       )
       st.success("✅ Thanks! We’ll contact you shortly.")
# -------------------------------------------------
# Footer
# -------------------------------------------------
st.caption("© Prasad Reality Vizag • Instagram-first property discovery")
