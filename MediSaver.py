# ============================================================
# MediSaver.py
# AI Medicine Best Price Finder
# Clean Production UI Version
# ============================================================

# INSTALL:
# pip install streamlit requests

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
import re
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

.result-card {
    background: white;
    padding: 25px;
    border-radius: 16px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.08);
}

.price-box {
    background: #dcfce7;
    color: #166534;
    padding: 12px;
    border-radius: 10px;
    font-size: 20px;
    font-weight: bold;
    margin-top: 10px;
    margin-bottom: 20px;
}

.footer {
    text-align: center;
    margin-top: 50px;
    color: gray;
    padding: 20px;
}

.consult-btn {
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.consult-btn a {
    text-decoration: none;
    width: 100%;
}

.consult-btn button {
    background-color: #2563eb;
    color: white;
    border: none;
    padding: 12px 18px;
    border-radius: 10px;
    font-size: 16px;
    font-weight: bold;
    cursor: pointer;
    width: 100%;
    transition: 0.3s;
}

.consult-btn button:hover {
    background-color: #1d4ed8;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER WITH CONSULT DOCTOR BUTTON
# ============================================================

col1, col2 = st.columns([6, 1.5])

with col1:

    st.markdown(
        '<div class="title">💊 MediSaver AI (Affordable Alternates)</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Find cheapest medicine prices dynamically using Google Search + SerpAPI.</div>',
        unsafe_allow_html=True
    )

with col2:

    st.markdown("""
    <div class="consult-btn" style="margin-top:25px;">
        <a href="https://www.practo.com/" target="_blank">
            <button>
                👨‍⚕️ Consult Doctor
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

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

        "Apollo":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# PRICE EXTRACTION
# ============================================================

def extract_price(text):

    prices = re.findall(r'₹\s?\d+|\$\s?\d+', text)

    if prices:

        return prices[0]

    return "Price Not Found"

# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_alternatives(
    medicine_name,
    api_key
):

    url = "https://serpapi.com/search.json"

    query = f"""
    cheapest {medicine_name}
    generic alternative
    medicine price
    buy online
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
        # HANDLE API ERRORS
        # ====================================================

        if "error" in data:

            st.error(f"SerpAPI Error: {data['error']}")

            return []

        # ====================================================
        # FETCH TOP 5 RESULTS
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

                price = extract_price(snippet)

                alternatives.append({

                    "title": title,

                    "snippet": snippet,

                    "price": price
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

search_btn = st.button("💰 Find Best Price")

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
            "Finding cheapest medicine prices..."
        ):

            results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        # ====================================================
        # RESULTS
        # ====================================================

        st.subheader(
            f"💊 Top 5 Best Price Results for '{medicine_name}'"
        )

        if not results:

            st.warning(
                "No medicine pricing results found."
            )

        else:

            for idx, result in enumerate(results, start=1):

                st.markdown(
                    '<div class="result-card">',
                    unsafe_allow_html=True
                )

                # ============================================
                # DYNAMIC TITLE
                # ============================================

                if idx == 1:

                    st.markdown(
                        "## 🤖 AI Info for Input Medicine"
                    )

                else:

                    st.markdown(
                        f"## 💊 Alternative #{idx}"
                    )

                # ============================================
                # MEDICINE INFO
                # ============================================

                st.markdown("### 💊 Medicine")
                st.write(result['title'])

                # ============================================
                # DETAILS
                # ============================================

                st.markdown("### 📄 Details")
                st.write(result['snippet'])

                # ============================================
                # PRICE
                # ============================================

                st.markdown("### 💰 Best Price")

                st.markdown(
                    f"""
                    <div class="price-box">
                        {result['price']}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # ============================================
                # PURCHASE LINKS
                # ============================================

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

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

                st.divider()

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Top 5 Cheapest Results  
✅ Runtime SerpAPI Key  
✅ Dynamic Google Search  
✅ AI Info for Input Medicine  
✅ Medicine Price Extraction  
✅ Purchase Links  
✅ Consult Doctor Button  
✅ Clean Streamlit UI  
✅ Responsive Layout  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using AI + Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
