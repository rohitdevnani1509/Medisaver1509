# ============================================================
# MediSaver.py
# AI Medicine Alternative Finder
# Single Working File
# ============================================================

# INSTALL:
# pip install -r requirements.txt

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

.result-card {
    background: white;
    padding: 25px;
    border-radius: 18px;
    margin-bottom: 25px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    border-left: 6px solid #2563eb;
    transition: 0.3s ease;
}

.result-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.12);
}

.purchase-btn {
    text-decoration: none;
    background: #16a34a;
    color: white !important;
    padding: 12px 16px;
    border-radius: 10px;
    display: block;
    text-align: center;
    font-weight: 600;
    margin-bottom: 12px;
}

.ai-box {
    background: #eef6ff;
    border-left: 6px solid #2563eb;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 25px;
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
    '<div class="title">💊 MediSaver AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Find alternate medicines dynamically using Google AI Search + SerpAPI.</div>',
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

        "Apollo":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# SEARCH FUNCTION
# ============================================================

def search_alternatives(
    medicine_name,
    api_key
):

    url = "https://serpapi.com/search.json"

    query = f"{medicine_name} substitute medicine"

    params = {

        "engine": "google",

        "q": query,

        "api_key": api_key,

        "num": 10,

        "google_domain": "google.com",

        "hl": "en",

        "gl": "us"
    }

    ai_answer = None
    alternatives = []

    try:

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        # ====================================================
        # AI SUMMARY
        # ====================================================

        if "answer_box" in data:

            ai_answer = data["answer_box"].get(
                "snippet",
                "No AI summary available."
            )

        elif "knowledge_graph" in data:

            ai_answer = data["knowledge_graph"].get(
                "description",
                "No AI summary available."
            )

        # ====================================================
        # ORGANIC RESULTS
        # ====================================================

        if "organic_results" in data:

            for item in data["organic_results"]:

                alternatives.append({

                    "title":
                    item.get("title", ""),

                    "snippet":
                    item.get("snippet", ""),

                    "link":
                    item.get("link", "#")
                })

        return ai_answer, alternatives

    except Exception as e:

        st.error(f"Search Error: {e}")

        return None, []

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
            "Searching AI alternatives..."
        ):

            ai_summary, results = search_alternatives(
                medicine_name,
                SERP_API_KEY
            )

        # ====================================================
        # AI SUMMARY
        # ====================================================

        if ai_summary:

            st.subheader("🤖 AI Search Summary")

            st.markdown(f"""
            <div class="ai-box">

            {ai_summary}

            </div>
            """, unsafe_allow_html=True)

        # ====================================================
        # EXTRACT MEDICINE NAMES
        # ====================================================

        alternative_names = set()

        for result in results:

            title = result.get("title", "")

            words = title.split()

            for word in words:

                clean_word = (
                    word
                    .replace("|", "")
                    .replace(",", "")
                    .replace("(", "")
                    .replace(")", "")
                )

                ignored = [

                    "tablet",
                    "tablets",
                    "capsule",
                    "capsules",
                    "uses",
                    "price",
                    "substitutes",
                    "substitute",
                    "medicine",
                    "mg",
                    "side",
                    "effects",
                    "for",
                    "and",
                    "with",
                    "the"
                ]

                if len(clean_word) > 3:

                    if clean_word.lower() not in ignored:

                        alternative_names.add(
                            clean_word
                        )

        # ====================================================
        # DISPLAY RESULTS
        # ====================================================

        st.subheader("💊 Alternate Medicines")

        if not alternative_names:

            st.warning(
                "No alternate medicines found."
            )

        else:

            for medicine in sorted(alternative_names):

                st.markdown(f"""
                <div class="result-card">

                    <div style="
                    display:flex;
                    align-items:center;
                    gap:15px;
                    ">

                        <div style="
                        background:#eff6ff;
                        padding:12px;
                        border-radius:12px;
                        font-size:28px;
                        ">
                        💊
                        </div>

                        <div>

                            <h2 style="
                            margin:0;
                            color:#0f172a;
                            font-size:26px;
                            font-weight:700;
                            ">

                            {medicine}

                            </h2>

                        </div>

                    </div>

                </div>
                """, unsafe_allow_html=True)

                # =============================================
                # PURCHASE LINKS
                # =============================================

                st.markdown("""
                <h3 style="
                margin-top:15px;
                margin-bottom:15px;
                color:#0f172a;
                ">
                🛒 Buy Medicine Online
                </h3>
                """, unsafe_allow_html=True)

                links = generate_purchase_links(
                    medicine
                )

                cols = st.columns(3)

                index = 0

                for site, link in links.items():

                    with cols[index % 3]:

                        st.markdown(f"""
                        <a href="{link}"
                           target="_blank"
                           class="purchase-btn">

                           Buy on {site}

                        </a>
                        """, unsafe_allow_html=True)

                    index += 1

                st.markdown("<hr>", unsafe_allow_html=True)

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ Runtime SerpAPI Key  
✅ Google AI Search  
✅ AI Search Summary  
✅ Alternate Medicine Finder  
✅ Purchase Links  
✅ 1mg / PharmEasy / Truemeds  
✅ Modern Frontend UI  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
