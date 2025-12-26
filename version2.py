
# streamlit_app.py — Components-only UI, brand-themed with your logo
import os
from datetime import datetime, timedelta, date, time
from urllib.parse import quote_plus

import pandas as pd
import streamlit as st
import pydeck as pdk
from streamlit.components.v1 import html as st_html

# -----------------------------
# Brand Theme (components-only)
# -----------------------------
st.set_page_config(
    page_title="Prasad Realty Vizag",
    page_icon="🏡",
    layout="wide",
    theme={
        "primaryColor": "#0E57D3",             # brand blue
        "backgroundColor": "#0F172A",          # dark background
        "secondaryBackgroundColor": "#1E293B", # cards/sidebar
        "textColor": "#F8FAFC",                # near-white text
        "font": "sans serif",
    }
)

# -----------------------------
# Feature toggles
# -----------------------------
ENABLE_HEATMAP   = True
ENABLE_INSTAGRAM = True      # official embed snippet via components.html
ENABLE_BOOKING   = True
ENABLE_LEADS     = True
ENABLE_SHORTLIST = True

DATA_DIR       = "."
LEADS_FILE     = os.path.join(DATA_DIR, "leads.csv")
BOOKINGS_FILE  = os.path.join(DATA_DIR, "bookings.csv")

# -----------------------------
# Contact constants
# -----------------------------
WA_INDIA_NUM = "916309729493"
WA_US_NUM    = "17864209015"
IG_HANDLE    = "prasad.reality_vizag"

# -----------------------------
# Logo loader (components-only)
# -----------------------------
def load_logo_path():
    for name in ("prasad_logo.jpg", "prasad_logo.png", "prasad_logo.jpeg"):
        path = os.path.join(DATA_DIR, name)
        if os.path.exists(path):
            return path
    return None

logo_path = load_logo_path()

# -----------------------------
# Mock data (replace later with CSVs)
# -----------------------------
mock_properties = [
    {
        "id":"VRV-101","title":"3BHK Premium — Seethammadhara (2050 sqft, 3rd Fl)",
        "locality":"Seethammadhara","condition":"New","property_type":"Apartment",
        "price_lakhs":205.0,"size_sqft":2050,"bed":3,"bath":3,
        "lat":17.7449,"lon":83.3120,
        "img":"https://images.unsplash.com/photo-1582582429416-d1e9b7a8479f?w=1200",
        "desc":"One flat per floor. False ceiling, woodwork, balcony, corridor, CCTV, power backup, Johnson lift. 100% Vastu.",
        "tags":["Premium","Vastu","New Listing"],
        "reel_url":"https://www.instagram.com/reel/C_demo_1/"
    },
    {
        "id":"VRV-102","title":"Commercial — Maddilapalem (1200 Sq. Yards)",
        "locality":"Maddilapalem","condition":"New","property_type":"Commercial",
        "price_lakhs":0.0,"size_sqft":10800,"bed":0,"bath":0,
        "lat":17.7365,"lon":83.3219,
        "img":"https://images.unsplash.com/photo-1503387762-592deb58ef4e?w=1200",
        "desc":"Ideal for showrooms/offices/complex. High visibility & connectivity in Vizag’s busiest zone.",
        "tags":["Investment","High Visibility"],
        "reel_url":"https://www.instagram.com/reel/C_demo_2/"
    },
    {
        "id":"VRV-103","title":"2BHK — Chinnamushidiwada (850 sqft, 2nd Fl)",
        "locality":"Chinnamushidiwada","condition":"New","property_type":"Apartment",
        "price_lakhs":0.0,"size_sqft":850,"bed":2,"bath":2,
        "lat":17.7780,"lon":83.2350,
        "img":"https://images.unsplash.com/photo-1507089943778-0d63b1f95b42?w=1200",
        "desc":"Group House near Indira Gandhi Park & Saradapeetam. Car parking. Two flats per floor.",
        "tags":["Family Friendly","Good Connectivity"],
        "reel_url":"https://www.instagram.com/reel/C_demo_3/"
    },
    {
        "id":"VRV-104","title":"Open Plot — Bheemili (567 Sq. Yards)",
        "locality":"Bheemili","condition":"New","property_type":"Plot",
        "price_lakhs":113.4,"size_sqft":5103,"bed":0,"bath":0,
        "lat":17.9050,"lon":83.4520,
        "img":"https://images.unsplash.com/photo-1523419409543-a4c7457fb928?w=1200",
        "desc":"South-facing 60×85 opposite Ramki Vacation Resorts Gate Road. Peaceful location.",
        "tags":["Investment","Peaceful"],
        "reel_url":"https://www.instagram.com/reel/C_demo_4/"
    },
]

