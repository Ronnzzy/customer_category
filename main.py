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
    non_individual_keywords = sorted(list(set([
        
    "ACHYUT", "ACADEMIC", "ACCELERATOR", "ACCOUNTS", "ADMIN", "ADMINISTRATION", "ADULT", "ADVISORY",
    "ADVISORS", "AG", "AGENCY", "ALLIANCE", "APOTHECARY", "APS", "ASSOCIATES", "ASSOCIATION", "ASOCIACION",
    "AS", "A/S", "BANK", "BIO-TECHNE", "BIOTECH", "BOARD", "BORAD", "BTP", "BUREAU", "BV", "CABINET",
    "CAPITAL", "CARDIO", "CARDIOFRONT", "CARE", "CENTER", "CENTRE", "CHAMBER", "CIF", "CIVIL", "CLEVELAND",
    "CLINIC", "CLUB", "CO", "CO.", "COALITION", "COLLEGE", "COLLEGES", "COMMERCE", "COMMITTEE", "COMM",
    "COMMUNITY", "COMPANY", "COMMERCE", "COMMITTEE", "CONSORTIUM", "CONSULATE", "CONSULTANTS", "CONSULTING",
    "CONVENT", "CORP", "CORPORATION", "CORPORATIVO", "COUNSEL", "COUNCIL", "COUNTY", "CTR", "DENTA", "DENTAL",
    "DENTISTRY", "DEPARTMENT", "DEPT", "DEVELOPMENT", "DISPENSARY", "DISTRIBUTION", "DISTRIBUTORS", "DITE",
    "DIVISION", "DOS", "DOTT.", "DRUGSTORE", "E.R.L.", "EDU", "EDUCATION", "EDUCATIONAL", "EMBASSY", "ENTERPRISE",
    "ENTERPRISES", "ENVIRONMENT", "EUROPE", "EURL", "FACULTY", "FEDERATION", "FINANCE", "FONDA", "FONDATION",
    "FOREST", "FOUNDATION", "FUND", "FUNDA", "GABINET", "GMBH", "GLOBAL", "GOVERNMENT", "GOVT", "GRAND", "GROUP",
    "HEALTH", "HEALTHCARE", "HLTH", "HOLDINGS", "HOME", "HOMEMED", "HOPITAL", "HOSPITAL", "HOSPITALITY", "IES",
    "IES TORRE VICEN", "IFSI", "INC", "INC.", "INCUBATOR", "INDUSTRIES", "INITIATIVE", "INSURANCE", "INST",
    "INSTITUTE", "INSTITUTION", "INNOVATION", "INTERNATIONAL", "INTL", "INVESTIGATION", "IPSB", "KK", "KFT",
    "LABO", "LABORATORY", "LAKE", "L.L.C.", "LIBRARY", "LIMITED", "LLC", "LLP", "LOGISTICS", "LOIRE", "LTD",
    "LTD.", "MANAGEMENT", "MARKET", "MED", "MEDCOR", "MEDICAL", "MEDICINE", "MEDISIZE", "MEDTECH", "MENT",
    "MENTAL", "METRO", "METROPOLITANO", "MINISTRY", "MNTL", "NETWORK", "NETWORKING", "N.G.O", "NGO", "NIGUARDA",
    "NOIRLAB", "NON-PROFIT", "NORD", "NV", "OFFICE", "OPTIMAL", "ORGANIZATION", "OSTEOPATHIC", "OUTLET", "OY",
    "PARTNERS", "PARTNERSHIP", "PAYABLE", "PERSONAL", "PETCARE", "PHARMA", "PHARMACEUTICAL", "PHARMACEUTICALS",
    "PHARMACY", "PHYSICAL", "PHYSIO", "PL", "PL.", "PLC", "PPE", "PTE", "PVT", "PUBLISHER", "PUBLISHING", "PT",
    "PTY LTD", "R&D", "RESEARCH", "RESOURCE", "RETAIL", "S.A", "S.A.R", "S.A.S", "SA", "SANTE", "SAR", "SAS",
    "SCHOOL", "SDN", "SECRETARIAT", "SE", "SERVICES", "SHOP", "SITE", "SL", "SOCIO", "SOCIETY", "SOLUTIONS",
    "SRO", "STATE", "STORE", "SUPPLY", "SYNDICATE", "TASKFORCE", "TECH", "TECHNOLOGY", "TECNICAS", "TEAM",
    "THERAPEUTICS", "THERAPEUTIC", "TORRE", "TRADE", "TRADING", "TRAVAIL", "TRUST", "UNIV", "UNIVERSITY",
    "UNLIMITED", "URBAN", "VALLEY", "VENTURE", "VENTURES", "VICENS", "UNIT", "UNION", "UNIT", "USA", "OFFICE",
    "OPTIMAL", "SCTD", "SRL", "S.R.L", "SP ZOO", "STATE", "TEAM", "TECH", "TECHNOLOGY", "TORRE", "TRUST", 
    "UNIV", "UNIVERSITY", "VENTURE", "VENTURES", "VICENS", "WORK", "IES TORRE VICEN", "ICO", "PHYSIO",
    ])))
    
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
