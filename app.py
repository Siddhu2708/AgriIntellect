import streamlit as st
from streamlit_option_menu import option_menu
import json
import streamlit.components.v1 as components
import urllib.request
from home import home_default
from soil import soil_home
from disease import disease_home
from residue import residue_home
from planty import Planty
from shop import Shop
from sarvamai import SarvamAI
from contact import Contact
from market import market_home
from utils import load_config, translate_text, LANGUAGES_MAP

# Load configuration for API keys
config = load_config()

SARVAM_API_KEY = config.get("SARVAM_API_KEY")
sarvam_client = SarvamAI(api_subscription_key=SARVAM_API_KEY)
languages = LANGUAGES_MAP
# --- GPS & Reverse Geocoding Logic ---
if "lat" in st.query_params and "lon" in st.query_params:
    try:
        lat = st.query_params["lat"]
        lon = st.query_params["lon"]
        # Use a more robust User-Agent (Chrome-like)
        geo_url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=10"
        geo_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        geo_req = urllib.request.Request(geo_url, headers=geo_headers)
        with urllib.request.urlopen(geo_req) as geo_res:
            geo_data = json.loads(geo_res.read().decode())
            address = geo_data.get("address", {})
            city = address.get("city") or address.get("town") or address.get("village") or address.get("suburb", "")
            region = address.get("state", "")
            if city:
                st.session_state.user_location = f"{city}, {region}"
                # Provide feedback in sidebar about GPS success
                st.session_state["gps_success"] = True
    except Exception as e:
        st.session_state["gps_error"] = str(e)
# --------------------------------------

st.set_page_config(
    page_title="AgrIntellect",
    page_icon="🌱",
    layout="wide"
)

with st.sidebar:
    st.title("⚙️ Settings")

    language = st.selectbox(
        "🌍 Select Language",
        list(languages.keys())
    )

    st.markdown("---")
    st.markdown("📍 **Location Settings**")
    
    if "user_location" not in st.session_state:
        st.session_state.user_location = ""
        
    def get_auto_location():
        # Try ip-api.com first (often more accurate city/region detection)
        try:
            with urllib.request.urlopen("http://ip-api.com/json/") as url:
                data = json.loads(url.read().decode())
                if data.get("status") == "success":
                    city = data.get("city", "")
                    region = data.get("regionName", "")
                    return f"{city}, {region}" if city and region else city
        except:
            pass

        # Fallback to ipapi.co
        try:
            with urllib.request.urlopen("https://ipapi.co/json/") as url:
                data = json.loads(url.read().decode())
                city = data.get("city", "")
                region = data.get("region", "")
                return f"{city}, {region}" if city and region else city
        except:
            return ""

    loc_col1, loc_col2, loc_col3 = st.columns([3, 1, 1])
    with loc_col1:
        user_loc = st.text_input("City / District", value=st.session_state.user_location, placeholder="e.g. Pune, Maharashtra")
        st.session_state.user_location = user_loc
    with loc_col2:
        if st.button("📍", help="Auto-detect Location (IP-based)"):
            detected = get_auto_location()
            if detected:
                st.session_state.user_location = detected
                st.rerun()
    with loc_col3:
        if st.button("🛰️", help="Precise Location (GPS)"):
            components.html("""
                <script>
                navigator.geolocation.getCurrentPosition(function(position) {
                    const url = new URL(window.parent.location.href);
                    url.searchParams.set("lat", position.coords.latitude);
                    url.searchParams.set("lon", position.coords.longitude);
                    window.parent.location.href = url.href;
                }, function(error) {
                    window.parent.alert("GPS Access Denied or Failed. Please check browser permissions.");
                });
                </script>
            """, height=0)

    # Show GPS Status Feedback
    if st.session_state.get("gps_success"):
        st.success("✅ GPS Location Resolved")
        del st.session_state["gps_success"]
    elif st.session_state.get("gps_error"):
        st.error(f"❌ GPS Error: {st.session_state['gps_error']}")
        del st.session_state["gps_error"]

    st.markdown("---")

    module_options = ["Hub", "Soil", "Disease", "Residue"]
    
    try:
        with open("nav_translations.json", encoding="utf-8") as f:
            nav_trans = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        nav_trans = {}

    module_translated = [nav_trans.get(opt, {}).get(language, opt) for opt in module_options]

    module_local = option_menu(
        menu_title=nav_trans.get("Modules", {}).get(language, "Modules"),
        options=module_translated,
        icons=["house", "droplet", "bug", "recycle"],
        default_index=0,
        styles={
            "nav-link-selected": {"background-color": "#66bb6a"},
        }
    )
    try:
        idx = module_translated.index(module_local)
        module_selection = module_options[idx]
    except (ValueError, IndexError):
        module_selection = module_options[0]

# Resolve redirect from shop buttons (separate key to avoid type conflict)
_nav_idx = st.session_state.pop("nav_idx", 0)

select_options = ['Home', 'Planty AI', 'Market', 'Shop', 'Contact']
select_translated = [nav_trans.get(opt, {}).get(language, opt) for opt in select_options]

select_local = option_menu(
    menu_title='',
    options=select_translated,
    icons=['house', 'robot', 'cart', 'shop', 'envelope'],
    orientation='horizontal',
    default_index=_nav_idx,
    key=f"main_nav_{_nav_idx}", # Dynamic key to force re-render on redirect
    styles={
        "nav-link-selected": {"background-color": "#66bb6a"},
    }
)

try:
    sel_idx = select_translated.index(select_local)
    select_selection = select_options[sel_idx]
except (ValueError, IndexError):
    select_selection = select_options[0]

if select_selection == "Home":

    if module_selection == "Hub":
        home_default(sarvam_client, language)

    elif module_selection == "Soil":
        soil_home(sarvam_client, language)

    elif module_selection == "Disease":
        disease_home(sarvam_client, language)

    elif module_selection == "Residue":
        residue_home(sarvam_client, language)

elif select_selection == "Planty AI":
    Planty(sarvam_client, language)

elif select_selection == "Market":
    market_home(sarvam_client, language)

elif select_selection == "Shop":
    Shop(sarvam_client, language)

elif select_selection == "Contact":
    Contact(sarvam_client, language)