mock_agents = [
    {"agent_id":"AG01","name":"Prasad","phone":"+91 6309729493","territories":["Seethammadhara","Maddilapalem"],"work_days":"Mon-Sat","work_start_ist":"10:00","work_end_ist":"18:00"},
    {"agent_id":"AG02","name":"Sai","phone":"+91 9000000001","territories":["Bheemili","Chinnamushidiwada"],"work_days":"Mon-Sat","work_start_ist":"10:00","work_end_ist":"18:00"},
    {"agent_id":"AG03","name":"Anjali","phone":"+91 9000000002","territories":["Seethammadhara","Bheemili"],"work_days":"Mon-Sat","work_start_ist":"11:00","work_end_ist":"19:00"},
]

# -----------------------------
# Session init
# -----------------------------
if "properties" not in st.session_state: st.session_state.properties = mock_properties
if "shortlist"  not in st.session_state: st.session_state.shortlist  = []
if "leads"      not in st.session_state: st.session_state.leads      = []
if "bookings"   not in st.session_state: st.session_state.bookings   = []
if "agents"     not in st.session_state: st.session_state.agents     = mock_agents

# -----------------------------
# Helpers
# -----------------------------
def format_price_lakhs(price):
    if not price or price <= 0: return "Price on request"
    return f"₹{price:.1f} Lakhs"

def price_per_sft(price, size):
    if price and price > 0 and size and size > 0:
        ppsf = (price * 100000) / float(size)
        return f"₹{ppsf:,.0f}/sft"
    return None

def whatsapp_link(number, text):
    return f"https://wa.me/{number}?text=" + quote_plus(text)

def ensure_csv(file_path, columns):
    if not os.path.exists(file_path):
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

def append_row_csv(file_path, row_dict, columns):
    ensure_csv(file_path, columns)
    try:
        df = pd.read_csv(file_path)
    except Exception:
        df = pd.DataFrame(columns=columns)
    df = pd.concat([df, pd.DataFrame([row_dict])], ignore_index=True)
    df.to_csv(file_path, index=False)

def generate_ics(summary, description, start_dt, end_dt, location, organizer_email="info@prasadrealityvizag.demo"):
    ist_offset = timedelta(hours=5, minutes=30)
    start_utc  = start_dt - ist_offset
    end_utc    = end_dt - ist_offset
    fmt = lambda dt: dt.strftime("%Y%m%dT%H%M%SZ")
    uid = f"{int(datetime.now().timestamp())}@prasadrealityvizag.demo"
    return f"""BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//PrasadRealityVizag//Booking Demo//EN
CALSCALE:GREGORIAN
METHOD:REQUEST
BEGIN:VEVENT
UID:{uid}
DTSTAMP:{fmt(datetime.utcnow())}
DTSTART:{fmt(start_utc)}
DTEND:{fmt(end_utc)}
SUMMARY:{summary}
DESCRIPTION:{description}
LOCATION:{location}
ORGANIZER;CN=Prasad Realty Vizag:MAILTO:{organizer_email}
END:VEVENT
END:VCALENDAR
"""

def assign_agent(locality):
    for ag in st.session_state.agents:
        if locality in ag.get("territories", []):
            return ag
    return st.session_state.agents[0]

