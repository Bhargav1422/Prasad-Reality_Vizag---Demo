import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import requests
import base64
from io import StringIO
from urllib.parse import quote_plus

if "admin" not in st.session_state:
    st.session_state.admin = False

if "favorites" not in st.session_state:
    st.session_state.favorites = []

if "compare" not in st.session_state:
    st.session_state.compare = False



# ---------------- CONFIG ----------------
st.set_page_config("Prasad Realty Vizag", "🏡", layout="wide")

GITHUB_REPO = "Bhargav1422/Prasad-Reality_Vizag---Demo"
DATA_PATH = "data"
PROPERTIES_FILE = "properties.csv"
LEADS_FILE = "leads.csv"

GITHUB_TOKEN = st.secrets["github_token"]

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
# ---------------- BRANDING ----------------
st.markdown("""
<style>
/* App background */
.stApp {
    background-color: #F5F7FA;
}

/* Header container */
.header-container {
    display: flex;
    align-items: center;
    padding: 1rem 0;
}

/* Title text */
.brand-title {
    font-size: 2.2rem;
    font-weight: 700;
    color: #0E2A47;
    margin-left: 1rem;
}

/* Accent buttons */
.stButton>button {
    background-color: #0E2A47;
    color: white;
    border-radius: 8px;
    padding: 0.4rem 0.8rem;
    border: none;
}

.stButton>button:hover {
    background-color: #C9A227;
    color: black;
}

/* Card effect */
.block-container {
    padding-top: 1.5rem;
}

/* Admin divider */
hr {
    border-top: 2px solid #C9A227;
}
</style>
""", unsafe_allow_html=True)

# ---------------- GITHUB HELPERS ----------------
def github_url(file):
    return f"https://api.github.com/repos/{GITHUB_REPO}/contents/{DATA_PATH}/{file}"

def read_csv_from_github(file):
    r = requests.get(github_url(file), headers=HEADERS)
    content = base64.b64decode(r.json()["content"])
    return pd.read_csv(StringIO(content.decode()))

def write_csv_to_github(df, file, message):
    r = requests.get(github_url(file), headers=HEADERS)
    sha = r.json()["sha"]

    csv_data = df.to_csv(index=False)
    encoded = base64.b64encode(csv_data.encode()).decode()

    payload = {
        "message": message,
        "content": encoded,
        "sha": sha
    }
    requests.put(github_url(file), headers=HEADERS, json=payload)

# ---------------- DATA ----------------
props = read_csv_from_github(PROPERTIES_FILE)
props = props[props["is_active"] == True]

# ---------------- HEADER ----------------
col1, col2 = st.columns([1, 6])

with col1:
    st.image("assets/logo.png", width=110)

with col2:
    st.markdown("""
    <div class="header-container">
        <div class="brand-title">Prasad Realty Vizag</div>
    </div>
    <span style="color:#555;">
        Explore verified properties • Watch reels • Book visits
    </span>
    """, unsafe_allow_html=True)


# ---------------- FILTERS ----------------
with st.sidebar:
    st.subheader("Filters")
    area = st.multiselect("Area", props["locality"].unique(), default=props["locality"].unique())
    category = st.multiselect("Type", props["property_category"].unique(), default=props["property_category"].unique())

filtered = props[
    (props["locality"].isin(area)) &
    (props["property_category"].isin(category))
]
with st.sidebar:
    st.subheader("Admin Login")
    pwd = st.text_input("Password", type="password")
    if st.button("Login"):
        if pwd == "prasad@admin":  # change later
            st.session_state.admin = True
            st.success("Admin access enabled")
        else:
            st.error("Wrong password")

with st.sidebar:
    st.subheader("⭐ Favorites")
    if st.session_state.favorites:
        fav_props = props[props["property_id"].isin(st.session_state.favorites)]
        st.sidebar.write(f"Selected: {len(fav_props)}")
        if len(fav_props) > 3:
            st.sidebar.warning("Select up to 3 properties to compare")
        if st.sidebar.button("🔁 Compare"):
            st.session_state.compare = True
    else:
        st.sidebar.caption("No favorites selected yet")

