# ============================================================
# MediSaver.py
# Top 5 Medicine Alternatives Finder
# Clean Streamlit Native UI
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
    margin-bottom: 10px;
}

.subtitle {
    font-size: 18px;
    color: #475569;
    margin-bottom: 30px;
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
    '<div class="subtitle">Find top medicine alternatives dynamically using Google Search + SerpAPI.</div>',
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

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# SERPAPI SEARCH
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

        "num": 5,

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
        # FETCH ONLY TOP 5 RESULTS
        # ====================================================

        if "organic_results" in data:

            for item in data["organic_results"][:5]:

                title = item.get(
                    "title",
                    "No Title"
                )

                snippet = item.get(
                    "snippet",
                    "No description available"
                )

                link = item.get(
                    "link",
                    "#"
                )

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
    placeholder="Example: Crocin, Calpol 650, Dolo 650"
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
            "Fetching Top 5 Medicine Alternatives..."
        ):

            results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        # ====================================================
        # RESULTS
        # ====================================================

        st.subheader(
            f"💊 Top 5 Alternatives for '{medicine_name}'"
        )

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
            # RESULTS LOOP
            # ====================================================

            for idx, result in enumerate(results, start=1):

                with st.container():

                    st.markdown(
                        f"## Alternative #{idx}"
                    )

                    # ========================================
                    # INFO
                    # ========================================

                    st.markdown("### Info")
                    st.write(result['title'])

                    # ========================================
                    # DETAILS
                    # ========================================

                    st.markdown("### Details")
                    st.write(result['snippet'])

                    # ========================================
                    # PURCHASE LINKS
                    # ========================================

                    st.markdown("### 🛒 Purchase Links")

                    links = generate_purchase_links(
                        medicine_name
                    )

                    cols = st.columns(3)

                    i = 0

                    for site, link in links.items():

                        with cols[i % 3]:

                            st.link_button(
                                f"Buy on {site}",
                                link
                            )

                        i += 1

                    st.divider()

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Top 5 Alternatives  
✅ Runtime SerpAPI Key  
✅ Dynamic Google Search  
✅ Medicine Substitute Search  
✅ Clean Streamlit UI  
✅ No Visible HTML Tags  
✅ Purchase Links  
✅ Responsive Layout  
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
