# streamlit_app.py
# -------------------------------------------------------------
# Prasad Reality Vizag — Streamlit Showcase (Enhanced Prototype)
# Features: Filters, Analytics, Heatmap, Lead Capture, Instagram Embeds,
# WhatsApp shortlist export, per-property contact CTAs.
# -------------------------------------------------------------
# Run:
#   pip install -r requirements.txt
#   streamlit run streamlit_app.py
# -------------------------------------------------------------

import streamlit as st
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
import pydeck as pdk
import streamlit.components.v1 as components

# -------------------------------
# APP SETUP & BRANDING
# -------------------------------
st.set_page_config(
    page_title="Prasad Reality Vizag — Property Showcase",
    page_icon="🏡",
    layout="wide",
)

BRAND_PRIMARY = "#0A7E8C"  # Teal
BRAND_ACCENT = "#F5A623"    # Warm accent (orange)
BRAND_DARK = "#0B2E33"      # Deep teal/dark
LIGHT_BG = "#F7FAFC"        # Light gray-blue

st.markdown(
    f"""
    <style>
        .main .block-container {{ padding-top: 1.2rem; }}
        body {{ background-color: {LIGHT_BG}; }}
        .brand-header {{
            background: linear-gradient(90deg, {BRAND_PRIMARY} 0%, {BRAND_DARK} 100%);
            color: white; padding: 24px 28px; border-radius: 14px; margin-bottom: 18px;
        }}
        .brand-header h1 {{ margin: 0; font-size: 32px; }}
        .brand-header p {{ margin: 6px 0 0 0; opacity: 0.9; }}
        .property-card {{
            background: white; border-radius: 16px; box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            overflow: hidden; margin-bottom: 16px; border: 1px solid #e9eef2;
        }}
        .card-image {{ width: 100%; height: 180px; object-fit: cover; display: block; }}
        .card-body {{ padding: 16px 18px; }}
        .badges {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 8px; }}
        .badge {{
            display: inline-block; padding: 6px 10px; border-radius: 999px; font-size: 12px; font-weight: 600;
            background: #edf2f7; color: #2d3748; border: 1px solid #e2e8f0;
        }}
        .badge-primary {{ background: {BRAND_PRIMARY}; color: white; border: none; }}
        .badge-accent {{ background: {BRAND_ACCENT}; color: white; border: none; }}
        .price {{ color: {BRAND_PRIMARY}; font-weight: 700; font-size: 20px; }}
        .meta {{ color: #4a5568; font-size: 13px; margin-top: 2px; }}
        .cta-row {{ display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }}
        .link-btn {{
            padding: 8px 12px; border-radius: 10px; text-decoration: none; background: #f1f5f9; color: #0f172a;
            font-weight: 600; border: 1px solid #e2e8f0; display: inline-block;
        }}
        .link-btn.primary {{ background: {BRAND_PRIMARY}; color: white; border: none; }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="brand-header">
        <h1>🏡 Prasad Reality Vizag</h1>
        <p>Digital showcase for homes in Visakhapatnam — browse, filter, and shortlist in seconds.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# -------------------------------
# MOCK DATA (No database; all in code)
# -------------------------------
BASE_PROPERTIES = [
    {
        "id": "VRV-001",
        "title": "Premium 3BHK Apartment — Sea View",
        "locality": "MVP Colony",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 120.0,
        "size_sqft": 1600,
        "bed": 3,
        "bath": 3,
        "lat": 17.7489,
        "lon": 83.3365,
        "img": "https://images.unsplash.com/photo-1505693416383-83d887b81a56?w=1200",
        "desc": "Modern tower apartment with panoramic Bay of Bengal views, close to schools & parks.",
        "tags": ["New Listing", "Premium", "Best for Families"],
        "is_premium": True,
        "is_new_listing": True,
        "family_friendly": True,
    },
    {
        "id": "VRV-002",
        "title": "Cozy 2BHK Individual House",
        "locality": "Visalakshinagar",
        "condition": "Old",
        "property_type": "Individual House",
        "price_lakhs": 72.5,
        "size_sqft": 1100,
        "bed": 2,
        "bath": 2,
        "lat": 17.7635,
        "lon": 83.3482,
        "img": "https://images.unsplash.com/photo-1560185127-6a93464c7f5a?w=1200",
        "desc": "Quiet lane, independent home with a small garden. Ideal for couples or small families.",
        "tags": ["Budget-Friendly", "Calm Neighbourhood"],
        "is_premium": False,
        "is_new_listing": False,
        "family_friendly": True,
    },
    {
        "id": "VRV-003",
        "title": "Elegant 4BHK Apartment — City Skyline",
        "locality": "Hanumanthawaka",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 145.0,
        "size_sqft": 1900,
        "bed": 4,
        "bath": 4,
        "lat": 17.7410,
        "lon": 83.3166,
        "img": "https://images.unsplash.com/photo-1617104125948-c2ca1964b4a2?w=1200",
        "desc": "Premium tower apartment near transit hubs. Spacious, bright, and well-ventilated.",
        "tags": ["Premium", "New Listing"],
        "is_premium": True,
        "is_new_listing": True,
        "family_friendly": True,
    },
    {
        "id": "VRV-004",
        "title": "3BHK Individual House — Corner Plot",
        "locality": "MVP Colony",
        "condition": "Old",
        "property_type": "Individual House",
        "price_lakhs": 98.0,
        "size_sqft": 1500,
        "bed": 3,
        "bath": 3,
        "lat": 17.7441,
        "lon": 83.3350,
        "img": "https://images.unsplash.com/photo-1600585154082-9d410a0fb096?w=1200",
        "desc": "Corner home with ample sunlight and parking. Easy access to main roads.",
        "tags": ["Best for Families", "Parking"],
        "is_premium": False,
        "is_new_listing": False,
        "family_friendly": True,
    },
    {
        "id": "VRV-005",
        "title": "Smart 2BHK Apartment — Move-in Ready",
        "locality": "Visalakshinagar",
        "condition": "New",
        "property_type": "Apartment",
        "price_lakhs": 85.0,
        "size_sqft": 1200,
        "bed": 2,
        "bath": 2,
        "lat": 17.7590,
        "lon": 83.3500,
        "img": "https://images.unsplash.com/photo-1519710164239-da123dc03ef4?w=1200",
        "desc": "Fresh interiors, great ventilation, and close to the beach. Ideal starter home.",
        "tags": ["New Listing", "Starter Home"],
        "is_premium": False,
        "is_new_listing": True,
        "family_friendly": True,
    },
    {
        "id": "VRV-006",
        "title": "Spacious 5BHK Individual House — Quiet Street",
        "locality": "Hanumanthawaka",
        "condition": "Old",
        "property_type": "Individual House",
        "price_lakhs": 165.0,
        "size_sqft": 2400,
        "bed": 5,
        "bath": 4,
        "lat": 17.7389,
        "lon": 83.3149,
        "img": "https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=1200",
        "desc": "Large family home with ample storage, balconies, and backyard space.",
        "tags": ["Premium", "Best for Families"],
        "is_premium": True,
        "is_new_listing": False,
        "family_friendly": True,
    },
]

# -------------------------------
# SESSION STATE
# -------------------------------
if "properties" not in st.session_state:
    st.session_state.properties = list(BASE_PROPERTIES)
if "shortlist" not in st.session_state:
    st.session_state.shortlist = []
if "leads" not in st.session_state:
    st.session_state.leads = []
if "analytics" not in st.session_state:
    st.session_state.analytics = {
        'locality_counts': {},
        'condition_counts': {},
        'type_counts': {},
        'search_terms': {},
        'sort_counts': {},
    }
if "prev_filters" not in st.session_state:
    st.session_state.prev_filters = {
        'localities': None, 'condition': None, 'type': None, 'search': None, 'sort': None
    }

# -------------------------------
# SIDEBAR — Filters & Actions
# -------------------------------
st.sidebar.title("Filter Properties")
localities = sorted({p["locality"] for p in st.session_state.properties})
conditions = ["New", "Old"]
prop_types = ["Apartment", "Individual House"]

selected_localities = st.sidebar.multiselect(
    "Area / Locality",
    options=localities,
    default=localities,
)
selected_condition = st.sidebar.radio(
    "Property Condition",
    options=["All"] + conditions,
    index=0,
)
selected_type = st.sidebar.radio(
    "Property Type",
    options=["All"] + prop_types,
    index=0,
)
search_text = st.sidebar.text_input("Keyword search", placeholder="e.g., sea view, garden, parking")
sort_by = st.sidebar.selectbox(
    "Sort by",
    ["Price (low → high)", "Price (high → low)", "Size (small → large)", "Size (large → small)", "Newest Listings"],
    index=0,
)

# --- Analytics update (only when filter changes) ---
prev = st.session_state.prev_filters
loc_set = tuple(sorted(selected_localities))
if prev['localities'] != loc_set:
    for loc in selected_localities:
        st.session_state.analytics['locality_counts'][loc] = st.session_state.analytics['locality_counts'].get(loc, 0) + 1
    st.session_state.prev_filters['localities'] = loc_set
if prev['condition'] != selected_condition:
    st.session_state.analytics['condition_counts'][selected_condition] = st.session_state.analytics['condition_counts'].get(selected_condition, 0) + 1
    st.session_state.prev_filters['condition'] = selected_condition
if prev['type'] != selected_type:
    st.session_state.analytics['type_counts'][selected_type] = st.session_state.analytics['type_counts'].get(selected_type, 0) + 1
    st.session_state.prev_filters['type'] = selected_type
if prev['search'] != (search_text or ''):
    term = (search_text or '').strip().lower()
    if term:
        st.session_state.analytics['search_terms'][term] = st.session_state.analytics['search_terms'].get(term, 0) + 1
    st.session_state.prev_filters['search'] = (search_text or '')
if prev['sort'] != sort_by:
    st.session_state.analytics['sort_counts'][sort_by] = st.session_state.analytics['sort_counts'].get(sort_by, 0) + 1
    st.session_state.prev_filters['sort'] = sort_by

st.sidebar.markdown("---")
show_map = st.sidebar.checkbox("Show heatmap of results", value=True)
admin_mode = st.sidebar.checkbox("Admin demo: add a property", value=False)

# -------------------------------
# FILTERING
# -------------------------------
def apply_filters(data):
    df = pd.DataFrame(data)
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

# -------------------------------
# ADMIN DEMO — Add property
# -------------------------------
if admin_mode:
    st.sidebar.subheader("Add a Property (Prototype)")
    with st.sidebar.form("add_prop_form"):
        new_id = st.text_input("ID", placeholder="e.g., VRV-007")
        new_title = st.text_input("Title", placeholder="e.g., Modern 3BHK near beach")
        new_locality = st.selectbox("Locality", options=localities)
        new_condition = st.selectbox("Condition", options=conditions)
        new_type = st.selectbox("Type", options=prop_types)
        new_price = st.number_input("Price (lakhs)", min_value=10.0, max_value=1000.0, step=1.0, value=95.0)
        new_size = st.number_input("Size (sqft)", min_value=300, max_value=5000, step=50, value=1350)
        new_bed = st.number_input("Bedrooms", min_value=1, max_value=10, step=1, value=3)
        new_bath = st.number_input("Bathrooms", min_value=1, max_value=10, step=1, value=3)
        new_lat = st.number_input("Latitude", value=17.7440, format="%.6f")
        new_lon = st.number_input("Longitude", value=83.3350, format="%.6f")
        new_img = st.text_input("Image URL", value="https://images.unsplash.com/photo-1600585154082-9d410a0fb096?w=1200")
        new_desc = st.text_area("Short description", value="Bright interiors, well-connected locality.")
        is_premium = st.checkbox("Premium", value=False)
        is_new_list = st.checkbox("New Listing", value=True)
        family_ok = st.checkbox("Best for Families", value=True)
        submitted = st.form_submit_button("Add to showcase")
        if submitted:
            if not new_id or not new_title:
                st.sidebar.error("Please provide at least an ID and Title.")
            else:
                st.session_state.properties.append({
                    "id": new_id,
                    "title": new_title,
                    "locality": new_locality,
                    "condition": new_condition,
                    "property_type": new_type,
                    "price_lakhs": float(new_price),
                    "size_sqft": int(new_size),
                    "bed": int(new_bed),
                    "bath": int(new_bath),
                    "lat": float(new_lat),
                    "lon": float(new_lon),
                    "img": new_img,
                    "desc": new_desc,
                    "tags": [tag for tag, flag in [("Premium", is_premium), ("New Listing", is_new_list), ("Best for Families", family_ok)] if flag],
                    "is_premium": bool(is_premium),
                    "is_new_listing": bool(is_new_list),
                    "family_friendly": bool(family_ok),
                })
                st.sidebar.success("Property added to in-memory showcase!")

# -------------------------------
# HEADER STATS
# -------------------------------
left, right = st.columns([3, 2])
with left:
    st.subheader("Find your Vizag home")
    st.write("Use filters to explore properties by area, condition, and type. Add to shortlist and share easily.")
with right:
    st.metric("Results", f"{len(filtered_props)} properties")
    total_premium = sum(1 for p in filtered_props if p.get("is_premium"))
    st.metric("Premium listings", f"{total_premium}")

# -------------------------------
# ANALYTICS DASHBOARD
# -------------------------------
st.markdown("---")
st.subheader("Filter Usage Analytics (Prototype)")
ac = st.session_state.analytics
col_a, col_b = st.columns(2)
with col_a:
    st.write("**Localities usage**")
    st.bar_chart(pd.Series(ac['locality_counts']))
    st.write("**Property type usage**")
    st.bar_chart(pd.Series(ac['type_counts']))
with col_b:
    st.write("**Condition usage**")
    st.bar_chart(pd.Series(ac['condition_counts']))
    st.write("**Sort choice usage**")
    st.bar_chart(pd.Series(ac['sort_counts']))
if ac['search_terms']:
    st.write("**Top search keywords**")
    df_terms = pd.DataFrame(sorted(ac['search_terms'].items(), key=lambda x: x[1], reverse=True), columns=["term","count"])
    st.dataframe(df_terms, use_container_width=True)
else:
    st.caption("No search terms recorded yet.")

# -------------------------------
# MAP — HEATMAP (pydeck)
# -------------------------------
if show_map and filtered_props:
    df_map = pd.DataFrame(filtered_props)[['lat','lon','price_lakhs']].rename(columns={'lat':'latitude','lon':'longitude'})
    heat_layer = pdk.Layer(
        'HeatmapLayer',
        data=df_map,
        get_position='[longitude, latitude]',
        aggregation='MEAN',
        get_weight=1,
        radiusPixels=40,
    )
    view_state = pdk.ViewState(latitude=df_map['latitude'].mean(), longitude=df_map['longitude'].mean(), zoom=12)
    st.pydeck_chart(pdk.Deck(layers=[heat_layer], initial_view_state=view_state, map_style='light'))

# -------------------------------
# PROPERTY GRID
# -------------------------------

def render_property_card(prop):
    badges_html = "".join([f'<span class="badge {"badge-primary" if t in ["New Listing", "Premium"] else ""}' + f'">{t}</span>' for t in prop.get("tags", [])])
    msg = (
        f"Hello Prasad Reality Vizag, I'm interested in {prop['title']} ({prop['id']}) in {prop['locality']}. Is it available?"
    )
    wa_india = f"https://wa.me/916309729493?text=" + quote_plus(msg)
    wa_us = f"https://wa.me/17864209015?text=" + quote_plus(msg)
    insta_profile = "https://www.instagram.com/prasad.reality_vizag/"
    insta_dm_app = "instagram://user?username=prasad.reality_vizag"

    st.markdown(
        f"""
        <div class="property-card">
            <img class="card-image" src="{prop['img']}" alt="property image">
            <div class="card-body">
                <div class="badges">{badges_html}</div>
                <div class="price">₹{int(prop['price_lakhs'])} Lakhs</div>
                <h3 style="margin: 6px 0 2px 0;">{prop['title']}</h3>
                <div class="meta">{prop['locality']} • {prop['condition']} • {prop['property_type']}</div>
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

    c1, c2, c3 = st.columns([1, 1, 2])
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

# -------------------------------
# SHORTLIST PANEL
# -------------------------------
st.markdown("---")
st.subheader("Your Shortlist")
if st.session_state.shortlist:
    sh_cols = st.columns(3)
    for i, prop in enumerate(st.session_state.shortlist):
        with sh_cols[i % 3]:
            st.write(f"**{prop['id']} — {prop['title']}**")
            st.caption(f"{prop['locality']} • ₹{int(prop['price_lakhs'])} Lakhs • {prop['size_sqft']} sqft")
            if st.button(f"Remove {prop['id']}", key=f"rm_{prop['id']}"):
                st.session_state.shortlist = [p for p in st.session_state.shortlist if p["id"] != prop["id"]]
                st.experimental_rerun()
    df_short = pd.DataFrame(st.session_state.shortlist)
    st.download_button(
        "⬇️ Download shortlist (CSV)",
        data=df_short.to_csv(index=False),
        file_name=f"shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )

    # WhatsApp export of shortlist (India/US)
    lines = []
    for p in st.session_state.shortlist:
        lines.append(f"{p['id']} | {p['title']} | {p['locality']} | ₹{int(p['price_lakhs'])} Lakhs | {p['size_sqft']} sqft")
    msg = "Prasad Reality Vizag — My shortlist:\n" + "\n".join(lines)
    wa_india_all = "https://wa.me/916309729493?text=" + quote_plus(msg)
    wa_us_all = "https://wa.me/17864209015?text=" + quote_plus(msg)
    c_ind, c_us = st.columns(2)
    with c_ind:
        st.link_button("Send shortlist via WhatsApp (India)", wa_india_all)
    with c_us:
        st.link_button("Send shortlist via WhatsApp (US)", wa_us_all)
else:
    st.info("Your shortlist is empty. Add properties using the ➕ button on each card.")

# -------------------------------
# LEAD CAPTURE
# -------------------------------
st.markdown("---")
st.subheader("Lead Capture")
with st.form("lead_capture_form"):
    name = st.text_input("Name", placeholder="Your full name")
    phone = st.text_input("Phone", placeholder="e.g., +91 6309729493")
    email = st.text_input("Email", placeholder="you@example.com")
    pref_loc = st.selectbox("Preferred locality", options=["Any"] + localities)
    pref_type = st.selectbox("Preferred type", options=["Any"] + prop_types)
    budget = st.text_input("Budget (Lakhs)", placeholder="e.g., 80–120")
    notes = st.text_area("Notes", placeholder="Tell us what you’re looking for…")
    submitted = st.form_submit_button("Submit lead")
    if submitted:
        if not name or not phone:
            st.warning("Please provide at least your name and phone.")
        else:
            st.session_state.leads.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'name': name,
                'phone': phone,
                'email': email,
                'preferred_locality': pref_loc,
                'preferred_type': pref_type,
                'budget_lakhs': budget,
                'notes': notes,
            })
            st.success("Lead submitted! Our team will reach out shortly.")

