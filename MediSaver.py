# ============================================================
# MediSaver.py
# Dynamic Medicine Alternative Finder
# Google Search + SerpAPI + Streamlit UI
# ============================================================

# INSTALL:
# pip install streamlit requests pandas

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
import re

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
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 20px;
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
}

.footer {
    text-align: center;
    color: gray;
    margin-top: 50px;
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
# EXTRACT MEDICINE NAMES
# ============================================================

def extract_possible_medicines(text):

    # Remove special chars
    text = re.sub(r'[^a-zA-Z0-9\\s-]', ' ', text)

    words = text.split()

    medicines = []

    for word in words:

        if len(word) > 3:

            if word.lower() not in [
                "medicine",
                "tablets",
                "capsule",
                "generic",
                "substitute",
                "alternative",
                "mg",
                "uses",
                "price",
                "side",
                "effects"
            ]:

                medicines.append(word)

    return list(set(medicines))

# ============================================================
# SERPAPI SEARCH FUNCTION
# ============================================================

def search_alternative_medicines(
    medicine_name,
    api_key
):

    url = "https://serpapi.com/search.json"

    query = f"{medicine_name} generic substitute alternative medicine"

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 10
    }

    medicines = []

    try:

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        # ====================================================
        # ORGANIC RESULTS
        # ====================================================

        if "organic_results" in data:

            for item in data["organic_results"]:

                title = item.get("title", "")

                snippet = item.get("snippet", "")

                link = item.get("link", "#")

                extracted = extract_possible_medicines(
                    title + " " + snippet
                )

                medicines.append({

                    "title": title,

                    "snippet": snippet,

                    "link": link,

                    "alternatives": extracted[:10]
                })

        # ====================================================
        # RELATED QUESTIONS
        # ====================================================

        if "related_questions" in data:

            for item in data["related_questions"]:

                question = item.get("question", "")

                snippet = item.get("snippet", "")

                link = item.get("link", "#")

                extracted = extract_possible_medicines(
                    question + " " + snippet
                )

                medicines.append({

                    "title": question,

                    "snippet": snippet,

                    "link": link,

                    "alternatives": extracted[:10]
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

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine",

        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Apollo":
        f"https://www.apollopharmacy.in/search-medicines/{med}"
    }

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

            results = search_alternative_medicines(
                medicine_name,
                SERP_API_KEY
            )

        st.subheader("💊 Alternative Medicines")

        if not results:

            st.warning("No alternatives found.")

        else:

            all_alternatives = set()

            for result in results:

                for med in result["alternatives"]:

                    all_alternatives.add(med)

            # =================================================
            # DISPLAY ALTERNATIVES
            # =================================================

            for alt in sorted(all_alternatives):

                st.markdown(f"""
                <div class="card">

                    <h2>{alt}</h2>

                </div>
                """, unsafe_allow_html=True)

                # =============================================
                # PURCHASE LINKS
                # =============================================

                st.markdown("### 🛒 Buy Online")

                links = generate_purchase_links(
                    alt
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

            # =================================================
            # GOOGLE SOURCES
            # =================================================

            st.subheader("🔍 Google Sources")

            for result in results:

                st.markdown(f"""
                <div class="card">

                    <h3>{result['title']}</h3>

                    <p>{result['snippet']}</p>

                    <a class="buy-btn"
                       href="{result['link']}"
                       target="_blank">

                       Open Source

                    </a>

                </div>
                """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR INFO
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Runtime SerpAPI Key  
✅ Dynamic Google Search  
✅ No Hardcoded Medicines  
✅ Live Medicine Alternatives  
✅ Purchase Links  
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