# -----------------------------
# Header (logo + quick actions)
# -----------------------------
col_header = st.columns([1, 3, 2])
with col_header[0]:
    if logo_path:
        st.image(logo_path, caption=None, use_column_width=True)
    else:
        st.write("🏡")

with col_header[1]:
    st.title("Prasad Realty Vizag — Demo Showcase")
    st.caption("Browse, filter, shortlist, watch reels, enquire on WhatsApp, capture leads, and book flexible visit slots.")

with col_header[2]:
    wa_hi_india = whatsapp_link(WA_INDIA_NUM, "Hi, I'm browsing the Vizag listings!")
    st.link_button("WhatsApp (India)", wa_hi_india, type="primary")
    st.link_button("Instagram", f"https://www.instagram.com/{IG_HANDLE}/")

st.divider()

# -----------------------------
# Sidebar filters (theme colors apply automatically)
# -----------------------------
st.sidebar.header("Filter Properties")
df_all = pd.DataFrame(st.session_state.properties)
localities = sorted(df_all["locality"].unique().tolist())
conditions = ["New", "Old"]
prop_types = ["Apartment", "Individual House", "Plot", "Commercial"]

selected_localities = st.sidebar.multiselect("Area / Locality", options=localities, default=localities)
selected_condition  = st.sidebar.radio("Property Condition", options=["All"] + conditions, index=0)
selected_type       = st.sidebar.radio("Property Type", options=["All"] + prop_types, index=0)
search_text         = st.sidebar.text_input("Keyword search", placeholder="e.g., sea view, garden, parking, Vastu")
sort_by             = st.sidebar.selectbox(
    "Sort by",
    ["Price (low → high)", "Price (high → low)", "Size (small → large)", "Size (large → small)", "Newest Listings"],
    index=0,
)

st.sidebar.divider()
show_map = st.sidebar.checkbox("Show heatmap of results", value=ENABLE_HEATMAP)

def apply_filters(data):
    df = pd.DataFrame(data)
    if df.empty: return []
    df = df[df["locality"].isin(selected_localities)]
    if selected_condition != "All":
        df = df[df["condition"] == selected_condition]
    if selected_type != "All":
        df = df[df["property_type"] == selected_type]
    if search_text:
        s = search_text.strip().lower()
        title = df["title"].astype(str).str.lower()
        desc  = df["desc"].astype(str).str.lower()
        df    = df[title.str.contains(s, na=False) | desc.str.contains(s, na=False)]
    if sort_by == "Price (low → high)":
        df = df.sort_values(by="price_lakhs", ascending=True)
    elif sort_by == "Price (high → low)":
        df = df.sort_values(by="price_lakhs", ascending=False)
    elif sort_by == "Size (small → large)":
        df = df.sort_values(by="size_sqft", ascending=True)
    elif sort_by == "Size (large → small)":
        df = df.sort_values(by="size_sqft", ascending=False)
    elif sort_by == "Newest Listings":
        df = df.sort_values(by="condition", ascending=False)  # demo heuristic
    return df.to_dict(orient="records")

filtered_props = apply_filters(st.session_state.properties)

# -----------------------------
# Stats row
# -----------------------------
left, right = st.columns([3, 2])
with left:
    st.subheader("Find your Vizag home")
    st.write("Filter by area, type, and condition. Add to shortlist, watch reels, and share instantly via WhatsApp.")
with right:
    st.metric("Results", f"{len(filtered_props)}")
    total_premium = sum(1 for p in filtered_props if "Premium" in p.get("tags", []))
    st.metric("Premium-tagged", f"{total_premium}")

