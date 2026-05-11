# ============================================================
# MediSaver.py
# Dynamic Medicine Alternative Finder
# Google Search Results + Purchase Links
# Runtime SerpAPI Key Input
# ============================================================

# INSTALL:
# pip install streamlit requests

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
    font-size: 48px;
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
    '<div class="subtitle">Find alternate medicines dynamically from Google Search using SerpAPI.</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔑 SerpAPI Key")

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

        "Apollo":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# GOOGLE SEARCH FUNCTION
# ============================================================

def search_alternatives(
    medicine_name,
    api_key
):

    url = "https://serpapi.com/search.json"

    query = f"{medicine_name} generic substitute medicine"

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
            params=params
        )

        data = response.json()

        # ====================================================
        # ORGANIC GOOGLE RESULTS
        # ====================================================

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

    except Exception as e:

        st.error(f"Search Error: {e}")

        return []

# ============================================================
# USER INPUT
# ============================================================

medicine_name = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Find Alternatives")

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
            "Searching Google for alternative medicines..."
        ):

            results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        st.subheader("💊 Google Search Results")

        if not results:

            st.warning(
                "No alternate medicines found."
            )

        else:

            for result in results:

                st.markdown(f"""
                <div class="card">

                    <h2>{result['title']}</h2>

                    <p>{result['snippet']}</p>

                    <a class="buy-btn"
                       href="{result['link']}"
                       target="_blank">

                       🔍 Open Google Result

                    </a>

                </div>
                """, unsafe_allow_html=True)

                # =============================================
                # PURCHASE LINKS
                # =============================================

                st.markdown("### 🛒 Purchase Links")

                links = generate_purchase_links(
                    medicine_name
                )

                for site, link in links.items():

                    st.markdown(f"""
                    <a class="buy-btn"
                       href="{link}"
                       target="_blank">

                       Buy on {site}

                    </a>
                    """, unsafe_allow_html=True)

                st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Runtime SerpAPI Key  
✅ Dynamic Google Search  
✅ Live Google Results  
✅ Medicine Alternative Search  
✅ 1mg Links  
✅ PharmEasy Links  
✅ Truemeds Links  
✅ Streamlit Frontend UI  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
