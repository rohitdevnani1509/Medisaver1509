# ============================================================
# MediSaver.py
# OpenAI + Google Search Medicine Alternative Finder
# ============================================================

# INSTALL:
# pip install streamlit openai requests

# RUN:
# streamlit run MediSaver.py

# ============================================================

import streamlit as st
import requests
from openai import OpenAI

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="MediSaver",
    page_icon="💊",
    layout="wide"
)

# ============================================================
# HEADER
# ============================================================

st.title("💊 MediSaver")

st.write(
    "Find alternative medicines using OpenAI + Google Search"
)

# ============================================================
# SIDEBAR API KEYS
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

# ============================================================
# GOOGLE SEARCH
# ============================================================

def google_search(query, api_key, cx):

    url = "https://www.googleapis.com/customsearch/v1"

    params = {
        "key": api_key,
        "cx": cx,
        "q": query,
        "num": 5
    }

    response = requests.get(url, params=params)

    data = response.json()

    results = []

    if "items" in data:

        for item in data["items"]:

            results.append({
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            })

    return results

# ============================================================
# OPENAI EXTRACTION
# ============================================================

def extract_alternatives(
    medicine,
    search_results,
    openai_key
):

    client = OpenAI(api_key=openai_key)

    content = ""

    for result in search_results:

        content += f"""
        Title: {result['title']}
        Snippet: {result['snippet']}
        """

    prompt = f"""
    Extract alternative medicines for {medicine}
    from the following Google search results.

    Return:
    - medicine name
    - short description

    Search Results:
    {content}
    """

    response = client.chat.completions.create(

        model="gpt-4o-mini",

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response.choices[0].message.content

# ============================================================
# PURCHASE LINKS
# ============================================================

def generate_links(medicine):

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
        f"https://pharmeasy.in/search/all?name={med}"
    }

# ============================================================
# USER INPUT
# ============================================================

medicine = st.text_input(
    "Enter Medicine Name",
    placeholder="Example: Crocin"
)

if st.button("Find Alternatives"):

    if not OPENAI_API_KEY:
        st.error("Enter OpenAI API key")

    elif not GOOGLE_API_KEY:
        st.error("Enter Google API key")

    elif not SEARCH_ENGINE_ID:
        st.error("Enter Search Engine ID")

    elif not medicine:
        st.error("Enter medicine name")

    else:

        with st.spinner("Searching Google..."):

            results = google_search(
                f"{medicine} generic substitute medicine",
                GOOGLE_API_KEY,
                SEARCH_ENGINE_ID
            )

        if not results:

            st.warning("No search results found.")

        else:

            with st.spinner("Analyzing alternatives with OpenAI..."):

                alternatives = extract_alternatives(
                    medicine,
                    results,
                    OPENAI_API_KEY
                )

            st.subheader("💊 Alternative Medicines")

            st.write(alternatives)

            st.subheader("🛒 Purchase Links")

            links = generate_links(medicine)

            for site, link in links.items():

                st.markdown(
                    f"[Buy on {site}]({link})"
                )