# -----------------------------
# Map heatmap (optional)
# -----------------------------
if show_map and filtered_props:
    df_map = pd.DataFrame(filtered_props)[["lat","lon","price_lakhs","size_sqft"]].rename(columns={"lat":"latitude","lon":"longitude"})
    df_map["weight"] = df_map["price_lakhs"].apply(lambda x: x if x and x > 0 else None)
    df_map["weight"] = df_map["weight"].fillna(df_map["size_sqft"].where(df_map["size_sqft"] > 0, 1)).fillna(1)
    layer = pdk.Layer("HeatmapLayer", data=df_map, get_position="[longitude, latitude]", get_weight="weight", radiusPixels=56)
    view  = pdk.ViewState(latitude=df_map["latitude"].mean(), longitude=df_map["longitude"].mean(), zoom=12)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view, map_style="light"))

st.divider()

# -----------------------------
# Property card (components-only)
# -----------------------------
def render_property_card(prop: dict):
    pid       = prop.get("id",""); title = prop.get("title",""); locality = prop.get("locality","")
    cond      = prop.get("condition",""); ptype = prop.get("property_type","")
    bed       = prop.get("bed",0); bath = prop.get("bath",0); size = prop.get("size_sqft",0)
    img       = prop.get("img",""); desc = prop.get("desc","")
    tags      = prop.get("tags", []); reel_url = prop.get("reel_url","")

    price_text = format_price_lakhs(prop.get("price_lakhs",0))
    ppsf_text  = price_per_sft(prop.get("price_lakhs",0), size)
    if ppsf_text and ptype in ("Apartment","Individual House"):
        price_text = f"{price_text} · {ppsf_text}"

    st.image(img, caption=title, use_column_width=True)
    tag_line = " · ".join(tags) if tags else ""
    st.caption(f"{locality} • {cond} • {ptype}" + (f" • {tag_line}" if tag_line else ""))

    col_specs = st.columns(3)
    with col_specs[0]: st.write(f"**Price:** {price_text}")
    with col_specs[1]: st.write(f"**Specs:** {bed} Bed · {bath} Bath")
    with col_specs[2]: st.write(f"**Size:** {size} sqft")

    msg = f"Hello Prasad Realty Vizag, I'm interested in {title} ({pid}) in {locality}. Is it available?"
    wa_india = whatsapp_link(WA_INDIA_NUM, msg)
    wa_us    = whatsapp_link(WA_US_NUM, msg)
    col_cta = st.columns(3)
    with col_cta[0]: st.link_button("WhatsApp (India)", wa_india, type="primary")
    with col_cta[1]: st.link_button("WhatsApp (US)", wa_us)
    with col_cta[2]: st.link_button("Instagram", f"https://www.instagram.com/{IG_HANDLE}/")

    with st.expander("📄 Show more details"):
        st.write(desc)

    if ENABLE_INSTAGRAM and reel_url and reel_url.startswith("https://www.instagram.com/reel/"):
        with st.expander("🎬 Watch Reel"):
            embed_html = f"""
            <blockquote class="instagram-media" data-instgrm-permalink="{reel_url}" data-instgrm-version="14"
                        style="background:#FFF;border:0;margin:1px;max-width:540px;padding:0;width:100%;"></blockquote>
            https://www.instagram.com/embed.js</script>
            """
            st_html(embed_html, height=620)

    col_actions = st.columns(3)
    with col_actions[0]:
        if ENABLE_SHORTLIST and st.button(f"➕ Shortlist {pid}", key=f"sl_{pid}"):
            if prop not in st.session_state.shortlist:
                st.session_state.shortlist.append(prop)
                st.success(f"Added {pid} to shortlist")
            else:
                st.info("Already in shortlist")
    with col_actions[1]:
        if ENABLE_BOOKING and st.button(f"📅 Book a slot ({pid})", key=f"bk_{pid}"):
            st.session_state["booking_target"]     = prop
            st.session_state["show_booking_modal"] = True

# Render grid of properties
cols = st.columns(3)
for i, prop in enumerate(filtered_props):
    with cols[i % 3]:
        render_property_card(prop)

