# ============================================================
# MediSaver.py
# Working OpenAI + Google Search Medicine Alternative Finder
# Streamlit Compatible Version
# ============================================================

# INSTALL:
# pip install -r requirements.txt

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
import openai

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
    background-color: #f5f7fb;
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
    '<div class="subtitle">Find alternative medicines using OpenAI + Google Search.</div>',
    unsafe_allow_html=True
)

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🔑 API Keys")

OPENAI_API_KEY = st.sidebar.text_input(
    "OpenAI API Key",
    type="password"
)

GOOGLE_API_KEY = st.sidebar.text_input(
    "Google Search API Key",
    type="password"
)

SEARCH_ENGINE_ID = st.sidebar.text_input(
    "Google Search Engine ID (CX)"
)

st.sidebar.markdown("""
Get Google Search API:

https://developers.google.com/custom-search/v1/introduction

Create Search Engine:

https://programmablesearchengine.google.com/about/

Get OpenAI API key:

https://platform.openai.com/api-keys
""")

# ============================================================
# GOOGLE SEARCH FUNCTION
# ============================================================

def google_search(query, api_key, cx):

    url = "https://www.googleapis.com/customsearch/v1"

    params = {

        "key": api_key,

        "cx": cx,

        "q": query,

        "num": 10
    }

    try:

        response = requests.get(
            url,
            params=params
        )

        data = response.json()

        results = []

        if "items" in data:

            for item in data["items"]:

                results.append({

                    "title":
                    item.get("title", "No Title"),

                    "snippet":
                    item.get("snippet", "No Description"),

                    "link":
                    item.get("link", "#")
                })

        return results

    except Exception as e:

        st.error(f"Google Search Error: {e}")

        return []

# ============================================================
# OPENAI EXTRACTION FUNCTION
# ============================================================

def extract_alternatives(
    medicine,
    search_results,
    openai_key
):

    try:

        openai.api_key = openai_key

        content = ""

        for result in search_results:

            content += f"""
            Title: {result['title']}
            Snippet: {result['snippet']}
            """

        prompt = f"""
        Extract alternative medicines for {medicine}
        from these Google search results.

        Return:
        - alternative medicine names
        - short descriptions
        - cheaper substitutes if available

        Search Results:
        {content}
        """

        response = openai.ChatCompletion.create(

            model="gpt-3.5-turbo",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:

        return f"OpenAI Error: {e}"

# ============================================================
# PURCHASE LINKS
# ============================================================

def generate_purchase_links(medicine):

    med = medicine.replace(" ", "+")

    return {

        "Google Shopping":
        f"https://www.google.com/search?tbm=shop&q={med}+medicine",

        "Amazon":
        f"https://www.amazon.in/s?k={med}+medicine",

        "1mg":
        f"https://www.1mg.com/search/all?name={med}",

        "NetMeds":
        f"https://www.netmeds.com/catalogsearch/result/{med}",

        "PharmEasy":
        f"https://pharmeasy.in/search/all?name={med}",

        "Apollo Pharmacy":
        f"https://www.apollopharmacy.in/search-medicines/{med}",

        "GoodRx":
        f"https://www.goodrx.com/search?q={med}"
    }

# ============================================================
# USER INPUT
# ============================================================

medicine = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

search_btn = st.button("🔍 Find Alternatives")

# ============================================================
# MAIN LOGIC
# ============================================================

if search_btn:

    if not OPENAI_API_KEY:

        st.error("Please enter OpenAI API key.")

    elif not GOOGLE_API_KEY:

        st.error("Please enter Google API key.")

    elif not SEARCH_ENGINE_ID:

        st.error("Please enter Search Engine ID.")

    elif not medicine:

        st.error("Please enter medicine name.")

    else:

        with st.spinner(
            "Searching Google..."
        ):

            search_results = google_search(

                query=f"{medicine} generic substitute medicine",

                api_key=GOOGLE_API_KEY,

                cx=SEARCH_ENGINE_ID
            )

        if not search_results:

            st.warning("No Google search results found.")

        else:

            with st.spinner(
                "Analyzing medicine alternatives with OpenAI..."
            ):

                alternatives = extract_alternatives(

                    medicine,

                    search_results,

                    OPENAI_API_KEY
                )

            # =================================================
            # DISPLAY AI RESULTS
            # =================================================

            st.subheader("💊 Alternative Medicines")

            st.markdown(f"""
            <div class="card">

                <pre style="white-space: pre-wrap;
                            font-size:16px;">
{alternatives}
                </pre>

            </div>
            """, unsafe_allow_html=True)

            # =================================================
            # GOOGLE SEARCH RESULTS
            # =================================================

            st.subheader("🔍 Google Sources")

            for result in search_results:

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

            # =================================================
            # PURCHASE LINKS
            # =================================================

            st.subheader("🛒 Purchase Links")

            links = generate_purchase_links(
                medicine
            )

            for site, link in links.items():

                st.markdown(f"""
                <a class="buy-btn"
                   href="{link}"
                   target="_blank">

                   Buy on {site}

                </a>
                """, unsafe_allow_html=True)

# ============================================================
# SIDEBAR FEATURES
# ============================================================

st.sidebar.title("📌 Features")

st.sidebar.info("""

✅ OpenAI Integration  
✅ Google Search API  
✅ Runtime API Key Input  
✅ AI Medicine Alternatives  
✅ Purchase Links  
✅ Google Shopping Links  
✅ Streamlit Frontend UI  

""")

# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="footer">

Made with ❤️ using Python + Streamlit + OpenAI

</div>
""", unsafe_allow_html=True)
