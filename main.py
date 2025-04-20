import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Customer Scope Classifier", layout="wide")

# Full keyword list for non-individual detection
non_individual_keywords = sorted(list(set([
    "ACHYUT", "ACADEMIC", "ACCELERATOR", "ACCOUNTS", "ADMIN", "ADMINISTRATION", "ADULT", "ADVISORY","press","PRESS","GENERAL","SUPERIORES","FUNDACAO",
    "ADVISORS", "AGENCY", "ALLIANCE", "APOTHECARY", "APS", "ASSOCIATES", "ASSOCIATION", "ASOCIACION","ZOO","TRAINING","CENTRO","LABORATORIO","BUSINESS",
    "A/S", "BANK", "BIO-TECHNE", "BIOTECH", "BOARD", "BORAD", "BTP", "BUREAU", "CABINET","TECNOLOGICA","ART","ARTS","ESTUDIOS","INVESTIGACAO",
    "CAPITAL", "CARDIO", "CARDIOFRONT", "CARE", "CENTER", "CENTRE", "CHAMBER", "CIF", "CIVIL", "CLEVELAND","COORDENACAO","SERVICE","INDUSTRIE","SANOFI",
    "CLINIC", "CLUB", "COALITION", "COLLEGE", "COLLEGES", "COMMERCE", "COMMITTEE", "COMM","APERFEICOAMENTO","PESSOAL","FIRE","RECHERCHE","EXTENSION","AEROSPACE",
    "COMMUNITY", "COMPANY", "CONSORTIUM", "CONSULATE", "CONSULTANTS", "CONSULTING", "CONVENT", "CORP","ITALIAN","NEONATAL","RESCUE","INNOVATION",
    "CORPORATION", "CORPORATIVO", "COUNSEL", "COUNCIL", "COUNTY", "CTR", "DENTA", "DENTAL", "DENTISTRY","AMERICAN","NATAL","VERITAS","TALENT","AEROSPACE",
    "DEPARTMENT", "DEPT", "DEVELOPMENT", "DISPENSARY", "DISTRIBUTION", "DISTRIBUTORS", "DITE", "DIVISION","LEARNING","NACIONAL","ORTHO","IRCCS",
    "DOTT.", "DRUGSTORE", "E.R.L.", "EDU", "EDUCATION", "EDUCATIONAL", "EMBASSY", "ENTERPRISE","ARTISTIC","MASSAGE","DENTSPLY","FOUR MSA","corp","CORP",
    "ENTERPRISES", "ENVIRONMENT", "EUROPE", "EURL", "FACULTY", "FEDERATION", "FINANCE", "FONDA", "FONDATION","RENURSE","GROUP","IMAGING",
    "FOREST", "FOUNDATION", "FUND", "FUNDA", "GABINET", "GMBH", "GLOBAL", "GOVERNMENT", "GOVT", "GRAND", "GROUP","SOLVED","SOFTWARE","ONIRIS",
    "HEALTH", "HEALTHCARE", "HLTH", "HOLDINGS", "HOME", "HOMEMED", "HOPITAL", "HOSPITAL", "HOSPITALITY", "IES","DENTSU","SIRONA","PRENAX",
    "IES TORRE VICEN", "IFSI", "INC", "INC.", "INCUBATOR", "INDUSTRIES", "INITIATIVE", "INSURANCE", "INST",",","LLC","OMS360",
    "INSTITUTE", "INSTITUTION", "INNOVATION", "INTERNATIONAL", "INTL", "INVESTIGATION", "IPSB", "KFT","BOARD","ACAD","ENDODONTICS",
    "LABO", "LABORATORY", "LAKE", "L.L.C.", "LIBRARY", "LIMITED", "LLC", "LLP", "LOGISTICS", "LOIRE", "LTD","NAILS","BEAUTY","PARTNERS",
    "LTD.", "MANAGEMENT", "MARKET", "MEDI", "MEDCOR", "MEDICAL", "MEDICINE", "MEDISIZE", "MEDTECH", "MENT","MANAGEMENT",
    "MENTAL", "METRO", "METROPOLITANO", "MINISTRY", "MNTL", "NETWORK", "NETWORKING", "N.G.O", "NGO", "NIGUARDA","ACADEMIA","BUSINESS"
    "NOIRLAB", "NON-PROFIT", "NORD", "OFFICE", "OPTIMAL", "ORGANIZATION", "OSTEOPATHIC", "OUTLET","NURSING","SECURITY","NOUVELLES",
    "PARTNERS", "PARTNERSHIP", "PAYABLE", "PERSONAL", "PETCARE", "PHARMA", "PHARMACEUTICAL", "PHARMACEUTICALS","INDEPENDENT","INDIA",
    "PHARMACY", "PHYSICAL", "PHYSIO", "PL.", "PLC", "PPE", "PTE", "PVT", "PUBLISHER", "PUBLISHING","INTERCULT","ENERGIES",
    "PTY LTD", "R&D", "RESEARCH", "RESOURCE", "RETAIL", "S.A", "S.A.R", "S.A.S", "SANTE", "SAR", " SAS","MASSACHUSETTS",
    "SCHOOL", "SDN", "SECRETARIAT", "SERVICES", "SHOP", "SITE", "SOCIO", "SOCIETY", "SOLUTIONS",
    "SRO", "STATE", "STORE", "SUPPLY", "SYNDICATE", "TASKFORCE", "TECH", "TECHNOLOGY", "TECNICAS", "TEAM",
    "THERAPEUTICS", "THERAPEUTIC", "TORRE", "TRADE", "TRADING", "TRAVAIL", "TRUST", "UNIV", "UNIVERSITY",
    "UNLIMITED", "URBAN", "VALLEY", "VENTURE", "VENTURES", "VICENS", "UNIT", "UNION", "USA", "WORK", "ICO","SCIENCE",
    "AFGHANISTAN", "ALBANIA", "ALGERIA", "ANDORRA", "ANGOLA", "ANTIGUA AND BARBUDA", "ARGENTINA", "ARMENIA", "AUSTRALIA", "AUSTRIA", "AZERBAIJAN", "BAHAMAS",
    "BAHRAIN", "BANGLADESH", "BARBADOS", "BELARUS", "BELGIUM", "BELIZE", "BENIN", "BHUTAN", "BOLIVIA", "BOSNIA AND HERZEGOVINA", "BOTSWANA", "BRAZIL", "BRUNEI",
    "BULGARIA", "BURKINA FASO", "BURUNDI", "CABO VERDE", "CAMBODIA", "CAMEROON", "CANADA", "CENTRAL AFRICAN REPUBLIC", "CHAD", "CHILE", "CHINA", "COLOMBIA", "COMOROS",
    "CONGO, DEMOCRATIC REPUBLIC OF THE", "CONGO, REPUBLIC OF THE", "COSTA RICA", "CÔTE D'IVOIRE", "CROATIA", "CUBA", "CYPRUS", "CZECHIA", "DENMARK", "DJIBOUTI", "DOMINICA",
    "DOMINICAN REPUBLIC", "ECUADOR", "EGYPT", "EL SALVADOR", "EQUATORIAL GUINEA", "ERITREA", "ESTONIA", "ESWATINI", "ETHIOPIA", "FIJI", "FINLAND", "FRANCE", "GABON", "GAMBIA", "GEORGIA", "GERMANY", "GHANA",
    "GREECE", "GRENADA", "GUATEMALA", "GUINEA", "GUINEA-BISSAU", "GUYANA", "HAITI", "HONDURAS", "HUNGARY", "ICELAND", "INDIA", "INDONESIA", "IRAN", "IRAQ", "IRELAND", "ISRAEL",
    "ITALY", "JAMAICA", "JAPAN", "JORDAN", "KAZAKHSTAN", "KENYA", "KIRIBATI", "KOREA, NORTH", "KOREA, SOUTH", "KUWAIT", "KYRGYZSTAN", "LAOS", "LATVIA", "LEBANON", "LESOTHO", "LIBERIA", "LIBYA", "LIECHTENSTEIN",
    "LITHUANIA", "LUXEMBOURG", "MADAGASCAR", "MALAWI", "MALAYSIA", "MALDIVES", "MALI", "MALTA", "MARSHALL ISLANDS", "MAURITANIA", "MAURITIUS", "MEXICO", "MICRONESIA",
    "MOLDOVA", "MONACO", "MONGOLIA", "MONTENEGRO", "MOROCCO", "MOZAMBIQUE", "MYANMAR", "NAMIBIA", "NAURU", "NEPAL", "NETHERLANDS", "NEW ZEALAND", "NICARAGUA", "NIGER",
    "NIGERIA", "NORTH MACEDONIA", "NORWAY", "OMAN", "PAKISTAN", "PALAU", "PANAMA", "PAPUA NEW GUINEA", "PARAGUAY", "PERU", "PHILIPPINES", "POLAND", "PORTUGAL", "QATAR", "ROMANIA", "RUSSIA",
    "RWANDA", "SAINT KITTS AND NEVIS", "SAINT LUCIA", "SAINT VINCENT AND THE GRENADINES", "SAMOA", "SAN MARINO", "SAO TOME AND PRINCIPE", "SAUDI ARABIA", "SENEGAL", "SERBIA", "SEYCHELLES",
    "SIERRA LEONE", "SINGAPORE", "SLOVAKIA", "SLOVENIA", "SOLOMON ISLANDS", "SOMALIA", "SOUTH AFRICA", "SOUTH SUDAN", "SPAIN", "SRI LANKA", "SUDAN", "SURINAME", "SWEDEN", "SWITZERLAND",
    "SYRIA", "TAJIKISTAN", "TANZANIA", "THAILAND", "TIMOR-LESTE", "TOGO", "TONGA", "TRINIDAD AND TOBAGO", "TUNISIA", "TURKEY", "TURKMENISTAN", "TUVALU", "UGANDA", "UKRAINE",
    "UNITED ARAB EMIRATES", "UNITED KINGDOM", "UNITED STATES", "URUGUAY", "UZBEKISTAN", "VANUATU", "VATICAN CITY", "VENEZUELA", "VIETNAM", "YEMEN", "ZAMBIA", "ZIMBABWE","NOVACAP"
    "achyut", "academic", "accelerator", "accounts", "admin", "administration", "adult", "advisory", "press", "press", "general", "superiores", "fundacao", "advisors",
    "agency", "alliance", "apothecary", "aps", "associates", "association", "asociacion", "zoo", "training", "centro", "laboratorio", "business", "a/s", "bank",
    "bio-techne", "biotech", "board", "borad", "btp", "bureau", "bv", "cabinet", "tecnologica", "art", "arts", "estudios", "investigacao", "capital", "cardio", "cardiofront",
    "care", "center", "centre", "chamber", "cif", "civil", "cleveland", "coordenacao", "service", "industrie", "sanofi", "clinic", "club", "co.", "coalition", "college",
    "colleges", "commerce", "committee", "comm", "aperfeicoamento", "pessoal", "fire", "recherche", "extension", "community", "company", "consortium", "consulate", "consultants",
    "consulting", "convent", "corp", "italian", "neonatal", "rescue", "innovation", "corporation", "corporativo", "counsel", "council", "county", "ctr", "denta", "dental",
    "dentistry", "american", "natal", "veritas", "talent", "department", "dept", "development", "dispensary", "distribution", "distributors", "dite", "division", "learning", "nacional",
    "ortho", "dott.", "drugstore", "e.r.l.", "edu", "education", "educational", "embassy", "enterprise", "artistic", "massage", "dentsply",
    "four msa", "enterprises", "environment", "europe", "eurl", "faculty", "federation", "finance", "fonda", "fondation", "renurse", "group", "imaging", "forest", "foundation",
    "fund", "funda", "gabinet", "gmbh", "global", "government", "govt", "grand", "group", "solved", "software", "health", "healthcare", "hlth", "holdings", "home", "homemed", "hopital",
    "hospital", "hospitality", "ies", "dentsu", "sirona", "ies torre vicen", "ifsi", "inc", "inc.", "incubator", "industries", "initiative", "insurance", "inst", "llc", "oms360", "institute",
    "institution", "innovation", "international", "intl", "investigation", "ipsb", "kft", "board", "acad", "endodontics", "labo", "laboratory", "lake", "l.l.c.", "library",
    "limited", "llc", "llp", "logistics", "loire", "ltd", "nails", "beauty", "partners", "ltd.", "management", "market", "medi", "medcor", "medical", "medicine", "medisize",
    "medtech", "ment", "management", "mental", "metro", "metropolitano", "ministry", "mntl", "network", "networking", "n.g.o", "ngo", "niguarda", "academia", "business",
    "noirlab", "non-profit", "nord", "office", "optimal", "organization", "osteopathic", "outlet", "nursing", "security", "partners", "partnership", "payable", "personal",
    "petcare", "pharma", "pharmaceutical", "pharmaceuticals", "independent", "india", "pharmacy", "physical", "physio", "pl.", "plc", "ppe", "pte", "pvt", "publisher",
    "publishing", "pty ltd", "r&d", "research", "resource", "retail", "s.a", "s.a.r", "s.a.s", "sante", "sar", "sas", "massachusetts", "school", "sdn", "secretariat",
    "services", "shop", "site", "socio", "society", "solutions", "sro", "state", "store", "supply", "syndicate", "taskforce", "tech", "technology", "tecnicas", "team",
    "therapeutics", "therapeutic", "torre", "trade", "trading", "travail", "trust", "univ", "university", "unlimited", "urban", "valley", "venture", "ventures", "vicens",
    "unit", "union", "usa", "work", "ico", "science", "afghanistan", "albania", "algeria", "andorra", "angola", "antigua and barbuda", "argentina", "armenia", "australia", "austria",
    "azerbaijan", "bahamas", "bahrain", "bangladesh", "barbados", "belarus", "belgium", "belize", "benin", "bhutan", "bolivia", "bosnia and herzegovina", "botswana", "brazil",
    "brunei", "bulgaria", "burkina faso", "burundi", "cabo verde", "cambodia", "cameroon", "canada", "central african republic", "chad", "chile", "china", "colombia", "comoros",
    "congo, democratic republic of the", "congo, republic of the", "costa rica", "côte d'ivoire", "croatia", "cuba", "cyprus", "czechia", "denmark", "djibouti", "dominica", "dominican","republic",
    "ecuador", "egypt", "el salvador", "equatorial guinea", "eritrea", "estonia", "eswatini", "ethiopia", "fiji", "finland", "france", "gabon", "gambia", "georgia", "germany", "ghana",
    "greece", "grenada", "guatemala", "guinea", "guinea-bissau", "guyana", "haiti", "honduras", "hungary", "iceland", "india", "indonesia", "iran", "iraq", "ireland",
    "israel", "italy", "jamaica", "japan", "jordan", "kazakhstan", "kenya", "kiribati", "korea, north", "korea, south", "kuwait", "kyrgyzstan", "laos", "latvia", "lebanon",
    "lesotho", "liberia", "libya", "liechtenstein", "lithuania", "luxembourg", "madagascar", "malawi", "malaysia", "maldives", "mali", "malta", "marshall islands", "mauritania",
    "mauritius", "mexico", "micronesia", "moldova", "monaco", "mongolia", "montenegro", "morocco", "mozambique", "myanmar", "namibia", "nauru", "nepal", "netherlands", "new zealand",
    "nicaragua", "niger", "nigeria", "north macedonia", "norway", "oman", "pakistan", "palau", "panama", "papua new guinea", "paraguay", "peru", "philippines", "poland", "portugal",
    "qatar", "romania", "russia", "rwanda", "saint kitts and nevis", "saint lucia", "saint vincent and the grenadines", "samoa", "san marino", "sao tome and principe", "saudi arabia", "senegal",
    "serbia", "seychelles", "sierra leone", "singapore", "slovakia", "slovenia", "solomon islands", "somalia", "south africa", "south sudan", "spain", "sri lanka",
    "sudan", "suriname", "sweden", "switzerland", "syria", "tajikistan", "tanzania", "thailand", "timor-leste", "togo", "tonga", "trinidad and tobago", "tunisia",
    "turkey", "turkmenistan", "tuvalu", "uganda", "ukraine", "united arab emirates", "united kingdom", "united states", "uruguay", "uzbekistan", "vanuatu",
    "vatican city", "venezuela", "vietnam", "yemen", "zambia", "zimbabwe", "novacap"
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