# -----------------------------
# Shortlist
# -----------------------------
st.divider()
st.subheader("⭐ Shortlist")
if st.session_state.shortlist:
    for p in st.session_state.shortlist:
        st.write(f"• **{p.get('id','')}** — {p.get('title','')}")
        st.caption(f"{p.get('locality','')} • {format_price_lakhs(p.get('price_lakhs', 0))}")
    df_short = pd.DataFrame(st.session_state.shortlist)
    st.download_button("⬇️ Download shortlist (CSV)", df_short.to_csv(index=False),
                       file_name=f"shortlist_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    lines = [f"{p.get('id','')} | {p.get('title','')} | {p.get('locality','')} | {format_price_lakhs(p.get('price_lakhs', 0))} | {p.get('size_sqft', 0)} sqft"
             for p in st.session_state.shortlist]
    msg_all = "Prasad Realty Vizag — My shortlist:\n" + "\n".join(lines)
    col_share = st.columns(2)
    with col_share[0]: st.link_button("Share shortlist (India)", whatsapp_link(WA_INDIA_NUM, msg_all), type="primary")
    with col_share[1]: st.link_button("Share shortlist (US)",    whatsapp_link(WA_US_NUM,    msg_all))
else:
    st.caption("No items yet—add properties using the ➕ buttons.")

# -----------------------------
# Booking modal
# -----------------------------
if ENABLE_BOOKING and st.session_state.get("show_booking_modal"):
    prop = st.session_state.get("booking_target")
    if prop:
        st.divider()
        st.subheader(f"Book a slot for {prop['id']} — {prop['title']}")
        with st.form("booking_form"):
            visit_type   = st.radio("Visit type", ["In-person visit","Video call"], index=0)
            d            = st.date_input("Select date (IST)", value=date.today())
            start        = st.time_input("Start time (IST)", value=time(11, 0))
            default_dur  = 45 if visit_type == "In-person visit" else 30
            duration_min = st.number_input("Duration (minutes)", min_value=15, max_value=180, value=default_dur, step=15)
            notes        = st.text_area("Notes", placeholder="Any preferences or questions...")
            name  = st.text_input("Your Name *")
            phone = st.text_input("Phone (WhatsApp preferred) *")
            email = st.text_input("Email (optional)")
            submitted = st.form_submit_button("Confirm booking")
            if submitted:
                if not name or not phone:
                    st.warning("Please provide at least your name and phone.")
                else:
                    start_dt_ist = datetime.combine(d, start)
                    end_dt_ist   = start_dt_ist + timedelta(minutes=int(duration_min))
                    agent        = assign_agent(prop.get("locality",""))
                    booking_id   = f"BK-{int(datetime.now().timestamp())}"
                    row = {
                        "booking_id": booking_id,
                        "lead_name": name.strip(), "lead_phone": phone.strip(),
                        "property_id": prop.get("id",""),
                        "agent_id": agent["agent_id"], "agent_name": agent["name"], "agent_phone": agent["phone"],
                        "type": "visit" if visit_type=="In-person visit" else "video",
                        "start_dt_ist": start_dt_ist.strftime("%Y-%m-%d %H:%M"),
                        "end_dt_ist": end_dt_ist.strftime("%Y-%m-%d %H:%M"),
                        "status":"scheduled","notes": notes.strip(),
                    }
                    append_row_csv(BOOKINGS_FILE, row, columns=[
                        "booking_id","lead_name","lead_phone","property_id","agent_id","agent_name","agent_phone",
                        "type","start_dt_ist","end_dt_ist","status","notes"
                    ])
                    st.session_state.bookings.append(row)

                    summary = f"Property Visit: {prop.get('id')} — {prop.get('title')}"
                    desc    = f"Agent: {agent['name']} ({agent['phone']})\nNotes: {notes}"
                    ics     = generate_ics(summary, desc, start_dt_ist, end_dt_ist, prop.get("locality","Vizag"))
                    st.download_button("⬇️ Add to calendar (ICS)", data=ics, file_name=f"{booking_id}.ics", mime="text/calendar")

                    customer_msg = (
                        f"Booking Confirmed: {prop.get('id')} — {prop.get('title')}\n"
                        f"Type: {visit_type}\nWhen (IST): {row['start_dt_ist']} to {row['end_dt_ist']}\n"
                        f"Agent: {agent['name']} ({agent['phone']})"
                    )
                    wa_customer = whatsapp_link(WA_INDIA_NUM, customer_msg)
                    wa_agent    = whatsapp_link(WA_INDIA_NUM, f"New Booking {booking_id}: {name} ({phone}) for {prop.get('id')} on {row['start_dt_ist']}")
                    col_notify = st.columns(2)
                    with col_notify[0]: st.link_button("Notify via WhatsApp (India)", wa_customer, type="primary")
                    with col_notify[1]: st.link_button("Notify agent (India)", wa_agent)

                    st.session_state["show_booking_modal"] = False
                    st.session_state["booking_target"]     = None

