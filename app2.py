import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from urllib.parse import quote_plus
import gspread
from google.oauth2.service_account import Credentials
# ---------------- CONFIG ----------------
st.set_page_config("Prasad Reality Vizag", "🏡", layout="wide")
ADMIN_PASSWORD = "prasad@admin"   # change later
PROPERTIES_SHEET = "properties_master"
LEADS_SHEET = "leads_bookings"
# ---------------- GOOGLE SHEETS ----------------
scope = [
   "https://spreadsheets.google.com/feeds",
   "https://www.googleapis.com/auth/drive"
]
creds = Credentials.from_service_account_info(
   st.secrets["gcp_service_account"],
   scopes=scope
)
client = gspread.authorize(creds)
sheet_props = client.open(PROPERTIES_SHEET).sheet1
sheet_leads = client.open(LEADS_SHEET).sheet1
def load_properties():
   data = sheet_props.get_all_records()
   return pd.DataFrame(data)
def save_lead(row):
   sheet_leads.append_row(row)
# ---------------- SESSION ----------------
if "admin" not in st.session_state:
   st.session_state.admin = False
if "revealed" not in st.session_state:
   st.session_state.revealed = {}
# ---------------- HEADER ----------------
st.title("🏡 Prasad Reality Vizag")
st.caption("Explore properties • Watch reels • Book visits")
# ---------------- ADMIN LOGIN ----------------
with st.sidebar:
   st.subheader("Admin Login")
   pwd = st.text_input("Password", type="password")
   if st.button("Login"):
       if pwd == ADMIN_PASSWORD:
           st.session_state.admin = True
           st.success("Admin access granted")
       else:
           st.error("Wrong password")
# ---------------- LOAD DATA ----------------
df = load_properties()
df = df[df["is_active"] == True]
# ---------------- FILTERS ----------------
st.sidebar.subheader("Filters")
locality = st.sidebar.multiselect(
   "Area",
   df["locality"].unique(),
   default=df["locality"].unique()
)
ptype = st.sidebar.multiselect(
   "Type",
   df["property_type"].unique(),
   default=df["property_type"].unique()
)
df = df[df["locality"].isin(locality)]
df = df[df["property_type"].isin(ptype)]
# ---------------- PROPERTY CARDS ----------------
cols = st.columns(3)
for i, row in df.iterrows():
   with cols[i % 3]:
       st.subheader(row["title"])
       st.caption(f"{row['locality']} • {row['property_type']}")
       st.write(f"📐 {row['size_sqft']} sqft")
       st.write(row["highlights"])
       # Reel
       st.components.v1.html(
           f"""
<blockquote class="instagram-media" data-instgrm-permalink="{row['reel_url']}" data-instgrm-version="14"></blockquote>
<script async src="https://www.instagram.com/embed.js"></script>
           """,
           height=450
       )
       pid = row["property_id"]
       # Price reveal
       if not st.session_state.revealed.get(pid):
           if st.button("🔒 Reveal Price", key=f"price_{pid}"):
               st.session_state.revealed[pid] = True
               save_lead([
                   datetime.now().strftime("%Y-%m-%d %H:%M"),
                   "", "",
                   "Price Reveal",
                   pid, "", "", "", "",
                   "Instagram",
                   row["reel_url"],
                   "New", ""
               ])
       else:
           st.success(f"₹ {row['price_lakhs']} Lakhs")
       # Booking
       with st.expander("📅 Book Visit / Video Call"):
           name = st.text_input("Name", key=f"name_{pid}")
           phone = st.text_input("Phone", key=f"phone_{pid}")
           btype = st.radio("Type", ["Video Call", "In-Person"], key=f"type_{pid}")
           date = st.date_input(
               "Date",
               min_value=datetime.today(),
               max_value=datetime.today() + timedelta(days=14),
               key=f"date_{pid}"
           )
           slot = st.selectbox("Slot", ["10–11", "11–12", "12–1", "3–4", "4–5"], key=f"slot_{pid}")
           if st.button("Confirm Booking", key=f"book_{pid}"):
               save_lead([
                   datetime.now().strftime("%Y-%m-%d %H:%M"),
                   name, phone,
                   "Booking",
                   pid, btype,
                   str(date), slot,
                   "7/14",
                   "Instagram",
                   row["reel_url"],
                   "Booked", ""
               ])
               st.success("Booking captured! We’ll contact you.")
# ---------------- ADMIN PANEL ----------------
if st.session_state.admin:
   st.divider()
   st.header("🛠 Admin Panel")
   st.dataframe(load_properties(), use_container_width=True)
   with st.form("add_property"):
       st.subheader("Add Property")
       new = [
           st.text_input("property_id"),
           st.text_input("title"),
           st.text_input("locality"),
           st.text_input("property_type"),
           st.text_input("condition"),
           st.number_input("bedrooms", 0),
           st.number_input("bathrooms", 0),
           st.number_input("size_sqft", 0),
           st.number_input("price_lakhs", 0),
           st.text_input("reel_url"),
           st.text_area("highlights"),
           st.selectbox("walkthrough_type", ["Video", "Visit", "Both"]),
           True,
           datetime.now().strftime("%Y-%m-%d")
       ]
       if st.form_submit_button("Add"):
           sheet_props.append_row(new)
           st.success("Property added")
