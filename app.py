import streamlit as st
from utils.config import BRAND_NAME, IG_HANDLE

st.set_page_config(
    page_title=f"{BRAND_NAME}",
    page_icon="🏖️",
    layout="wide"
)

st.markdown("""
<style>
:root { --accent: #1A73E8; --ink: #222; }
header {visibility: hidden;}
.block-container {padding-top: 0.75rem;}
.stButton>button, .stSelectbox div[data-baseweb="select"], .stTextInput>div>div>input {border-radius: 12px;}
a.sidebar-link {text-decoration: none;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title(BRAND_NAME)
st.sidebar.caption("Instagram-native property explorer")
st.sidebar.page_link("pages/1_🏠_Home.py", label="Home")
st.sidebar.page_link("pages/2_🔎_Explore.py", label="Explore")
st.sidebar.page_link("pages/3_📊_Compare.py", label="Compare")
st.sidebar.page_link("pages/4_💬_Enquire.py", label="Enquire")
st.sidebar.page_link("pages/5_❤️_Saved.py", label="Saved")

st.sidebar.markdown(f"**Instagram:** [@{IG_HANDLE}](https://instagram.com/{IG_HANDLE})")

st.title("Welcome ✨")
st.write("Use the left navigation to explore the prototype. For a quick visual overview, open **Home**.")