# -----------------------------
# Lead capture
# -----------------------------
if ENABLE_LEADS:
    st.divider()
    st.subheader("Lead Capture")
    utm = st.experimental_get_query_params()
    utm_source   = utm.get("utm_source",   [""])[0]
    utm_medium   = utm.get("utm_medium",   [""])[0]
    utm_campaign = utm.get("utm_campaign", [""])[0]
    if any([utm_source, utm_medium, utm_campaign]):
        st.caption(f"Traffic source: {utm_source or 'n/a'} / {utm_medium or 'n/a'} / {utm_campaign or 'n/a'}")

    with st.form("lead_capture_form"):
        name     = st.text_input("Name",  placeholder="Your full name")
        phone    = st.text_input("Phone", placeholder="WhatsApp preferred")
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
                row = {
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                    "name": name.strip(), "phone": phone.strip(), "email": email.strip(),
                    "preferred_locality": pref_loc, "preferred_type": pref_type,
                    "budget_lakhs": budget.strip(), "notes": notes.strip(),
                    "utm_source": utm_source, "utm_medium": utm_medium, "utm_campaign": utm_campaign,
                    "status": "New",
                }
                append_row_csv(LEADS_FILE, row, columns=[
                    "timestamp","name","phone","email","preferred_locality","preferred_type","budget_lakhs",
                    "notes","utm_source","utm_medium","utm_campaign","status"
                ])
                st.session_state.leads.append(row)
                st.success("Lead submitted! Our team will reach out shortly.")

    if st.session_state.leads:
        df = pd.DataFrame(st.session_state.leads)
        st.dataframe(df, use_container_width=True)
        st.download_button("⬇️ Download leads (CSV)", df.to_csv(index=False),
                           file_name=f"leads_{datetime.now().strftime('%Y%m%d_%H%M')}.csv", mime="text/csv")
    else:
        st.info("No leads yet. Use the form above to capture inquiries.")

# -----------------------------
# Instagram (official embed via components.html)
# -----------------------------
if ENABLE_INSTAGRAM:
    st.divider()
    st.subheader(f"Instagram Feed — @{IG_HANDLE}")
    st.caption("Paste a public Instagram Reel URL to embed it below (demo).")
    insta_url = st.text_input("Instagram Reel URL", placeholder="https://www.instagram.com/reel/<id>/")
    if insta_url and insta_url.startswith("https://www.instagram.com/reel/"):
        embed_html = f"""
        <blockquote class="instagram-media" data-instgrm-permalink="{insta_url}" data-instgrm-version="14"
                    style="background:#FFF;border:0;margin:1px;max-width:540px;padding:0;width:100%;"></blockquote>
        https://www.instagram.com/embed.js</script>
        """
        st_html(embed_html, height=620)
    else:
        st.link_button("Open Instagram Profile", f"https://www.instagram.com/{IG_HANDLE}/")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption("Demo notes: Mocked data only; CSV persistence for leads & bookings; no backend.")
st.caption("Contact via WhatsApp India (+91 6309729493) or US (+1 786 420 9015).")