if st.session_state.leads:
    df_leads = pd.DataFrame(st.session_state.leads)
    st.dataframe(df_leads, use_container_width=True)
    st.download_button(
        "⬇️ Download leads (CSV)",
        data=df_leads.to_csv(index=False),
        file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv",
        mime="text/csv",
    )
else:
    st.info("No leads yet. Use the form above to capture inquiries.")

# -------------------------------
# INSTAGRAM FEED EMBED
# -------------------------------
st.markdown("---")
st.subheader("Instagram Feed — @prasad.reality_vizag")
st.caption("Paste a public Instagram post URL to embed it below (Reels/Posts).")
insta_url = st.text_input("Instagram post URL", placeholder="https://www.instagram.com/p/<post_id>/")
if insta_url:
    embed_html = f"""
    <blockquote class=\"instagram-media\" data-instgrm-permalink=\"{insta_url}\" data-instgrm-version=\"14\" style=\"background:#FFF; border:0; margin: 1px; max-width:540px; padding:0; width:100%;\"></blockquote>
    <script async src=\"https://www.instagram.com/embed.js\"></script>
    """
    components.html(embed_html, height=600)
else:
    st.link_button("Open Instagram Profile", "https://www.instagram.com/prasad.reality_vizag/")

# -------------------------------
# FOOTER — Helpful notes
# -------------------------------
st.markdown(
    f"""
    <div style="margin-top: 20px; color:#475569;">
        <strong>Prototype notes:</strong> This is a demo with mocked data and no backend.\n
        <br>For production: connect real listings, WhatsApp/Instagram, and admin uploads.\n
        <br>Contact via WhatsApp India (+91 6309729493) or US (+1 786 420 9015).\n
    </div>
    """,
    unsafe_allow_html=True,
)
