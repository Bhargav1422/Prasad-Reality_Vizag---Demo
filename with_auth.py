
# streamlit_app.py — Public showcase, premium UI, no login, all HTML entity fixes applied
import os
import base64
from datetime import datetime
from urllib.parse import quote_plus
import pandas as pd
import streamlit as st
import pydeck as pdk

# -----------------------------
# Feature toggles
# -----------------------------
ENABLE_HEATMAP   = True
ENABLE_LEADS     = False          # off by default
ENABLE_INSTAGRAM = False          # off by default
ENABLE_PER_CARD_DOWNLOAD = False  # off by default

# -----------------------------
# App setup
# -----------------------------
st.set_page_config(page_title="Prasad Reality Vizag — Property Showcase", page_icon="🏡", layout="wide")

# -----------------------------
# Brand & contact constants
# -----------------------------
BRAND_PRIMARY = "#0E57D3"
BRAND_ACCENT  = "#FF5A3D"
BRAND_DARK    = "#0A2B6D"
BG_DARK       = "#0F172A"     # backdrop
TEXT_LIGHT    = "#F8FAFC"
TEXT_MUTED    = "#94A3B8"

WA_INDIA_NUM = "916309729493"
WA_US_NUM    = "17864209015"
IG_PROFILE   = "prasad.reality_vizag"

