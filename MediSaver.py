# ============================================================
# MediSaver.py
# Clean Streamlit Native UI Version
# No Visible HTML Tags
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
    page_title="MediSaver AI",
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

.debug-box {
    background: #fff3cd;
    padding: 15px;
    border-radius: 12px;
    margin-top: 20px;
    color: #856404;
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
    '<div class="title">💊 MediSaver AI (Affordable Alternates)</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find alternate medicines dynamically from Google Search using SerpAPI.</div>',
    unsafe_allow_html=True
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
# SERPAPI GOOGLE SEARCH
# ============================================================

def search_alternatives(
    medicine_name,
    api_key
):

    url = "https://serpapi.com/search.json"

    query = f"""
    {medicine_name} generic alternative
    same salt composition
    lower price
    """

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 10,

        "google_domain": "google.com",

        "hl": "en",

        "gl": "in"
    }

    alternatives = []

    try:

        response = requests.get(
            url,
            params=params
        )

        st.write("HTTP Status:", response.status_code)

        data = response.json()

        # ====================================================
        # DEBUG RESPONSE
        # ====================================================

        with st.expander("🔍 Debug API Response"):

            st.json(data)

        # ====================================================
        # HANDLE API ERRORS
        # ====================================================

        if "error" in data:

            st.error(f"SerpAPI Error: {data['error']}")

            return []

        # ====================================================
        # ORGANIC RESULTS
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
    placeholder="Example: Calpol 650"
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
            "Searching Google for alternate medicines..."
        ):

            results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        # ====================================================
        # RESULTS
        # ====================================================

        st.subheader("💊 AI Engine Search Results")

        if not results:

            st.warning(
                "No alternate medicines found."
            )

            st.markdown("""
            <div class="debug-box">

            Possible reasons:

            • Invalid SerpAPI key  
            • Free plan exhausted  
            • Google returned no organic results  
            • Query returned limited data  

            Try another medicine name.

            </div>
            """, unsafe_allow_html=True)

        else:

            # ====================================================
            # PURCHASE LINKS
            # ====================================================

            st.subheader("🛒 Purchase Links")

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

            st.markdown("---")

            # ====================================================
            # RESULTS LOOP
            # ====================================================

            for result in results:

                with st.container():

                    st.markdown("### Info")
                    st.write(result['title'])

                    st.markdown("### Details")
                    st.write(result['snippet'])

                    if result['link'] != "#":

                        st.link_button(
                            "🔍 Open Source",
                            result['link']
                        )

                    st.divider()

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Runtime SerpAPI Key  
✅ Dynamic Google Search  
✅ Live Google Results  
✅ Generic Alternative Search  
✅ Clean Streamlit Native UI  
✅ No Visible HTML Tags  
✅ Purchase Links  
✅ API Debug Response  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using AI + Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
