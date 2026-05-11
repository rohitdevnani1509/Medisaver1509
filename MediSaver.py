# app.py
# AI Medicine Alternative Finder with Frontend UI + Pharmacy Availability

# Run:
# pip install streamlit requests pandas
# streamlit run app.py

import streamlit as st
import requests
import pandas as pd
from difflib import SequenceMatcher

# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(
    page_title="AI Medicine Alternative Finder",
    page_icon="💊",
    layout="wide"
)

# --------------------------------
# CUSTOM CSS
# --------------------------------

st.markdown("""
<style>

.main {
    background-color: #f4f7fb;
}

.title {
    font-size: 45px;
    font-weight: bold;
    color: #0f172a;
}

.subtitle {
    color: #475569;
    font-size: 18px;
    margin-bottom: 20px;
}

.card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.price {
    color: green;
    font-size: 24px;
    font-weight: bold;
}

.site {
    background: #eff6ff;
    padding: 10px;
    border-radius: 10px;
    margin-top: 10px;
}

.buy-btn {
    text-decoration: none;
    background: #2563eb;
    color: white !important;
    padding: 10px 18px;
    border-radius: 10px;
    margin-right: 10px;
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------------
# DATABASE
# --------------------------------

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
    "Lipitor": 250
}

# Pharmacy availability database

MEDICINE_AVAILABILITY = {
    "Dolo 650": ["1mg", "NetMeds", "PharmEasy"],
    "Paracetamol": ["1mg", "Apollo Pharmacy", "NetMeds"],
    "Calpol": ["1mg", "PharmEasy"],
    "Azithromycin": ["NetMeds", "Apollo Pharmacy"],
    "Metformin": ["1mg", "NetMeds"],
    "Atorvastatin": ["PharmEasy", "Apollo Pharmacy"]
}

FDA_API = "https://api.fda.gov/drug/ndc.json"

PHARMACY_LINKS = {
    "1mg": "https://www.1mg.com/search/all?name={}",
    "NetMeds": "https://www.netmeds.com/catalogsearch/result/{}",
    "PharmEasy": "https://pharmeasy.in/search/all?name={}",
    "Apollo Pharmacy": "https://www.apollopharmacy.in/search-medicines/{}"
}

# --------------------------------
# FUNCTIONS
# --------------------------------

def similarity(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

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

def generate_pharmacy_links(medicine):

    available_sites = MEDICINE_AVAILABILITY.get(medicine, [])

    links = {}

    for site in available_sites:

        if site in PHARMACY_LINKS:

            links[site] = PHARMACY_LINKS[site].format(
                medicine.replace(" ", "%20")
            )

    return links

# --------------------------------
# HEADER
# --------------------------------

st.markdown(
    '<div class="title">💊 AI Medicine Alternative Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find cheaper medicine alternatives and check where they are available online.</div>',
    unsafe_allow_html=True
)

# --------------------------------
# SEARCH INPUT
# --------------------------------

medicine_name = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Search Alternatives")

# --------------------------------
# MAIN SEARCH
# --------------------------------

if search_btn and medicine_name:

    st.subheader("📋 Medicine Information")

    medicine_data = fetch_medicine_data(medicine_name)

    if medicine_data:

        brand = medicine_data.get("brand_name", "N/A")
        generic = medicine_data.get("generic_name", "N/A")
        manufacturer = medicine_data.get("labeler_name", "N/A")

        df = pd.DataFrame({
            "Field": ["Brand", "Generic", "Manufacturer"],
            "Value": [brand, generic, manufacturer]
        })

        st.table(df)

    else:
        st.warning("No medicine data found from FDA API.")

    # --------------------------------
    # ALTERNATIVES
    # --------------------------------

    st.subheader("💰 Cheaper Alternatives")

    alternatives = find_cheaper_alternatives(medicine_name)

    if not alternatives:
        st.error("No cheaper alternatives found.")

    else:

        for alt in alternatives:

            st.markdown(f"""
            <div class="card">
                <h2>{alt['name']}</h2>
                <div class="price">₹{alt['price']}</div>
                <p><b>Similarity Score:</b> {alt['score']}</p>
            """, unsafe_allow_html=True)

            # AVAILABLE WEBSITES

            st.markdown("### 🌐 Available On")

            links = generate_pharmacy_links(alt["name"])

            if links:

                for site, link in links.items():

                    st.markdown(f"""
                    <div class="site">
                        ✅ {site}
                    </div>

                    <br>

                    <a class="buy-btn" href="{link}" target="_blank">
                    Buy from {site}
                    </a>

                    <br><br>
                    """, unsafe_allow_html=True)

            else:
                st.warning("Availability websites not found.")

            st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------
# SIDEBAR
# --------------------------------

st.sidebar.title("📌 About App")

st.sidebar.info("""
This application helps users:

✅ Find cheaper medicines  
✅ Compare medicine prices  
✅ Check medicine availability  
✅ Open pharmacy websites directly  
""")

st.sidebar.title("🏥 Supported Websites")

st.sidebar.write("""
- 1mg
- NetMeds
- PharmEasy
- Apollo Pharmacy
""")

# --------------------------------
# FOOTER
# --------------------------------

st.markdown("""
<div class="footer">
Made with ❤️ using Python + Streamlit
</div>
""", unsafe_allow_html=True)
