import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Customer Categorizer", layout="wide")

# Non-individual keywords (integrated with potential 29,450 list patterns)
non_individual_keywords = [
    # Legal/Corporate Structures (Global)
    "inc", "inc.", "llc", "l.l.c.", "ltd", "ltd.", "limited", "corp", "corporation", "co", "co.", "pte", "pvt", "llp", "home",
    "accounts", "payable", "price", "IPSB", "gmbh", "ag", "nv", "bv", "kk", "oy", "ab", "plc", "s.a", "s.a.s", "sa", "sarl", "sl",
    "aps", "as", "kft", "pt", "sdn", "bhd", "dite", "cabinet", "gabinet", "univ", "university", "srl", "pty ltd", "se", "a/s",
    "sp zoo", "eurl", "LIBRARY", "IFSI ", "sante", "BTP", "nord", "travail", "hopital", "grand", "site", "COMMUNITY", "urban",
    "AGGLOPOLYS", "AZIENDA SOCIO SANITARIA TERRITORIALE GRANDE OSPEDALE METROPOLITANO NIGUARDA", "ACHYUT",
    # Pharmacy/Healthcare (Global)
    "pharmacy", "drugstore", "healthcare", "medical", "clinic", "hospital", "apothecary", "dispensary", "NIGUARDA", "TECNICAS",
    "ICO", "THERAPEUTICS", "OPTIMAL", "coll", "med", "dent", "denta", "PHARMACEUTICALS", "PHARMACEUTICAL", "pharma",
    # Academic/Institutional
    "university", "uni", "institute", "inst", "college", "academy", "school", "faculty", "dept", "department", "loire", "dente",
    "tech", "SRL", "S.R.L", "personal", "homemed", "sro",
    # Science/R&D
    "centre", "center", "r&d", "science", "biotech", "medtech", "ai", "fondu", "funda", "Cardio", "college", "ctr", "adult",
    "lake", "comm", "education", "edu", "resource", "care", "health", "ASOCIACION", "CIF", "IES TORRE VICENS",
    # Government/NGO
    "govt", "government", "ngo", "n.g.o", "nonprofit", "non-profit", "ministry", "embassy", "consulate", "office", "admin",
    "administration", "secretariat", "authority", "commission", "agency", "bureau", "OSPEDALE", "valley", "limited", "ltd",
    "ltd.", "unlimited",
    # Professional Services
    "solutions", "consulting", "consultants", "advisory", "advisors", "partners", "partnership", "associates", "services",
    "ventures", "enterprises", "management", "finance", "capital", "holdings", "intl", "international", "global", "industries",
    "logistics", "trading", "procurement", "group", "SAR", "S.A.R", "DOTT.", "sro", "dos", "santos", "labo", "laboratory",
    "products", "forest",
    # Retail/Media
    "store", "shop", "outlet", "market", "retail", "distributors", "hlth", "mental", "ment", "mntl", "agency", "environment",
    "borad", "environment", "investigation", "agency", "PHYSIO",
    # Others
    "foundation", "trust", "association", "organization", "network", "CNRS", "C.N.R.S", "state", "SCTD", "europe", "medcor",
    "medi", "metro", "SOCIO", "METROPOLITANO", "County", "council", "foundation", "fondation", "trust", "union", "syndicate",
    "board", "chamber", "association", "club", "society", "network", "cooperative", "federation", "council", "committee",
    "coalition", "initiative", "team", "division", "branch", "unit", "project", "consortium", "alliance", "hub", "taskforce",
    "incubator", "accelerator",
    # Potential Keywords from 29,450 List (Assumed from global patterns)
    "company", "organization", "institution", "corporativo", "gesellschaft", "assurance", "bank", "insurance", "enterprise",
    "commerce", "trade", "supply", "distribution", "networking", "technology", "innovation", "research", "development",
    "healthcare", "medical", "dental", "pharmaceutical", "therapeutics", "optimal", "clinic", "hospitality", "services",
    "consulting", "partners", "group", "holdings", "international", "global", "industries", "logistics", "trading","FOUNDATION","publishing","cleveland","press","inc","inc.","science","america","advancement","acpa","jounrnal","publishers","department","injury","civil","society",
]

# Enhanced out-of-scope detection logic
def classify_name(name):
    try:
        if not isinstance(name, str):
            return "Needs Review"
        name = name.strip().lower()
        # Check for non-individual keywords with improved regex
        for keyword in non_individual_keywords:
            pattern = rf'\b{re.escape(keyword)}\b(?=\s|$)'
            if re.search(pattern, name, re.IGNORECASE):
                return "Out of Scope"
        return "In Scope"  # Default to In Scope if no keywords match
    except Exception as e:
        st.error(f"Classification error for '{name}': {e}")
        return "Needs Review"

# UI setup and main app logic
st.title("🌍 Global Customer Categorizer")
st.markdown("""
This tool categorizes customers as **Out of Scope (Non-Individuals)** or **In Scope (Individuals)** based on global keywords. Upload your Excel/CSV file to start.
""")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV file", type=["csv", "xlsx"], help="Upload a file with a 'name' column or similar.")

if uploaded_file is not None:
    try:
        # Process in chunks for large datasets
        chunksize = 1000
        chunks = []
        for chunk in pd.read_csv(uploaded_file, chunksize=chunksize) if uploaded_file.name.lower().endswith('.csv') else pd.read_excel(uploaded_file, chunksize=chunksize):
            chunk["Scope Status"] = chunk.apply(lambda row: classify_name(row[chunk.columns[0]] if "name" in chunk.columns else row[chunk.columns[0]]), axis=1)
            chunks.append(chunk)

        df = pd.concat(chunks, ignore_index=True)

        # Auto-detect name column or let user select
        name_col = next((col for col in df.columns if "name" in col.lower() or "customer" in col.lower()), None)
        if not name_col:
            name_col = st.selectbox("🔍 Select the column containing customer names:", df.columns.tolist())

        st.info(f"🔧 Using column: **{name_col}** for categorization")

        # Apply classification (already done in chunks)
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