# -----------------------------
# Logo auto-load (from repo)
# -----------------------------
def load_logo_src():
    for name in ('prasad_logo.png', 'prasad_logo.jpg', 'prasad_logo.jpeg'):
        if os.path.exists(name):
            with open(name, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
            ext = name.split('.')[-1]
            return f'data:image/{ext};base64,{b64}'
    return None

logo_src = load_logo_src()

# -----------------------------
# CSS (premium UI) — raw HTML with f-string and escaped braces
# -----------------------------
st.markdown(
    f"""
    <style>
      :root {{
        --brand-primary: {BRAND_PRIMARY};
        --brand-accent:  {BRAND_ACCENT};
        --brand-dark:    {BRAND_DARK};
        --bg-dark:       {BG_DARK};
        --text-light:    {TEXT_LIGHT};
        --text-muted:    {TEXT_MUTED};
      }}

      body {{ background-color: var(--bg-dark); }}
      .main .block-container {{ padding-top: 0.6rem; max-width: 1200px; }}

      /* Header */
      .brand-header {{
        background: linear-gradient(98deg, var(--brand-primary) 0%, var(--brand-dark) 100%);
        color: var(--text-light);
        padding: 18px 24px;
        border-radius: 16px;
        margin-bottom: 18px;
        display: flex; align-items: center; gap: 16px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.25);
      }}
      .brand-logo {{
        height: 56px; width: auto; border-radius: 10px;
        background: rgba(255,255,255,0.10); padding: 6px; backdrop-filter: blur(4px);
      }}
      .brand-header h1 {{ margin: 0; font-size: 30px; line-height: 1.2; letter-spacing: 0.3px; }}
      .brand-header p  {{ margin: 6px 0 0 0; opacity: 0.92; font-size: 14px; }}

      /* Sticky actions bar */
      .sticky-actions {{
        position: sticky; top: 0; z-index: 5; margin-bottom: 16px;
        background: linear-gradient(98deg, rgba(14,87,211,0.2), rgba(10,43,109,0.15));
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(8px);
        padding: 10px 12px; border-radius: 12px;
        display: flex; align-items: center; gap: 8px;
      }}
      .pill-mini {{
        display:inline-flex; align-items:center; gap:6px;
        padding:6px 10px; border-radius:999px;
        background: rgba(255,255,255,0.10); color: var(--text-light);
        font-weight:700; font-size:12px; border: 1px solid rgba(255,255,255,0.14);
      }}
      .link-btn {{
        padding: 10px 14px; border-radius: 12px; text-decoration: none;
        background: #f1f5f9; color: #0f172a; font-weight: 700;
        border: 1px solid #e2e8f0; display: inline-block;
        transition: transform .08s ease, box-shadow .12s ease;
      }}
      .link-btn:hover {{ transform: translateY(-1px); box-shadow: 0 8px 20px rgba(0,0,0,0.18); }}
      .link-btn.primary {{ background: var(--brand-primary); color: #FFFFFF; border: none; }}

      /* Cards */
      .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
      @media (max-width: 1000px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} }}
      @media (max-width: 680px)  {{ .grid {{ grid-template-columns: 1fr; }} }}

      .property-card {{
        background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 18px; box-shadow: 0 10px 24px rgba(0,0,0,0.18);
        overflow: hidden; border: 1px solid #e6edf3;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
      }}
      .property-card:hover {{ transform: translateY(-3px); box-shadow: 0 16px 32px rgba(0,0,0,0.22); }}
      .card-image {{ width: 100%; height: 240px; object-fit: cover; display: block; }}
      .card-body  {{ padding: 14px 16px; }}

      .badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }}
      .badge {{ display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; background: #eef2ff; color: #1e293b; border: 1px solid #e5e7eb; }}
      .badge-primary {{ background: var(--brand-primary); color: #FFFFFF; border: none; }}
      .badge-accent  {{ background: var(--brand-accent);  color: #FFFFFF; border: none; }}

      .pill {{
        display:inline-block; padding:4px 8px; border-radius:999px; background:#eef2ff; color:#1e293b;
        font-weight:700; font-size:12px; border:1px solid #e5e7eb; margin-bottom: 6px;
      }}
      .price {{ color: var(--brand-primary); font-weight: 800; font-size: 20px; }}

      .meta  {{ color: #334155; font-size: 13px; margin-top: 2px; }}
      .desc  {{ margin-top: 8px; color:#334155; line-height: 1.45; }}

      .cta-row {{ display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }}
      .card-actions {{ display:flex; gap:8px; margin-top:10px; }}

      /* Floating shortlist drawer */
      .drawer {{
        position: sticky; top: 72px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.16);
        backdrop-filter: blur(10px);
        padding: 12px; border-radius: 12px; color: var(--text-light);
      }}
      .drawer h4 {{ margin: 2px 0 10px 0; font-size: 16px; }}
      .drawer-item {{ font-size: 13px; color: var(--text-light); margin-bottom: 8px; }}
      .drawer-caption {{ font-size: 11px; color: var(--text-muted); }}
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Header (raw HTML)
# -----------------------------
if logo_src:
    st.markdown(
        f"""
        <div class="brand-header">
          {logo_src}
          <div>
            <h1>Prasad Reality Vizag</h1>
            <p>Browse, filter, and shortlist homes in Visakhapatnam—then share via WhatsApp in seconds.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div class="brand-header">
          <div>
            <h1>🏡 Prasad Reality Vizag</h1>
            <p>Browse, filter, and shortlist homes in Visakhapatnam—then share via WhatsApp in seconds.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# -----------------------------
# Data (your listings)
# -----------------------------
BASE_PROPERTIES = [
    {
        "id": "VRV-007",
        "title": "2BHK Flat — Sai Santhoshi Residence (2nd Floor)",
        "locality": "Chinnamushidiwada",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 0.0,
        "size_sqft": 850,
        "bed": 2, "bath": 2,
        "lat": 17.7780, "lon": 83.2350,
        "img": "https://images.unsplash.com/photo-1507089943778-0d63b1f95b42?w=1200",
        "desc": "Group House near Indira Gandhi Park & Saradapeetam. Car parking available. Each floor has 2 flats.",
        "tags": ["Best for Families", "Excellent Connectivity"],
        "is_premium": False, "is_new_listing": True, "family_friendly": True
    },
    {
        "id": "VRV-008",
        "title": "Commercial Property — Prime Maddilapalem (1200 Sq. Yards)",
        "locality": "Maddilapalem",
        "condition": "New",
        "property_type": "Commercial",
        "price_lakhs": 0.0,
        "size_sqft": 10800,
        "bed": 0, "bath": 0,
        "lat": 17.7365, "lon": 83.3219,
        "img": "https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200",
        "desc": "Ideal for showrooms, offices, complexes. High visibility & excellent connectivity in Vizag’s busiest zone.",
        "tags": ["Investment Opportunity", "High Visibility"],
        "is_premium": True, "is_new_listing": True, "family_friendly": False
    },
    {
        "id": "VRV-009",
        "title": "Premium 3BHK — Seethammadhara (2050 sqft, 3rd Floor)",
        "locality": "Seethammadhara",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 205.0,
        "size_sqft": 2050,
        "bed": 3, "bath": 3,
        "lat": 17.7449, "lon": 83.3120,
        "img": "https://images.unsplash.com/photo-1582582429416-d1e9b7a8479f?w=1200",
        "desc": "One flat per floor. False ceiling & quality woodwork. Balcony & corridor. CCTV, power backup, Johnson lift. 100% Vastu.",
        "tags": ["Premium", "Vastu", "New Listing"],
        "is_premium": True, "is_new_listing": True, "family_friendly": True
    },
    {
        "id": "VRV-010",
        "title": "Open Plot — Borapeta, Bheemili (567 Sq. Yards)",
        "locality": "Bheemili",
        "condition": "New",
        "property_type": "Plot",
        "price_lakhs": 113.4,
        "size_sqft": 5103,
        "bed": 0, "bath": 0,
        "lat": 17.9050, "lon": 83.4520,
        "img": "https://images.unsplash.com/photo-1523419409543-a4c7457fb928?w=1200",
        "desc": "South-facing 60×85 opposite Ramki Vacation Resorts Gate Road. Peaceful location for investment or your dream home.",
        "tags": ["Investment", "Peaceful"],
        "is_premium": False, "is_new_listing": True, "family_friendly": True
    },
]

# -----------------------------
# Session
# -----------------------------
if "properties" not in st.session_state:
    st.session_state.properties = list(BASE_PROPERTIES)
if "shortlist" not in st.session_state:
    st.session_state.shortlist = []

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.title("Filter Properties")
localities = sorted({p.get("locality", "") for p in st.session_state.properties})
conditions = ["New", "Old"]
prop_types = ["Apartment", "Individual House", "Plot", "Commercial"]

selected_localities = st.sidebar.multiselect("Area / Locality", options=localities, default=localities)
selected_condition = st.sidebar.radio("Property Condition", options=["All"] + conditions, index=0)
selected_type = st.sidebar.radio("Property Type", options=["All"] + prop_types, index=0)
search_text = st.sidebar.text_input("Keyword search", placeholder="e.g., sea view, garden, parking, Vastu")
sort_by = st.sidebar.selectbox(
    "Sort by",
    ["Price (low → high)", "Price (high → low)", "Size (small → large)", "Size (large → small)", "Newest Listings"],
    index=0,
)
st.sidebar.markdown("---")
show_map = st.sidebar.checkbox("Show heatmap of results", value=ENABLE_HEATMAP)

# -----------------------------
# Helpers
# -----------------------------
def format_price_lakhs(price_lakhs: float | int | None) -> str:
    if not price_lakhs or price_lakhs <= 0:
        return "Price on request"
    return f"₹{price_lakhs:.1f} Lakhs"

def price_per_sft(price_lakhs: float, size_sqft: float) -> str | None:
    if price_lakhs and price_lakhs > 0 and size_sqft and size_sqft > 0:
        ppsf = (price_lakhs * 100000) / float(size_sqft)
        return f"₹{ppsf:,.0f}/sft"
    return None

def whatsapp_link(number: str, text: str) -> str:
    return f"https://wa.me/{number}?text=" + quote_plus(text)

# -----------------------------
# Filtering
# -----------------------------
def apply_filters(data):
    df = pd.DataFrame(data)
    if df.empty:
        return []
    df = df[df["locality"].isin(selected_localities)]
    if selected_condition != "All":
        df = df[df["condition"] == selected_condition]
    if selected_type != "All":
        df = df[df["property_type"] == selected_type]
    if search_text:
        s = search_text.strip().lower()
        title = df["title"].astype(str).str.lower()
        desc  = df["desc"].astype(str).str.lower()
        df = df[title.str.contains(s) | desc.str.contains(s)]
    if sort_by == "Price (low → high)":
        df = df.sort_values(by="price_lakhs", ascending=True)
    elif sort_by == "Price (high → low)":
        df = df.sort_values(by="price_lakhs", ascending=False)
    elif sort_by == "Size (small → large)":
        df = df.sort_values(by="size_sqft", ascending=True)
    elif sort_by == "Size (large → small)":
        df = df.sort_values(by="size_sqft", ascending=False)
    elif sort_by == "Newest Listings":
        df = df.sort_values(by="is_new_listing", ascending=False)
    return df.to_dict(orient="records")

filtered_props = apply_filters(st.session_state.properties)

# -----------------------------
# Sticky quick actions bar (safe version)
# -----------------------------
wa_hi_india = whatsapp_link(WA_INDIA_NUM, "Hi, I'm browsing the Vizag listings!")
sticky_html = f"""
<div class="sticky-actions">
  <span class="pill-mini">🔎 Filters active</span>
  <span class="pill-mini">📦 {len(filtered_props)} results</span>
  <span class="pill-mini">⭐ Shortlist: {len(st.session_state.shortlist)}</span>
  <span style="margin-left:auto;">
    {wa_hi_india}WhatsApp (India)</a>
    https://www.instagram.com/{IG_PROFILE}/Instagram</a>
  </span>
</div>
"""
st.markdown(sticky_html, unsafe_allow_html=True)

# -----------------------------
# Header stats
# -----------------------------
left, right = st.columns([3, 2])
with left:
    st.subheader("Find your Vizag home")
    st.write("Filter by area, type, and condition. Add to shortlist and share instantly via WhatsApp.")
with right:
    st.metric("Results", f"{len(filtered_props)} properties")
    total_premium = sum(1 for p in filtered_props if p.get("is_premium"))
    st.metric("Premium listings", f"{total_premium}")

# -----------------------------
# Map heatmap (optional)
# -----------------------------
if show_map and filtered_props:
    df_map = pd.DataFrame(filtered_props)[["lat","lon","price_lakhs","size_sqft"]].rename(columns={"lat":"latitude","lon":"longitude"})
    df_map["weight"] = df_map["price_lakhs"].apply(lambda x: x if x and x > 0 else None)
    df_map["weight"] = df_map["weight"].fillna(df_map["size_sqft"].where(df_map["size_sqft"] > 0, 1)).fillna(1)
    heat_layer = pdk.Layer("HeatmapLayer", data=df_map, get_position="[longitude, latitude]", get_weight="weight", radiusPixels=56)
    view_state = pdk.ViewState(latitude=df_map["latitude"].mean(), longitude=df_map["longitude"].mean(), zoom=12)
    st.pydeck_chart(pdk.Deck(layers=[heat_layer], initial_view_state=view_state, map_style="light"))

# -----------------------------
# Property Cards (grid)
# -----------------------------
def render_property_card(prop: dict):
    price_text = format_price_lakhs(prop.get("price_lakhs", 0))
    ppsf_text = price_per_sft(prop.get("price_lakhs", 0), prop.get("size_sqft", 0))
    if ppsf_text and prop.get("property_type") in ("Apartment", "Individual House"):
        price_text = f"{price_text} · {ppsf_text}"

    badges_html = "".join([
        f'<span class="badge {"badge-primary" if t in ["New Listing", "Premium"] else ""}">{t}</span>'
        for t in prop.get("tags", [])
    ])
    locality_pill = f'<span class="pill">{prop.get("locality","")}</span>'

    msg = (
        f"Hello Prasad Reality Vizag, I'm interested in {prop.get('title')} ({prop.get('id')}) "
        f"in {prop.get('locality')}. Is it available?"
    )
    wa_india = whatsapp_link(WA_INDIA_NUM, msg)
    wa_us    = whatsapp_link(WA_US_NUM, msg)
    insta_profile = f"https://www.instagram.com/{IG_PROFILE}/"
    insta_dm_app  = f"instagram://user?username={IG_PROFILE}"

    # Card HTML
    st.markdown(
        f"""
        <div class="property-card">
          {prop.get(
          <div class="card-body">
            {locality_pill}
            <div class="badges">{badges_html}</div>
            <div class="price">{price_text}</div>
            <h3 style="margin: 6px 0 2px 0;">{prop.get('title')}</h3>
            <div class="meta">{prop.get('condition')} • {prop.get('property_type')}</div>
            <div class="meta">{prop.get('bed')} Bed · {prop.get('bath')} Bath · {prop.get('size_sqft')} sqft</div>
            <div class="card-actions">
              {wa_india}WhatsApp (India)</a>
              {wa_us}WhatsApp (US)</a>
              {insta_profile}Instagram</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("📄 Show more details"):
        st.write(prop.get("desc"))

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button(f"➕ Shortlist {prop['id']}", key=f"sl_{prop['id']}"):
            if prop not in st.session_state.shortlist:
                st.session_state.shortlist.append(prop)
                st.success(f"Added {prop['id']} to shortlist")
            else:
                st.info("Already in shortlist")
    if ENABLE_PER_CARD_DOWNLOAD:
        with c2:
            st.download_button(
                label="⬇️ Download info",
                data=pd.Series(prop).to_json(indent=2),
                file_name=f"{prop['id']}.json",
                mime="application/json",
                key=f"dl_{prop['id']}",
            )

# Render grid with a floating shortlist drawer on the side
col_grid, col_drawer = st.columns([4, 1])
with col_grid:
    st.markdown('<div class="grid">', unsafe_allow_html=True)
    for prop in filtered_props:
        render_property_card(prop)
    st.markdown('</div>', unsafe_allow_html=True)

with col_drawer:
    st.markdown(
        """
        <div class="drawer">
          <h4>⭐ Shortlist</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.shortlist:
        for p in st.session_state.shortlist:
            st.markdown(f"<div class='drawer-item'>• <strong>{p['id']}</strong> — {p['title']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='drawer-caption'>{p['locality']} • {format_price_lakhs(p.get('price_lakhs', 0))}</div>", unsafe_allow_html=True)

        # Export & share
        df_short = pd.DataFrame(st.session_state.shortlist)
        st.download_button(
            "⬇️ Download shortlist (CSV)",
            data=df_short.to_csv(index=False),
            file_name=f"shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
            use_container_width=True,
        )
        lines = [
            f"{p['id']} | {p['title']} | {p['locality']} | {format_price_lakhs(p.get('price_lakhs', 0))} | {p['size_sqft']} sqft"
            for p in st.session_state.shortlist
        ]
        msg_all = "Prasad Reality Vizag — My shortlist:\n" + "\n".join(lines)
        wa_india_all = whatsapp_link(WA_INDIA_NUM, msg_all)
        wa_us_all    = whatsapp_link(WA_US_NUM, msg_all)
        st.markdown(
            f'{wa_india_all}Share shortlist (India)</a>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'{wa_us_all}Share shortlist (US)</a>',
            unsafe_allow_html=True,
        )
    else:
        st.caption("No items yet—add properties using the ➕ buttons.")

# -----------------------------
# Lead Capture (optional)
# -----------------------------
if ENABLE_LEADS:
    st.markdown("---")
    st.subheader("Lead Capture")
    with st.form("lead_capture_form"):
        name     = st.text_input("Name",  placeholder="Your full name")
        phone    = st.text_input("Phone", placeholder="e.g., +91 6309729493")
        email    = st.text_input("Email", placeholder="you@example.com")
        pref_loc = st.selectbox("Preferred locality", options=["Any"] + localities)
        pref_type= st.selectbox("Preferred type", options=["Any"] + prop_types)
        budget   = st.text_input("Budget (Lakhs)", placeholder="e.g., 80–120")
        notes    = st.text_area("Notes", placeholder="Tell us what you’re looking for…")
        submitted= st.form_submit_button("Submit lead")
        if submitted:
            if not name or not phone:
                st.warning("Please provide at least your name and phone.")
            else:
                leads = st.session_state.setdefault("leads", [])
                leads.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name, "phone": phone, "email": email,
                    "preferred_locality": pref_loc, "preferred_type": pref_type,
                    "budget_lakhs": budget, "notes": notes,
                })
                st.success("Lead submitted! Our team will reach out shortly.")
    if st.session_state.get("leads"):
        df_leads = pd.DataFrame(st.session_state.leads)
        st.dataframe(df_leads, use_container_width=True)
        st.download_button(
            "⬇️ Download leads (CSV)",
            data=df_leads.to_csv(index=False),
            file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
            mime="text/csv",
        )

# -----------------------------
# Instagram embed (optional)
# -----------------------------
if ENABLE_INSTAGRAM:
    from streamlit.components.v1 import html as st_html
    st.markdown("---")
    st.subheader(f"Instagram Feed — @{IG_PROFILE}")
    st.caption("Paste a public Instagram post URL to embed it below (Reels/Posts).")
    insta_url = st.text_input("Instagram post URL", placeholder="https://www.instagram.com/p/<post_id>/")
    if insta_url:
        embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{insta_url}" data-instgrm-version="14"
                    style="background:#FFF; border:0; margin: 1px; max-width:540px; padding:0; width:100%;"></blockquote>
        <script async src="https://wwwd.js</script>
        """
        st_html(embed_html, height=600)
    else:
        st.markdown(
            f'https://www.instagram.com/{IG_PROFILE}/Open Instagram Profile</a>',
            unsafe_allow_html=True,
        )

# -----------------------------
# Footer (raw HTML)
# -----------------------------
st.markdown(
    """
    <div style="margin-top: 20px; color:#e2e8f0    <div style="margin-top: 20px; color:#e2e8f0;">
      <strong>Prototype notes:</strong> Mocked data only, no backend. For production: connect real listings & social leads.
      <br>Contact via WhatsApp India (+91 6309729493) or US (+1 786 420 9015).
    </div>
    """,
    unsafe_allow_html=True,
