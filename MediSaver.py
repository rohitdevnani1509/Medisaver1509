# ============================================================
# MediSaver.py
# Working AI Medicine Alternative Finder
# Dynamic Google Search + Runtime SerpAPI Key
# Shows Alternate Medicines + Purchase Links
# ============================================================

# INSTALL:
# pip install streamlit requests pandas

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
import pandas as pd

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
    font-size: 50px;
    font-weight: bold;
    color: #0f172a;
}

.subtitle {
    color: #475569;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
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
    '<div class="title">💊 MediSaver</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find alternative medicines dynamically from Google Search using SerpAPI.</div>',
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
# GOOGLE SEARCH FUNCTION
# ============================================================

def search_alternative_medicines(medicine_name, api_key):

    url = "https://serpapi.com/search.json"

    # Better query for substitutes
    query = f"{medicine_name} generic substitute medicine"

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 20
    }

    try:

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        medicines = []

        # ====================================================
        # ORGANIC RESULTS
        # ====================================================

        if "organic_results" in data:

            for item in data["organic_results"]:

                title = item.get("title", "")

                snippet = item.get("snippet", "")

                link = item.get("link", "#")

                if len(title) < 3:
                    continue

                medicines.append({

                    "name": title,

                    "description": snippet,

                    "link": link
                })

        # ====================================================
        # RELATED QUESTIONS
        # ====================================================

        if "related_questions" in data:

            for item in data["related_questions"]:

                question = item.get("question", "")

                snippet = item.get("snippet", "")

                link = item.get("link", "#")

                medicines.append({

                    "name": question,

                    "description": snippet,

                    "link": link
                })

        return medicines

    except Exception as e:

        st.error(f"Search Error: {e}")

        return []

# ============================================================
# PURCHASE LINKS
# ============================================================

def generate_purchase_links(medicine):

    med = medicine.replace(" ", "+")

    return {

        # GOOGLE
        "Google Search":
        f"https://www.google.com/search?q={med}+medicine",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}+medicine",

        # INDIA PHARMACY LINKS
        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        # GLOBAL LINKS
        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine",

        "GoodRx":
        f"https://www.goodrx.com/search?q={med}",

        "Walgreens":
        f"https://www.walgreens.com/search/results.jsp?Ntt={med}",

        "CVS Pharmacy":
        f"https://www.cvs.com/search/?searchTerm={med}"
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

    if not SERP_API_KEY:

        st.error("Please enter your SerpAPI Key.")

    elif not medicine_name:

        st.error("Please enter medicine name.")

    else:

        with st.spinner(
            "Searching Google for alternative medicines..."
        ):

            alternatives = search_alternative_medicines(
                medicine_name,
                SERP_API_KEY
            )

        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        st.subheader("💊 Alternative Medicines")

        if not alternatives:

            st.warning("No alternatives found.")

        else:

            for medicine in alternatives:

                st.markdown(f"""
                <div class="card">

                    <h2>{medicine['name']}</h2>

                    <p>{medicine['description']}</p>

                    <a class="buy-btn"
                       href="{medicine['link']}"
                       target="_blank">

                       🔍 Open Source

                    </a>

                </div>
                """, unsafe_allow_html=True)

                # ============================================
                # PURCHASE LINKS
                # ============================================

                st.markdown("### 🛒 Buy Online")

                purchase_links = generate_purchase_links(
                    medicine_name
                )

                for site, link in purchase_links.items():

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

✅ Runtime SerpAPI Key Input  
✅ Dynamic Google Search  
✅ Alternate Medicine Detection  
✅ Google Shopping Integration  
✅ Purchase Links  
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
- GoodRx
- Walgreens
- CVS Pharmacy

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