if st.session_state.compare:
    st.subheader("🔁 Property Comparison")

    compare_df = props[
        props["property_id"].isin(st.session_state.favorites[:3])
    ][[
        "title",
        "locality",
        "property_category",
        "size_value",
        "size_unit",
        "price_value",
        "price_unit"
    ]]

    st.dataframe(compare_df.T, use_container_width=True)

    if st.button("❌ Close Comparison"):
        st.session_state.compare = False

    st.divider()

# ---------------- PROPERTY CARDS ----------------
cols = st.columns(3)

for i, row in filtered.iterrows():
    with cols[i % 3]:
        st.subheader(row["title"])
        st.caption(f"{row['locality']} • {row['property_category']}")
        st.write(f"📐 {row['size_value']} {row['size_unit']}")
        st.write(row["highlights"])

        st.components.v1.html(
            f"""
            <blockquote class="instagram-media" data-instgrm-permalink="{row['reel_url']}" data-instgrm-version="14"></blockquote>
            <script async src="https://www.instagram.com/embed.js"></script>
            """,
            height=420
        )

        if st.button("🔒 Reveal Price", key=f"price_{row['property_id']}"):
            leads = read_csv_from_github(LEADS_FILE)
            leads.loc[len(leads)] = [
                datetime.now(), "Price Reveal", row["property_id"],
                "", "", "", "", "", "",
                "Instagram", row["reel_url"], "New", ""
            ]
            write_csv_to_github(leads, LEADS_FILE, "Price reveal lead")
            st.success(
                f"💰 {row['price_value']} {row['price_unit']}"
                if pd.notna(row["price_value"])
                else "💰 Price on request"
            )
            pid = row["property_id"]
            if pid not in st.session_state.favorites:
                if st.button("⭐ Add to Favorites", key=f"fav_{pid}"):
                    st.session_state.favorites.append(pid)
                    st.success("Added to favorites")
            else:
                st.info("⭐ In your favorites")


        with st.expander("📅 Book Visit / Video Call"):
            name = st.text_input("Name", key=f"name_{i}")
            phone = st.text_input("Phone", key=f"phone_{i}")
            visit = st.radio("Type", ["Video Call", "In-Person"], key=f"visit_{i}")
            date = st.date_input("Date", datetime.today(), key=f"date_{i}")
            slot = st.selectbox(
                "Slot",
                ["10–11", "11–12", "12–1", "3–4", "4–5"],
                key=f"slot_{i}"
            )
        
            if st.button("Confirm Booking", key=f"book_{i}"):
        
                leads = read_csv_from_github(LEADS_FILE)
        
                leads.loc[len(leads)] = [
                    datetime.now(),
                    "Booking",
                    row["property_id"],
                    name,
                    phone,
                    "Visit",
                    visit,
                    str(date),
                    slot,
                    "Instagram",
                    row["reel_url"],
                    "Booked",
                    ""
                ]
        
                write_csv_to_github(leads, LEADS_FILE, "New booking")
        
                message = f"""
        Hello Prasad Realty,
        
        I’m interested in the following property:
        
        {row['title']}
        Property ID: {row['property_id']}
        
        Booking Type: {visit}
        Preferred Date: {date}
        Slot: {slot}
        
        Name: {name}
        Phone: {phone}
        
        Please confirm availability.
        """
        
                whatsapp_url = f"https://wa.me/916309729493?text={quote_plus(message)}"
                st.markdown("<hr>", unsafe_allow_html=True)
                st.success("Booking captured successfully.")
                st.markdown(
                    f"[📲 Open WhatsApp to Confirm]({whatsapp_url})",
                    unsafe_allow_html=True
                )

                
    # ------------------------------------------ Admin Panel ---------------------------------------------------------
if st.session_state.admin:
    st.divider()
    st.header("🛠 Admin Panel")

    editable = props.copy()

    edited = st.data_editor(
        editable[["property_id", "title", "is_active"]],
        use_container_width=True,
        num_rows="fixed",
        disabled=["property_id", "title"]
    )

    if st.button("Save Property Status"):
        full = read_csv_from_github(PROPERTIES_FILE)
        full.update(edited)
        write_csv_to_github(full, PROPERTIES_FILE, "Update property active status")
        st.success("Property status updated successfully")

