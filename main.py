import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Customer Scope Classifier", layout="wide")

# Full keyword list for non-individual detection
non_individual_keywords = sorted(list(set([
    "ACHYUT", "ACADEMIC", "ACCELERATOR", "ACCOUNTS", "ADMIN", "ADMINISTRATION", "ADULT", "ADVISORY",
    "ADVISORS", "AG", "AGENCY", "ALLIANCE", "APOTHECARY", "APS", "ASSOCIATES", "ASSOCIATION", "ASOCIACION",
    "AS", "A/S", "BANK", "BIO-TECHNE", "BIOTECH", "BOARD", "BORAD", "BTP", "BUREAU", "BV", "CABINET",
    "CAPITAL", "CARDIO", "CARDIOFRONT", "CARE", "CENTER", "CENTRE", "CHAMBER", "CIF", "CIVIL", "CLEVELAND",
    "CLINIC", "CLUB", "CO", "CO.", "COALITION", "COLLEGE", "COLLEGES", "COMMERCE", "COMMITTEE", "COMM",
    "COMMUNITY", "COMPANY", "CONSORTIUM", "CONSULATE", "CONSULTANTS", "CONSULTING", "CONVENT", "CORP",
    "CORPORATION", "CORPORATIVO", "COUNSEL", "COUNCIL", "COUNTY", "CTR", "DENTA", "DENTAL", "DENTISTRY",
    "DEPARTMENT", "DEPT", "DEVELOPMENT", "DISPENSARY", "DISTRIBUTION", "DISTRIBUTORS", "DITE", "DIVISION",
    "DOS", "DOTT.", "DRUGSTORE", "E.R.L.", "EDU", "EDUCATION", "EDUCATIONAL", "EMBASSY", "ENTERPRISE",
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
    "UNLIMITED", "URBAN", "VALLEY", "VENTURE", "VENTURES", "VICENS", "UNIT", "UNION", "USA", "WORK", "ICO"
])))

# Function to classify names
def classify_customer(name):
    if pd.isna(name):
        return "Out of Scope"
    name_upper = str(name).upper()
    for keyword in non_individual_keywords:
        if keyword in name_upper:
            return "Out of Scope"
    return "In Scope"

# Streamlit UI
st.title("📋 Customer Scope Classifier")
st.markdown("Upload an Excel file to classify customer names as **In Scope** or **Out of Scope** based on business indicators.")

uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        customer_col = st.selectbox("Select the Customer Name Column", df.columns)

        # Classify
        df["Scope Status"] = df[customer_col].apply(classify_customer)

        # Show preview
        st.success("Classification Complete ✅")
        st.dataframe(df.head(20), use_container_width=True)

        # Convert to Excel
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name="Classified Data")
        output.seek(0)

        st.download_button(
            label="📥 Download Processed File",
            data=output,
            file_name="classified_customers.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("👆 Upload an Excel file to begin.")
