# ============================================================
# app.py
# AI Medicine Alternative Finder using SerpAPI
# Runtime Google Search + Frontend UI
# ============================================================

# INSTALL:
# pip install streamlit google-search-results requests pandas

# RUN:
# streamlit run app.py

# ============================================================

import streamlit as st
from serpapi.google_search import GoogleSearch
import pandas as pd

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Medicine Alternative Finder",
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
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
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
    '<div class="title">💊 AI Medicine Alternative Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find medicine alternatives dynamically from Google Search using SerpAPI.</div>',
    unsafe_allow_html=True
)

# ============================================================
# SERP API KEY INPUT
# ============================================================

st.sidebar.title("🔑 SerpAPI Configuration")

serp_api_key = st.sidebar.text_input(
    "Enter SerpAPI Key",
    type="password"
)

st.sidebar.markdown("""
Get free API key from:

https://serpapi.com/users/sign_up
""")

# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_alternative_medicines(medicine, api_key):

    query = f"{medicine} alternative medicine generic substitute"

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 10
    }

    search = GoogleSearch(params)

    results = search.get_dict()

    alternatives = []

    if "organic_results" in results:

        for item in results["organic_results"]:

            title = item.get("title", "No Title")

            snippet = item.get("snippet", "No Description")

            link = item.get("link", "#")

            alternatives.append({

                "title": title,

                "snippet": snippet,

                "link": link
            })

    return alternatives

# ============================================================
# PRODUCT LINKS
# ============================================================

def generate_product_links(medicine):

    med = medicine.replace(" ", "+")

    return {

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}+medicine",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine",

        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}"
    }

# ============================================================
# SEARCH INPUT
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

    if not serp_api_key:

        st.error("Please enter your SerpAPI Key.")

    elif not medicine_name:

        st.error("Please enter medicine name.")

    else:

        with st.spinner("Searching Google for alternative medicines..."):

            results = search_alternative_medicines(
                medicine_name,
                serp_api_key
            )

        # ====================================================
        # SHOW RESULTS
        # ====================================================

        st.subheader("💊 Alternative Medicines Found")

        if not results:

            st.warning("No alternatives found.")

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

                # ==============================================
                # PURCHASE LINKS
                # ==============================================

                st.markdown("### 🛒 Purchase Links")

                links = generate_product_links(
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

                st.markdown("<br><hr>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Runtime Google Search  
✅ SerpAPI Integration  
✅ Dynamic Medicine Alternatives  
✅ Google Shopping Links  
✅ Purchase Redirect Buttons  
✅ Streamlit Frontend UI  

""")

# ============================================================

st.sidebar.title("🌍 Supported Websites")

st.sidebar.write("""

- Google Search
- Google Shopping
- Amazon
- 1mg
- NetMeds
- PharmEasy
- Apollo Pharmacy

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
