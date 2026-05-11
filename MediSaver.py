# app.py
# ============================================
# AI Medicine Alternative Finder
# Full Single File Project
# ============================================

# INSTALL:
# pip install streamlit requests pandas

# RUN:
# streamlit run app.py

import streamlit as st
import requests
import pandas as pd
from difflib import SequenceMatcher

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="AI Medicine Alternative Finder",
    page_icon="💊",
    layout="wide"
)

# ============================================
# CUSTOM CSS
# ============================================

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
    margin-bottom: 25px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 5px 15px rgba(0,0,0,0.08);
}

.price {
    color: green;
    font-size: 26px;
    font-weight: bold;
}

.site {
    background: #eff6ff;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
}

.buy-btn {
    text-decoration: none;
    background: #2563eb;
    color: white !important;
    padding: 10px 18px;
    border-radius: 10px;
    display: inline-block;
    margin-top: 8px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE
# ============================================

PRICE_DB = {
    "Crocin": 35,
    "Dolo 650": 28,
    "Paracetamol": 12,
    "Calpol": 30,
    "Azithromycin": 65,
    "Azee": 120,
    "Metformin": 22,
    "Glycomet": 110,
    "Atorvastatin": 40,
    "Lipitor": 250,
    "Cetirizine": 18,
    "Zyrtec": 120,
    "Amoxicillin": 55,
    "Augmentin": 210
}

# ============================================
# API
# ============================================

FDA_API = "https://api.fda.gov/drug/ndc.json"

# ============================================
# FUNCTIONS
# ============================================

def similarity(a, b):
    return SequenceMatcher(
        None,
        a.lower(),
        b.lower()
    ).ratio()

# --------------------------------------------

def fetch_medicine_data(medicine_name):

    try:

        url = f"{FDA_API}?search=brand_name:{medicine_name}&limit=1"

        response = requests.get(url)

        if response.status_code != 200:
            return None

        data = response.json()

        if "results" not in data:
            return None

        return data["results"][0]

    except:
        return None

# --------------------------------------------

def find_cheaper_alternatives(medicine_name):

    if medicine_name not in PRICE_DB:
        return []

    original_price = PRICE_DB[medicine_name]

    alternatives = []

    for med, price in PRICE_DB.items():

        if med.lower() == medicine_name.lower():
            continue

        score = similarity(medicine_name, med)

        if price < original_price:

            alternatives.append({
                "name": med,
                "price": price,
                "score": round(score, 2)
            })

    alternatives = sorted(
        alternatives,
        key=lambda x: (-x["score"], x["price"])
    )

    return alternatives[:5]

# --------------------------------------------

def generate_global_links(medicine):

    medicine_encoded = medicine.replace(" ", "%20")

    links = {

        # INDIA
        "1mg":
        f"https://www.1mg.com/search/all?name={medicine_encoded}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{medicine_encoded}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={medicine_encoded}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{medicine_encoded}",

        # GLOBAL
        "Amazon":
        f"https://www.amazon.in/s?k={medicine_encoded}+medicine",

        "Google Search":
        f"https://www.google.com/search?q=buy+{medicine_encoded}+medicine+online",

        "GoodRx":
        f"https://www.goodrx.com/search?q={medicine_encoded}",

        "Walgreens":
        f"https://www.walgreens.com/search/results.jsp?Ntt={medicine_encoded}",

        "CVS Pharmacy":
        f"https://www.cvs.com/search/?searchTerm={medicine_encoded}",

        "eBay":
        f"https://www.ebay.com/sch/i.html?_nkw={medicine_encoded}+medicine"
    }

    return links

# ============================================
# HEADER
# ============================================

st.markdown(
    '<div class="title">💊 AI Medicine Alternative Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find cheaper alternative medicines using AI logic and purchase them online globally.</div>',
    unsafe_allow_html=True
)

# ============================================
# SEARCH BOX
# ============================================

medicine_name = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Find Alternatives")

# ============================================
# MAIN LOGIC
# ============================================

if search_btn and medicine_name:

    st.subheader("📋 Medicine Information")

    medicine_data = fetch_medicine_data(medicine_name)

    if medicine_data:

        brand = medicine_data.get("brand_name", "N/A")
        generic = medicine_data.get("generic_name", "N/A")
        manufacturer = medicine_data.get("labeler_name", "N/A")

        info_df = pd.DataFrame({
            "Field": [
                "Brand Name",
                "Generic Name",
                "Manufacturer"
            ],
            "Value": [
                brand,
                generic,
                manufacturer
            ]
        })

        st.table(info_df)

    else:
        st.warning("Medicine information not found from FDA API.")

    # ============================================
    # FIND ALTERNATIVES
    # ============================================

    st.subheader("💰 Cheaper Alternatives")

    alternatives = find_cheaper_alternatives(medicine_name)

    if not alternatives:

        st.error("No cheaper alternatives found.")

    else:

        for alt in alternatives:

            st.markdown(f"""
            <div class="card">

                <h2>{alt['name']}</h2>

                <div class="price">
                    ₹{alt['price']}
                </div>

                <p>
                    <b>Similarity Score:</b>
                    {alt['score']}
                </p>

            </div>
            """, unsafe_allow_html=True)

            # ============================================
            # WEBSITE LINKS
            # ============================================

            st.markdown("### 🌐 Buy / Search Online")

            links = generate_global_links(alt["name"])

            for site, link in links.items():

                st.markdown(f"""
                <div class="site">

                    <h4>✅ {site}</h4>

                    <a class="buy-btn"
                       href="{link}"
                       target="_blank">

                       Buy / Search on {site}

                    </a>

                </div>
                """, unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================

st.sidebar.title("📌 About")

st.sidebar.info("""
This AI app helps users:

✅ Find cheaper medicine alternatives  
✅ Compare medicine prices  
✅ Search globally  
✅ Buy medicines online  
✅ Open pharmacy websites directly  
""")

# ============================================

st.sidebar.title("🌍 Supported Websites")

st.sidebar.write("""
🇮🇳 India:
- 1mg
- NetMeds
- PharmEasy
- Apollo Pharmacy

🌎 Global:
- Amazon
- GoodRx
- Walgreens
- CVS Pharmacy
- eBay
- Google Search
""")

# ============================================

st.sidebar.title("🛠 Tech Stack")

st.sidebar.write("""
- Python
- Streamlit
- Requests
- Pandas
- AI Similarity Matching
- FDA API
""")

# ============================================
# FOOTER
# ============================================

st.markdown("""
<div class="footer">
Made with ❤️ using Python + Streamlit
</div>
""", unsafe_allow_html=True)
