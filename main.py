import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Customer Categorizer", layout="wide")

# Expanded non-individual keywords for global coverage
non_individual_keywords = [
    # Legal/Corporate Structures (Global)
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp","home","accounts","payable","price","IPSB",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd","dite","cabinet","gabinet","univ","university",
    "srl", "pty ltd", "se", "a/s", "sp zoo", "eurl","LIBRARY","IFSI ","sante","BTP","nord","travail","hopital","grand","site","COMMUNITY","urban","AGGLOPOLYS",
    # Pharmacy/Healthcare (Global)
    "pharmacy", "drugstore", "healthcare", "medical", "clinic", "hospital", "apothecary", "dispensary","NIGUARDA","TECNICAS","ICO","THERAPEUTICS","OPTIMAL","coll","med","dent",
    # Academic/Institutional
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department","loire","dente","tech","SRL","S.R.L","personal","homemed","sro"
    # Science/R&D
    "centre", "center", "r&d", "science", "biotech", "medtech", "ai","fondu","funda","Cardio","college","ctr","adult","lake","comm","education","edu","resource","care","health",
    # Government/NGO
    "govt", "government", "ngo", "ministry", "agency", "authority","OSPEDALE","valley","limited","ltd","ltd.","unlimited","ACHYUT","store", "shop", "bookshop", "library", "distribution", "distributors", "outlet", "media", "publications", "books", "press",
    # Professional Services
    "solutions", "consulting", "partners", "services", "group", "holdings", "enterprises","SAR","S.A.R","DOTT.","sro","dos","santos","labo","laboratory","products","forest",
    # Retail/Media
    "store", "shop", "outlet", "market", "retail", "distributors","hlth","mental","ment","mntl","agency","environment","borad","environment","investigation","agency",""
    # Others
    "foundation", "trust", "association", "organization", "network","CNRS","C.N.R.S","state","SCTD","europe","medcor","medi","metro","SOCIO","METROPOLITANO","County","council","foundation", "fondation", "trust", "union", "syndicate", "board", "chamber", "association", "club", "society",
    "network", "cooperative", "federation", "council", "committee", "coalition", "initiative",
    # Professional / Financial Services
    "solutions", "consulting", "consultants", "advisory", "advisors", "partners", "partnership", "associates",
    "services", "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl", "international",
    "global", "industries", "logistics", "trading", "procurement", "group",
    #govt
    "govt", "government", "ngo", "n.g.o", "nonprofit", "non-profit", "ministry", "embassy", "consulate",
    "office", "admin", "administration", "secretariat", "authority", "commission", "agency", "bureau","solutions", "consulting", "consultants", "advisory", "advisors", "partners", "partnership", "associates",
    "services", "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl", "international",
    "global", "industries", "logistics", "trading", "procurement", "group","team", "division", "branch", "unit", "project", "consortium", "alliance", "hub", "taskforce", "incubator", "accelerator",
    # Science / R&D
    "centre", "center", "r&d", "science", "sciences", "technical", "technological", "technology", "innovation",
    "biotech", "medtech", "ai", "ml", "cybernetics",
    # Legal/Corporate Structures
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp",
    "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl", "aps", "as", "kft", "pt", "sdn", "bhd",

    # Academic / Institutional
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department", "cnrs",
    "research", "laboratory", "lab", "education", "educational", "engineering", "polytechnic", "polytech",
]

# Enhanced out-of-scope detection logic
def classify_name(name):
    try:
        if not isinstance(name, str):
            return "Needs Review"
        name = name.strip().lower()
        # Check for non-individual keywords with regex for better matching
        for keyword in non_individual_keywords:
            if re.search(rf'\b{re.escape(keyword)}\b', name):
                return "Out of Scope"
        return "In Scope"  # Default to In Scope if no keywords match
    except Exception as e:
        st.error(f"Classification error for '{name}': {e}")
        return "Needs Review"

# UI setup and main app logic
st.title("🌍 Global Customer Categorizer")
st.markdown("""
This tool categorizes customers as **Out of Scope (Non-Individuals)** (e.g., companies, institutions) or **In Scope (Individuals)** based on global keywords. Upload your Excel/CSV file to start.
""")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV file", type=["csv", "xlsx"], help="Upload a file with a 'name' column or similar.")

if uploaded_file is not None:
    try:
        ext = os.path.splitext(uploaded_file.name)[1].lower()

        if ext == ".csv":
            df = pd.read_csv(uploaded_file)
        elif ext in [".xls", ".xlsx"]:
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format. Please use .csv or .xlsx.")
            st.stop()

        # Auto-detect name column or let user select
        name_col = None
        for col in df.columns:
            if "name" in col.lower() or "customer" in col.lower():
                name_col = col
                break

        if not name_col:
            name_col = st.selectbox("🔍 Select the column containing customer names:", df.columns.tolist())

        st.info(f"🔧 Using column: **{name_col}** for categorization")

        # Apply classification
        df["Scope Status"] = df[name_col].apply(classify_name)
        st.success("✅ Categorization completed successfully!")

        # Display results
        st.subheader("📊 Categorization Results")
        st.dataframe(df.head(50))  # Show more rows for review

        # Downloadable result
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name="Categorized")
        output.seek(0)
        st.download_button(
            label="⬇️ Download Categorized File",
            data=output.getvalue(),
            file_name=f"categorized_customers_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Download the categorized data as an Excel file."
        )

        # Summary stats
        st.subheader("📈 Summary")
        scope_counts = df["Scope Status"].value_counts()
        st.write("Categorization Breakdown:")
        st.json(scope_counts.to_dict())

    except Exception as e:
        st.error(f"❌ An error occurred: {e}")
