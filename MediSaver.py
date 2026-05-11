# ============================================================
# EXTRACT ALTERNATIVE MEDICINE NAMES
# ============================================================

alternative_names = set()

for result in results:

    title = result.get("title", "")

    words = title.split()

    for word in words:

        clean_word = word.replace("|", "").replace(",", "")

        # Ignore generic unwanted words
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
            "effects"
        ]

        if len(clean_word) > 3:

            if clean_word.lower() not in ignored:

                alternative_names.add(clean_word)

# ============================================================
# SHOW CLEAN MEDICINE CARDS
# ============================================================

st.subheader("💊 Alternate Medicines")

if not alternative_names:

    st.warning("No alternate medicines found.")

else:

    for medicine in sorted(alternative_names):

        st.markdown(f"""
        <div class="result-card">

            <div style="
            display:flex;
            align-items:center;
            justify-content:space-between;
            flex-wrap:wrap;
            gap:15px;
            ">

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

        </div>
        """, unsafe_allow_html=True)

        # ====================================================
        # PURCHASE LINKS
        # ====================================================

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
