# ============================================================
# MediSaver.py
# AI Medicine Alternative Finder
# Improved Informative UI
# Google AI Search + SerpAPI + Purchase Links
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

.buy-btn {
    text-decoration: none;
    background: #2563eb;
    color: white !important;
    padding: 12px 20px;
    border-radius: 10px;
    display: inline-block;
    margin-top: 12px;
    margin-right: 10px;
    font-weight: 600;
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

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine"
    }

# ============================================================
# GOOGLE AI SEARCH
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
                    item.get("title", "No Title"),

                    "snippet":
                    item.get(
                        "snippet",
                        "No description available"
                    ),

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
        # RESULTS
        # ====================================================

        st.subheader("🤖 AI Search Results")

        if not results:

            st.warning(
                "No alternate medicines found."
            )

        else:

            for result in results:

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
                        font-size:30px;
                        ">
                        💊
                        </div>

                        <div>

                            <h2 style="
                            margin:0;
                            color:#0f172a;
                            font-size:28px;
                            font-weight:700;
                            ">

                            {result['title']}

                            </h2>

                            <p style="
                            margin-top:10px;
                            color:#475569;
                            font-size:16px;
                            line-height:1.7;
                            ">

                            {result['snippet']}

                            </p>

                        </div>

                    </div>

                    <div style="margin-top:20px;">

                        <a href="{result['link']}"
                           target="_blank"
                           class="buy-btn">

                           🔍 View Full Details

                        </a>

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
                🛒 Buy Alternative Medicine Online
                </h3>
                """, unsafe_allow_html=True)

                links = generate_purchase_links(
                    medicine_name
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
✅ Informative Medicine Cards  
✅ Purchase Links  
✅ 1mg / PharmEasy / Truemeds  
✅ Modern Frontend UI  
✅ Streamlit Based App  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + SerpAPI

</div>
""", unsafe_allow_html=True)
