import pandas as pd
import re
import streamlit as st

# Upload file
uploaded_file = st.file_uploader("Upload Excel or CSV", type=["xlsx", "xls", "csv"])
if uploaded_file:
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.write("### Preview of Uploaded Data")
    st.dataframe(df.head())

    # Input: name column to classify
    name_column = st.selectbox("Select the column containing names", df.columns)

    # Keywords list (yours + extended, no removal)
    keywords = [
        "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
        "accounts", "payable", "university", "pharma", "clinic", "government", "foundation", "trust", "group", "bank",
        "hospital", "srl", "gmbh", "bhd", "s.a", "plc", "institute", "association", "organization", "network", "partners",
        "consulting", "company", "enterprise", "committee", "council", "ministry", "ngo", "dental", "medtech", "research",
        "govt", "logistics", "academy", "solutions", "holding", "services", "ventures", "industries", "labo", "univ",
        "healthcare", "laboratory", "medical", "medicine", "commerce", "distribution", "development", "educational",
        "international", "trading", "global", "insurance", "corporativo", "innovation", "technology", "r&d", "office",
        "admin", "metro", "sante", "hopital", "dispensary", "home", "cabinet", "gabinet", "therapeutics", "dott.", "sro",
        "forest", "products", "board", "publishing", "publisher", "school", "denta", "asociacion", "ies", "torre", "vicens",
        "environment", "unlimited", "syndicate", "venture", "accelerator", "incubator", "cardio", "cardiofront",
        "cleveland", "physio"
    ]
    keywords = sorted(set([k.lower() for k in keywords]), key=len, reverse=True)

    titles = ["mr", "mr.", "ms", "ms.", "mrs", "mrs.", "dr", "dr."]

    def classify_name(name):
        name = str(name).lower()

        if re.search(r"[^a-zA-Z0-9.\- ]", name):
            return "Needs Review"

        if any(re.search(rf"\b{k}\b", name) for k in keywords):
            return "Out of Scope"

        if any(name.startswith(t + " ") or f" {t} " in name for t in titles):
            return "In Scope"

        return "In Scope"

    df["Classification"] = df[name_column].apply(classify_name)

    st.write("### Classified Results")
    st.dataframe(df)

    # Download link
    st.download_button(
        label="Download Classified File",
        data=df.to_csv(index=False),
        file_name="classified_output.csv",
        mime="text/csv"
    )
