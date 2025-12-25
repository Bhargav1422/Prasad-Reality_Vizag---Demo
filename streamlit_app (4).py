# streamlit_app.py (Auto logo from repo + contrast fix + only user listings)
import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
import pydeck as pdk
import streamlit.components.v1 as components
import base64
import os

st.set_page_config(page_title="Prasad Reality Vizag — Property Showcase", page_icon="🏡", layout="wide")

# Brand colors (matched to logo)
BRAND_PRIMARY = "#0E57D3"  # blue
BRAND_ACCENT  = "#FF5A3D"  # orange
BRAND_DARK    = "#0A2B6D"  # deep blue
LIGHT_BG      = "#0F172A"  # dark background for contrast (Tailwind slate-900 equivalent)
TEXT_DARK     = "#0F172A"  # text dark
TEXT_LIGHT    = "#F8FAFC"  # near-white text

# Auto-load logo from local repo file
logo_src = None
for name in ('prasad_logo.png','prasad_logo.jpg','prasad_logo.jpeg'):
    if os.path.exists(name):
        with open(name,'rb') as f:
            b64 = base64.b64encode(f.read()).decode('utf-8')
        ext = name.split('.')[-1]
        logo_src = f'data:image/{ext};base64,' + b64
        break

# CSS (escaped braces for f-string)
st.markdown(
    f"""
    <style>
      body {{ background-color: {{LIGHT_BG}}; }}
      .main .block-container {{ padding-top: 0.6rem; }}

      .brand-header {{
        background: linear-gradient(90deg, {{BRAND_PRIMARY}} 0%, {{BRAND_DARK}} 100%);
        color: {{TEXT_LIGHT}}; padding: 18px 24px; border-radius: 16px; margin-bottom: 18px;
        display: flex; align-items: center; gap: 16px;
      }}
      .brand-logo {{ height: 60px; width: auto; border-radius: 8px; background: rgba(255,255,255,0.12); padding: 6px; }}
      .brand-header h1 {{ margin: 0; font-size: 30px; line-height: 1.2; }}
      .brand-header p  {{ margin: 4px 0 0 0; opacity: 0.95; font-size: 13px; }}

      .property-card {{ background: #FFFFFF; border-radius: 18px; box-shadow: 0 10px 20px rgba(0,0,0,0.18);
                        overflow: hidden; margin-bottom: 18px; border: 1px solid #e6edf3; transition: transform 0.15s ease, box-shadow 0.15s ease; }}
      .property-card:hover {{ transform: translateY(-2px); box-shadow: 0 14px 28px rgba(0,0,0,0.22); }}
      .card-image {{ width: 100%; height: 260px; object-fit: cover; display: block; }}
      .card-body  {{ padding: 16px 18px; }}

      .badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }}
      .badge {{ display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 600; background: #eef2ff; color: #1e293b; border: 1px solid #e5e7eb; }}
      .badge-primary {{ background: {{BRAND_PRIMARY}}; color: #FFFFFF; border: none; }}
      .badge-accent  {{ background: {{BRAND_ACCENT}};  color: #FFFFFF; border: none; }}

      .price {{ color: {{BRAND_PRIMARY}}; font-weight: 800; font-size: 22px; }}
      .card-body h3 {{ color: #0F172A; font-weight: 800; }} /* Headline contrast */
      .meta  {{ color: #334155; font-size: 13px; margin-top: 2px; }}
      .cta-row {{ display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }}
      .link-btn {{ padding: 10px 14px; border-radius: 12px; text-decoration: none; background: #f1f5f9; color: #0f172a; font-weight: 700; border: 1px solid #e2e8f0; display: inline-block; }}
      .link-btn.primary {{ background: {{BRAND_PRIMARY}}; color: #FFFFFF; border: none; }}

      .pill {{ display:inline-block; padding:4px 8px; border-radius:999px; background:#eef2ff; color:#1e293b; font-weight:700; font-size:12px; border:1px solid #e5e7eb; }}
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
if logo_src:
    st.markdown(
        f"""
        <div class="brand-header">
          <img class="brand-logo" src="{logo_src}" alt="brand logo">
          <div>
            <h1>🏡 Prasad Reality Vizag</h1>
            <p>Digital showcase for homes in Visakhapatnam — browse, filter, and shortlist in seconds.</p>
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
            <p>Digital showcase for homes in Visakhapatnam — browse, filter, and shortlist in seconds.</p>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Listings — only user-provided
BASE_PROPERTIES = [
    {
        "id": "VRV-007",
        "title": "2BHK Flat — Sai Santhoshi Residence (2nd Floor)",
        "locality": "Chinnamushidiwada",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 0.0,
        "size_sqft": 850,
        "bed": 2,
        "bath": 2,
        "lat": 17.7780,
        "lon": 83.2350,
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

# Session state
if "properties" not in st.session_state:
    st.session_state.properties = list(BASE_PROPERTIES)
if "shortlist" not in st.session_state:
    st.session_state.shortlist = []
if "leads" not in st.session_state:
    st.session_state.leads = []

# Sidebar filters
st.sidebar.title("Filter Properties")
localities = sorted({p["locality"] for p in st.session_state.properties})
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
show_map = st.sidebar.checkbox("Show heatmap of results", value=True)

# Filtering
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
        df = df[df["title"].str.lower().str.contains(s) | df["desc"].str.lower().str.contains(s)]
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

# Header stats
left, right = st.columns([3, 2])
with left:
    st.subheader("Find your Vizag home")
    st.write("Use filters to explore properties by area, condition, and type. Add to shortlist and share easily.")
with right:
    st.metric("Results", f"{len(filtered_props)} properties")
    total_premium = sum(1 for p in filtered_props if p.get("is_premium"))
    st.metric("Premium listings", f"{total_premium}")

# Map heatmap
if show_map and filtered_props:
    df_map = pd.DataFrame(filtered_props)[['lat','lon','price_lakhs']].rename(columns={'lat':'latitude','lon':'longitude'})
    heat_layer = pdk.Layer(
        'HeatmapLayer', data=df_map,
        get_position='[longitude, latitude]', aggregation='MEAN', get_weight=1,
        radiusPixels=60,
    )
    view_state = pdk.ViewState(latitude=df_map['latitude'].mean(), longitude=df_map['longitude'].mean(), zoom=12)
    st.pydeck_chart(pdk.Deck(layers=[heat_layer], initial_view_state=view_state, map_style='light'))

# Property cards

def render_property_card(prop):
    price_val = prop.get("price_lakhs")
    price_html = ""
    if price_val and price_val > 0:
        price_html = f"₹{price_val:.1f} Lakhs"
        if prop.get("size_sqft") and prop.get("property_type") in ("Apartment", "Individual House"):
            ppsf = (price_val * 100000) / float(prop["size_sqft"])
            price_html += f" · ₹{ppsf:,.0f}/sft"

    badges_html = "".join([
        f'<span class="badge {"badge-primary" if t in ["New Listing", "Premium"] else ""}">{t}</span>'
        for t in prop.get("tags", [])
    ])

    locality_pill = f'<span class="pill">{prop["locality"]}</span>'

    msg = (
        f"Hello Prasad Reality Vizag, I'm interested in {prop['title']} ({prop['id']}) "
        f"in {prop['locality']}. Is it available?"
    )
    wa_india      = "https://wa.me/916309729493?text=" + quote_plus(msg)
    wa_us         = "https://wa.me/17864209015?text=" + quote_plus(msg)
    insta_profile = "https://www.instagram.com/prasad.reality_vizag/"
    insta_dm_app  = "instagram://user?username=prasad.reality_vizag"

    st.markdown(
        f"""
        <div class="property-card">
          <img class="card-image" src="{prop['img']}" alt="property image">
          <div class="card-body">
            {locality_pill}
            <div class="badges">{badges_html}</div>
            <div class="price">{price_html}</div>
            <h3 style="margin: 6px 0 2px 0;">{prop['title']}</h3>
            <div class="meta">{prop['condition']} • {prop['property_type']}</div>
            <div class="meta">{prop['bed']} Bed · {prop['bath']} Bath · {prop['size_sqft']} sqft</div>
            <p style="margin-top: 10px; color:#334155;">{prop['desc']}</p>
            <div class="cta-row">
              <a class="link-btn primary" href="{wa_india}" target="_blank">WhatsApp (India)</a>
              <a class="link-btn" href="{wa_us}" target="_blank">WhatsApp (US)</a>
              <a class="link-btn" href="{insta_profile}" target="_blank">Instagram</a>
            </div>
            <div class="cta-row">
              <a class="link-btn" href="{insta_dm_app}">Open Instagram DM (App)</a>
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button(f"➕ Shortlist {prop['id']}", key=f"sl_{prop['id']}"):
            if prop not in st.session_state.shortlist:
                st.session_state.shortlist.append(prop)
                st.success(f"Added {prop['id']} to shortlist")
            else:
                st.info("Already in shortlist")
    with c2:
        st.download_button(
            label="⬇️ Download info",
            data=pd.Series(prop).to_json(indent=2),
            file_name=f"{prop['id']}.json",
            mime="application/json",
            key=f"dl_{prop['id']}",
        )

cols = st.columns(3)
for i, prop in enumerate(filtered_props):
    with cols[i % 3]:
        render_property_card(prop)

# Shortlist
st.markdown("---")
st.subheader("Your Shortlist")
if st.session_state.shortlist:
    sh_cols = st.columns(3)
    for i, prop in enumerate(st.session_state.shortlist):
        with sh_cols[i % 3]:
            st.write(f"**{prop['id']} — {prop['title']}**")
            price_line = f"₹{int(prop['price_lakhs'])} Lakhs" if prop.get("price_lakhs", 0) else "Price on request"
            st.caption(f"{prop['locality']} • {price_line} • {prop['size_sqft']} sqft")
            if st.button(f"Remove {prop['id']}", key=f"rm_{prop['id']}"):
                st.session_state.shortlist = [p for p in st.session_state.shortlist if p["id"] != prop["id"]]
                st.experimental_rerun()

    df_short = pd.DataFrame(st.session_state.shortlist)
    st.download_button(
        "⬇️ Download shortlist (CSV)", data=df_short.to_csv(index=False),
        file_name=f"shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv",
    )

    lines = [
        f"{p['id']} | {p['title']} | {p['locality']} | "
        f"{('₹' + str(int(p['price_lakhs'])) + ' Lakhs') if p.get('price_lakhs', 0) else 'Price on request'} | "
        f"{p['size_sqft']} sqft"
        for p in st.session_state.shortlist
    ]
    msg = "Prasad Reality Vizag — My shortlist:\n" + "\n".join(lines)
    wa_india_all = "https://wa.me/916309729493?text=" + quote_plus(msg)
    wa_us_all    = "https://wa.me/17864209015?text=" + quote_plus(msg)

    c_ind, c_us = st.columns(2)
    with c_ind:
        st.link_button("Send shortlist via WhatsApp (India)", wa_india_all)
    with c_us:
        st.link_button("Send shortlist via WhatsApp (US)", wa_us_all)
else:
    st.info("Your shortlist is empty. Add properties using the ➕ button on each card.")

# Lead Capture
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
            st.session_state.leads.append({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "name": name, "phone": phone, "email": email,
                "preferred_locality": pref_loc, "preferred_type": pref_type,
                "budget_lakhs": budget, "notes": notes,
            })
            st.success("Lead submitted! Our team will reach out shortly.")

if st.session_state.leads:
    df_leads = pd.DataFrame(st.session_state.leads)
    st.dataframe(df_leads, use_container_width=True)
    st.download_button(
        "⬇️ Download leads (CSV)", data=df_leads.to_csv(index=False),
        file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv",
    )
else:
    st.info("No leads yet. Use the form above to capture inquiries.")

# Instagram embed
st.markdown("---")
st.subheader("Instagram Feed — @prasad.reality_vizag")
st.caption("Paste a public Instagram post URL to embed it below (Reels/Posts).")
insta_url = st.text_input("Instagram post URL", placeholder="https://www.instagram.com/p/<post_id>/")
if insta_url:
    embed_html = f"""
    <blockquote class=\"instagram-media\" data-instgrm-permalink=\"{insta_url}\" data-instgrm-version=\"14\"
                style=\"background:#FFF; border:0; margin: 1px; max-width:540px; padding:0; width:100%;\"></blockquote>
    <script async src=\"https://www.instagram.com/embed.js\"></script>
    """
    components.html(embed_html, height=600)
else:
    st.link_button("Open Instagram Profile", "https://www.instagram.com/prasad.reality_vizag/")

# Footer
st.markdown(
    """
    <div style="margin-top: 20px; color:#e2e8f0;">
      <strong>Prototype notes:</strong> Mocked data only, no backend. For production: connect real listings & social leads.
      <br>Contact via WhatsApp India (+91 6309729493) or US (+1 786 420 9015).
    </div>
    """,
    unsafe_allow_html=True,
)
