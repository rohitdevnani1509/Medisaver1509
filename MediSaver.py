# app.py
# AI Medicine Alternative Finder with Frontend UI
# Run using:
# pip install streamlit requests pandas
# streamlit run app.py

import streamlit as st
import requests
import pandas as pd
from difflib import SequenceMatcher

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="AI Medicine Alternative Finder",
    page_icon="💊",
    layout="wide"
)

# -----------------------------
# CUSTOM CSS
# -----------------------------

st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}

.title {
    font-size: 42px;
    font-weight: bold;
    color: #0f172a;
}

.subtitle {
    font-size: 18px;
    color: #475569;
}

.med-card {
    background-color: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.08);
}

.price {
    color: green;
    font-size: 22px;
    font-weight: bold;
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
    text-align:center;
    margin-top:50px;
    color:gray;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATABASE
# -----------------------------

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

FDA_API = "https://api.fda.gov/drug/ndc.json"

PHARMACY_LINKS = {
    "1mg": "https://www.1mg.com/search/all?name={}",
    "NetMeds": "https://www.netmeds.com/catalogsearch/result/{}",
    "PharmEasy": "https://pharmeasy.in/search/all?name={}"
}

# -----------------------------
# FUNCTIONS
# -----------------------------

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

def generate_links(medicine):

    links = {}

    for pharmacy, url in PHARMACY_LINKS.items():
        links[pharmacy] = url.format(
            medicine.replace(" ", "%20")
        )

    return links

# -----------------------------
# HEADER
# -----------------------------

st.markdown(
    '<div class="title">💊 AI Medicine Alternative Finder</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find cheaper medicine alternatives instantly using AI logic.</div>',
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# SEARCH SECTION
# -----------------------------

medicine_name = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Find Alternatives")

# -----------------------------
# SEARCH LOGIC
# -----------------------------

if search_btn and medicine_name:

    st.subheader("Medicine Information")

    medicine_data = fetch_medicine_data(medicine_name)

    if medicine_data:

        brand = medicine_data.get("brand_name", "N/A")
        generic = medicine_data.get("generic_name", "N/A")
        manufacturer = medicine_data.get("labeler_name", "N/A")

        info_df = pd.DataFrame({
            "Field": ["Brand", "Generic", "Manufacturer"],
            "Value": [brand, generic, manufacturer]
        })

        st.table(info_df)

    else:
        st.warning("Medicine information not found from FDA API.")

    # -----------------------------
    # ALTERNATIVES
    # -----------------------------

    st.subheader("💰 Cheaper Alternatives")

    alternatives = find_cheaper_alternatives(medicine_name)

    if not alternatives:
        st.error("No cheaper alternatives found.")
    else:

        for alt in alternatives:

            links = generate_links(alt["name"])

            st.markdown(f"""
            <div class="med-card">
                <h2>{alt['name']}</h2>
                <div class="price">₹{alt['price']}</div>
                <p>Similarity Score: {alt['score']}</p>

                <a class="buy-btn" href="{links['1mg']}" target="_blank">
                Buy on 1mg
                </a>

                <a class="buy-btn" href="{links['NetMeds']}" target="_blank">
                Buy on NetMeds
                </a>

                <a class="buy-btn" href="{links['PharmEasy']}" target="_blank">
                Buy on PharmEasy
                </a>
            </div>
            """, unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.title("📌 About")

st.sidebar.info(
    """
    This AI medicine finder helps users:
    
    ✅ Find cheaper alternatives  
    ✅ Compare medicine prices  
    ✅ Get pharmacy links  
    ✅ Save medicine costs  
    """
)

st.sidebar.title("🛠 Tech Stack")

st.sidebar.write("""
- Python
- Streamlit
- Requests
- Pandas
- AI Similarity Matching
""")

# -----------------------------
# FOOTER
# -----------------------------

st.markdown(
    """
    <div class="footer">
    Made with ❤️ using Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)
