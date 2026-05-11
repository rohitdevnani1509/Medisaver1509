# MediSaver.py (Improved Version)

```python
# ============================================================
# MediSaver.py
# Improved Medicine Alternative Finder
# Clean Streamlit UI + Proper HTML Rendering
# ============================================================

# INSTALL:
# pip install -r requirements.txt

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
from urllib.parse import quote_plus

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MediSaver",
    page_icon="💊",
    layout="wide"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f4f7fb;
}

.title {
    font-size: 52px;
    font-weight: bold;
    color: #0f172a;
}

.subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 24px;
    border-radius: 18px;
    margin-bottom: 22px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

.buy-btn {
    text-decoration: none;
    background: #2563eb;
    color: white !important;
    padding: 10px 18px;
    border-radius: 10px;
    display: inline-block;
    margin-top: 10px;
    margin-right: 10px;
    font-weight: 500;
}

.alt-caption {
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 10px;
}

.alt-text {
    font-size: 16px;
    color: #475569;
    line-height: 1.7;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: gray;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💊 MediSaver</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find alternate medicines dynamically using SerpAPI.</div>',
    unsafe_allow_html=True
)

# ============================================================
# DISCLAIMER
# ============================================================

st.warning(
    "⚠️ This app does NOT provide medical advice. Always consult a doctor or pharmacist before using substitute medicines."
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔑 SerpAPI Configuration")

SERP_API_KEY = st.sidebar.text_input(
    "Enter SerpAPI Key",
    type="password"
)

st.sidebar.markdown("""
Get free API key from:

https://serpapi.com/users/sign_up
""")

# ============================================================
# PURCHASE LINKS
# ============================================================


def generate_purchase_links(medicine):

    med = quote_plus(medicine)

    return {

        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Truemeds":
        f"https://www.truemeds.in/search/{med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# SERPAPI SEARCH
# ============================================================


@st.cache_data(ttl=3600)
def search_alternatives(medicine_name, api_key):

    url = "https://serpapi.com/search.json"

    query = f"{medicine_name} alternative generic substitute"

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 10,

        "google_domain": "google.com",

        "hl": "en",

        "gl": "us"
    }

    alternatives = []

    try:

        response = requests.get(
            url,
            params=params,
            timeout=15
        )

        response.raise_for_status()

        try:
            data = response.json()
        except:
            st.error("Invalid API response")
            return []

        if "error" in data:

            st.error(f"SerpAPI Error: {data['error']}")

            return []

        if "organic_results" in data:

            for item in data["organic_results"]:

                title = item.get("title", "No Title")

                snippet = item.get(
                    "snippet",
                    "No description available"
                )

                link = item.get("link", "#")

                alternatives.append({

                    "title": title,

                    "snippet": snippet,

                    "link": link
                })

        return alternatives

    except requests.exceptions.RequestException as e:

        st.error(f"Search Error: {e}")

        return []

# ============================================================
# USER INPUT FORM
# ============================================================

with st.form("medicine_form"):

    medicine_name = st.text_input(
        "Enter Medicine Name",
        placeholder="Example: Calpol 650"
    )

    search_btn = st.form_submit_button("🔍 Find Alternatives")

# ============================================================
# MAIN LOGIC
# ============================================================

if search_btn:

    if not SERP_API_KEY:

        st.error("Please enter SerpAPI Key.")

    elif not medicine_name:

        st.error("Please enter medicine name.")

    else:

        with st.spinner(
            "Searching for alternate medicines..."
        ):

            results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        st.subheader("💊 Alternative Medicines")

        if not results:

            st.warning(
                "No alternate medicines found."
            )

        else:

            for result in results:

                st.markdown(f"""
                <div class="card">

                    <div class="alt-caption">
                        💊 Alternatives
                    </div>

                    <h3>
                        {result['title']}
                    </h3>

                    <p class="alt-text">
                        {result['snippet']}
                    </p>

                </div>
                """, unsafe_allow_html=True)

                st.link_button(
                    "🔍 Open Google Result",
                    result['link']
                )

                st.markdown("<br>", unsafe_allow_html=True)

            # ====================================================
            # PURCHASE LINKS
            # ====================================================

            st.subheader("🛒 Purchase Links")

            links = generate_purchase_links(
                medicine_name
            )

            cols = st.columns(3)

            idx = 0

            for site, link in links.items():

                with cols[idx % 3]:

                    st.link_button(
                        f"Buy on {site}",
                        link
                    )

                idx += 1

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Proper Streamlit UI Rendering
✅ No Raw HTML Tags
✅ Runtime SerpAPI Key
✅ Dynamic Google Search
✅ Purchase Links
✅ Cached API Calls
✅ Better Error Handling
✅ Clean Alternative Cards
✅ Responsive UI

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)

```
