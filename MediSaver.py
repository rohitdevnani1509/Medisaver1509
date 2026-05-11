# ============================================================
# app.py
# AI Medicine Alternative Finder + Google Product Search
# ============================================================

# INSTALL:
# pip install streamlit requests pandas

# RUN:
# streamlit run app.py

# ============================================================

import streamlit as st
import requests
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
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}

.price {
    color: green;
    font-size: 28px;
    font-weight: bold;
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

.site-box {
    background: #eff6ff;
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 12px;
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
# MEDICINE DATABASE
# SAME SALT / GENERIC LOGIC
# ============================================================

MEDICINE_DB = {

    "Crocin": {
        "salt": "Paracetamol",
        "price": 35,
        "alternatives": [
            "Dolo 650",
            "Paracetamol",
            "Calpol"
        ]
    },

    "Dolo 650": {
        "salt": "Paracetamol",
        "price": 28,
        "alternatives": [
            "Crocin",
            "Paracetamol",
            "Calpol"
        ]
    },

    "Calpol": {
        "salt": "Paracetamol",
        "price": 30,
        "alternatives": [
            "Crocin",
            "Dolo 650",
            "Paracetamol"
        ]
    },

    "Paracetamol": {
        "salt": "Paracetamol",
        "price": 12,
        "alternatives": [
            "Crocin",
            "Dolo 650",
            "Calpol"
        ]
    },

    "Azithromycin": {
        "salt": "Azithromycin",
        "price": 65,
        "alternatives": [
            "Azee"
        ]
    },

    "Azee": {
        "salt": "Azithromycin",
        "price": 120,
        "alternatives": [
            "Azithromycin"
        ]
    }
}

# ============================================================
# FDA API
# ============================================================

FDA_API = "https://api.fda.gov/drug/ndc.json"

# ============================================================
# FUNCTIONS
# ============================================================

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

# ------------------------------------------------------------

def find_alternatives(medicine_name):

    if medicine_name not in MEDICINE_DB:
        return []

    alternatives = []

    medicine_data = MEDICINE_DB[medicine_name]

    original_price = medicine_data["price"]

    for alt in medicine_data["alternatives"]:

        if alt in MEDICINE_DB:

            alt_data = MEDICINE_DB[alt]

            cheaper = alt_data["price"] < original_price

            alternatives.append({
                "name": alt,
                "salt": alt_data["salt"],
                "price": alt_data["price"],
                "cheaper": cheaper
            })

    return sorted(
        alternatives,
        key=lambda x: x["price"]
    )

# ------------------------------------------------------------

def generate_links(medicine):

    med = medicine.replace(" ", "+")

    return {

        # =====================================================
        # GOOGLE LINKS
        # =====================================================

        "Google Search":
        f"https://www.google.com/search?q={med}+medicine",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}+medicine",

        # =====================================================
        # INDIA PHARMACY LINKS
        # =====================================================

        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        # =====================================================
        # GLOBAL LINKS
        # =====================================================

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
# HEADER
# ============================================================

st.markdown(
    '<div class="title">💊 AI Medicine Alternative Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find cheaper alternatives of the same medicine and purchase online globally.</div>',
    unsafe_allow_html=True
)

# ============================================================
# SEARCH BOX
# ============================================================

medicine_name = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Find Alternatives")

# ============================================================
# MAIN LOGIC
# ============================================================

if search_btn and medicine_name:

    st.subheader("📋 Medicine Information")

    # ========================================================
    # FDA API DATA
    # ========================================================

    medicine_data = fetch_medicine_data(medicine_name)

    if medicine_data:

        brand = medicine_data.get("brand_name", "N/A")
        generic = medicine_data.get("generic_name", "N/A")
        manufacturer = medicine_data.get("labeler_name", "N/A")

        df = pd.DataFrame({

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

        st.table(df)

    else:
        st.warning("Medicine information not found from FDA API.")

    # ========================================================
    # ALTERNATIVES
    # ========================================================

    st.subheader("💰 Alternative Medicines")

    alternatives = find_alternatives(medicine_name)

    if not alternatives:

        st.error("No alternatives found.")

    else:

        for alt in alternatives:

            cheaper_text = (
                "✅ Cheaper Alternative"
                if alt["cheaper"]
                else "⚠ Similar Price"
            )

            st.markdown(f"""
            <div class="card">

                <h2>{alt['name']}</h2>

                <div class="price">
                    ₹{alt['price']}
                </div>

                <p>
                    <b>Salt Composition:</b>
                    {alt['salt']}
                </p>

                <p>
                    <b>Status:</b>
                    {cheaper_text}
                </p>

            </div>
            """, unsafe_allow_html=True)

            # =================================================
            # PURCHASE LINKS
            # =================================================

            st.markdown("### 🌐 Buy / Search Online")

            links = generate_links(alt["name"])

            for site, link in links.items():

                st.markdown(f"""
                <div class="site-box">

                    <h4>✅ {site}</h4>

                    <a class="buy-btn"
                       href="{link}"
                       target="_blank">

                       🛒 Open {site}

                    </a>

                </div>
                """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Same Salt Alternatives  
✅ Cheaper Medicine Detection  
✅ Google Search Integration  
✅ Google Shopping Links  
✅ Online Pharmacy Redirects  
✅ Global Product Search  
✅ FDA API Integration  

""")

# ============================================================

st.sidebar.title("🌍 Supported Websites")

st.sidebar.write("""

🇮🇳 India:
- 1mg
- NetMeds
- PharmEasy
- Apollo Pharmacy

🌎 Global:
- Google Search
- Google Shopping
- Amazon
- GoodRx
- Walgreens
- CVS Pharmacy

""")

# ============================================================

st.sidebar.title("🛠 Tech Stack")

st.sidebar.write("""

- Python
- Streamlit
- Requests
- Pandas
- FDA API

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit

</div>
""", unsafe_allow_html=True)
