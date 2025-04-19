import streamlit as st
import pandas as pd
import os
from io import BytesIO
import re
import time

# Set page configuration as the first Streamlit command
st.set_page_config(page_title="Customer Categorizer", layout="wide")

# Non-individual keywords (base list + space for your additions)
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
    # Potential Keywords from 29,450 List (Assumed)
    "company", "organization", "institution", "corporativo", "gesellschaft", "assurance", "bank", "insurance", "enterprise",
    "commerce", "trade", "supply", "distribution", "networking", "technology", "innovation", "research", "development",
    "healthcare", "medical", "dental", "pharmaceutical", "therapeutics", "optimal", "clinic", "hospitality", "services",
    "consulting", "partners", "group", "holdings", "international", "global", "industries", "logistics", "trading",
    # Add your missing keywords here as you find them
    # Example: 
    "publishing","publisher","agency","MEDICINE","DENTISTRY","ACADEMIC","COMPANY","BOARD","FOUNDATION","CLEVELAND","CARDIOFRONT","univ","BOOLE","CCMAR","ABBVIE","ROD","BW-FAULKNER","MEMORIALCARE","APNIMED","CWSHIN"
    "NOBLIS","CONDE","ESTRO"
]

# Out-of-scope detection logic based on strict keyword matching
def classify_name(name):
    try:
        if not isinstance(name, str):
            return "Needs Review"
        name = name.strip().lower()
        # Check for keyword match (no ignore for . or - when keyword is present)
        for keyword in non_individual_keywords:
            pattern = rf'\b{re.escape(keyword)}\b(?=\s|$)'
            if re.search(pattern, name, re.IGNORECASE):
                return "Out of Scope"
        # Check for special characters (except . and -)
        special_chars = re.compile(r'[^a-zA-Z0-9.\-]')
        if special_chars.search(name):
            return "Needs Review"
        # If only . or - are present (e.g., Dr., Smith-Jones) and no keyword, mark as In Scope
        if re.search(r'[.\-]', name) and not any(re.search(rf'\b{re.escape(keyword)}\b(?=\s|$)', name, re.IGNORECASE) for keyword in non_individual_keywords):
            return "In Scope"
        # Default to In Scope if no keyword or special chars (except . and -)
        return "In Scope"
    except Exception as e:
        st.error(f"Classification error for '{name}': {e}")
        return "Needs Review"

# UI setup and main app logic
st.title("🌍 Global Customer Categorizer")
st.markdown("""
This tool categorizes customers as **Out of Scope**, **In Scope**, or **Needs Review** based on strict keyword matching. Upload your Excel/CSV file to start.
For files >200MB, process locally or split into parts.
""")

uploaded_file = st.file_uploader("📤 Upload Excel or CSV file", type=["csv", "xlsx"], help="For files >200MB, process locally or split into parts.")

if uploaded_file is not None:
    try:
        # Adjustable chunk size for large datasets (only for CSV)
        chunksize = st.slider("Select chunk size (rows, for CSV only)", 500, 5000, 1000, step=500) if uploaded_file.name.lower().endswith('.csv') else None
        st.write(f"Processing with chunk size: {chunksize} rows" if chunksize else "Processing Excel file directly (no chunking)")
        chunks = []
        start_time = time.time()

        # Process based on file type
        if uploaded_file.name.lower().endswith('.csv'):
            for chunk in pd.read_csv(uploaded_file, chunksize=chunksize):
                chunk["Scope Status"] = chunk.iloc[:, 0].apply(classify_name)
                chunks.append(chunk)
        else:  # Excel file
            df = pd.read_excel(uploaded_file)
            df["Scope Status"] = df.iloc[:, 0].apply(classify_name)
            chunks.append(df)

        df = pd.concat(chunks, ignore_index=True) if chunks else df
        end_time = time.time()
        st.write(f"Processing time: {end_time - start_time:.2f} seconds")

        # Auto-detect name column or let user select
        name_col = next((col for col in df.columns if "name" in col.lower() or "customer" in col.lower()), None)
        if not name_col:
            name_col = st.selectbox("🔍 Select the column containing customer names:", df.columns.tolist())

        st.info(f"🔧 Using column: **{name_col}** for categorization")

        # Apply classification
        df["Scope Status"] = df[name_col].apply(classify_name)
        st.success("✅ Categorization completed successfully!")

        # Save to processed folder (local)
        if os.path.exists("processed"):
            output_path = os.path.join("processed", f"categorized_customers_{pd.Timestamp.now().strftime('%Y%m%d_%H%M')}.xlsx")
            df.to_excel(output_path, index=False)
            st.write(f"Results saved to: {output_path}")

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
