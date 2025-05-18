
import streamlit as st
from database.db import DatabaseManager
from database.models import User, Product, NGO
from logic.scanner import scan_and_check
from database.auth import AuthManager
from db_initializer import create_db

st.set_page_config(page_title="Baynah – Shop with Integrity", layout="wide")

# Enhanced CSS for dark mode, sidebar, and layout
st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"], .main, .block-container {
        background: #121212 !important;
        color: #e0e0e0 !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        color: white !important;
    }
    [data-testid="stSidebar"] .css-1v0mbdj, 
    [data-testid="stSidebar"] .css-1oe6wy7, 
    [data-testid="stSidebar"] .css-1hynsf2, 
    [data-testid="stSidebar"] .css-1d391kg {
        color: #ffffff !important;
        text-shadow: 0 0 8px #ffffffaa;
        font-weight: bold;
    }

    .title {
        font-size: 3.5rem;
        font-weight: 900;
        text-align: center;
        color: #00b894;
        margin-top: 1.5rem;
        margin-bottom: 0.2rem;
        letter-spacing: 2px;
        text-shadow: 0 0 10px #00b894aa;
        user-select: none;
    }

    .subtitle {
        font-size: 1.25rem;
        text-align: center;
        color: #a0a0a0;
        margin-bottom: 2rem;
        font-style: italic;
    }

    .stButton>button {
        background-color: #00b894;
        color: #121212;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
        transition: background-color 0.3s ease;
        border: none;
        box-shadow: 0 0 8px #00b89488;
    }
    .stButton>button:hover {
        background-color: #019875;
        color: white;
        transform: scale(1.05);
        box-shadow: 0 0 15px #019875cc;
    }

    div.stTextInput > label, div.stTextInput > div > input {
        color: #e0e0e0 !important;
        background-color: #222 !important;
        border-radius: 6px;
        border: 1px solid #00b894;
        padding: 0.4rem;
    }

    label[data-baseweb="radio"] > span:first-child {
        color: #e0e0e0 !important;
        font-weight: 600;
    }

    a {
        color: #00cec9;
        text-decoration: none;
    }
    a:hover {
        text-decoration: underline;
        color: #00b894;
    }

    footer {
        position: fixed;
        bottom: 0;
        width: 100%;
        background: #222;
        color: #888;
        text-align: center;
        padding: 0.8rem 0;
        font-size: 0.85rem;
        user-select: none;
        box-shadow: 0 -1px 5px #00b89433;
    }
    </style>
""", unsafe_allow_html=True)

create_db()
db = DatabaseManager()
user_manager = User(db)
product_manager = Product(db)
auth_manager = AuthManager()
ngo_manager = NGO(db)

if not hasattr(ngo_manager, "list_ngos"):
    def list_ngos(self):
        query = "SELECT id, name, website, country, description FROM ngos"
        return self.db.cursor.execute(query).fetchall()
    setattr(ngo_manager, "list_ngos", list_ngos.__get__(ngo_manager))

# Session Init
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""

st.markdown('<div class="title">🇵🇸 Baynah – Shop with Integrity</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Resist with awareness. Support with action.</div>', unsafe_allow_html=True)

# authenticatuon
if not st.session_state["authenticated"]:
    st.subheader("🔐 Please Login or Register to Continue")
    mode = st.radio("Choose an action:", ["Login", "Register"], horizontal=True)
    username = st.text_input("Username or Email")
    password = st.text_input("Password", type="password")
    submit = st.button("Submit")

    if submit:
        if mode == "Register":
            if username and password:
                if auth_manager.register_user(username, password):
                    st.success("✅ Registration successful. You can now login.")
                else:
                    st.error("❌ Username already exists.")
            else:
                st.warning("⚠ Please fill in both username and password.")
        else:
            if username and password:
                if auth_manager.authenticate_user(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["username"] = username
                    st.query_params["refresh"] = "true"
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials.")
            else:
                st.warning("⚠ Please fill in both username and password.")
    st.stop()

# navigation
tab = st.sidebar.radio(
    f"👋 Hello, {st.session_state['username']}! Navigate:",
    ["🏠 Home", "🔍 Scan Product", "🤝 NGOs & Donate", "📊 Dashboard", "📖 About & Impact", "🚪 Logout"]
)

# pages
if tab == "🏠 Home":
    st.header("✊ Welcome to the Movement")
    st.markdown("""
    ---
    ### 💥 What Is **بَيِّنَة**?

    **Baynah** (بَيِّنَة) is an Arabic word meaning **clear proof** or **decisive evidence**.  
    In Islamic and classical Arabic, it represents the kind of truth that cannot be ignored—justice backed by transparency. 
    Baynah is your ethical companion for resisting injustice through conscious shopping and direct support.

    ---
    ### 🧠 Why We Chose the Name

    Because this tool is not just an app—it's **a moral lens**.  
    You deserve to know the truth behind every product you buy.  
    **Baynah** reveals it. With clarity. With purpose. With integrity.

    ---
    ### 🔧 Key Features

    - 🕵️ **Product Scanner:** Instantly check if a product supports harmful regimes.
    - 🚫 **Boycott Alerts:** Avoid Israeli-affiliated brands.
    - 🤲 **Verified Donations:** Support NGOs working on the ground in Gaza.

    ---
    ### 🚀 Why It Matters

    Every purchase you *don't* make from unethical corporations is a form of protest.  
    Every dollar you donate is a lifeline.

    🕊️ Let your wallet speak truth to power.
    """)

elif tab == "🔍 Scan Product":
    st.header("🔍 Scan a Product")
    search_term = st.text_input("Enter product name, brand, or barcode")
    if st.button("Check Product"):
        if search_term.strip():
            result = scan_and_check(search_term.strip())
            if result.get("product_found"):
                st.markdown(f"**🔎 Product:** *{result['product']['product_name']}*")
                st.markdown(f"**🏷 Brand:** *{result['product']['brand']}*")
                if result["is_israeli"]:
                    st.error("🚫 This product is from an Israeli brand.")
                    if result.get("alt_product"):
                        alt = result["alt_product"]
                        st.success(f"💡 Try alternative: *{alt['product_name']}* by *{alt['brand']}*")
                    else:
                        st.info("❓ No alternative found.")
                else:
                    st.success("✅ This product is clean.")
            else:
                st.warning("⚠ Product not found.")
        else:
            st.warning("Please enter a product name or barcode.")

elif tab == "🤝 NGOs & Donate":
    st.header("🤝 Verified NGOs Supporting Gaza")
    ngos = ngo_manager.list_ngos()
    if ngos:
        for ngo_id, name, website, country, desc in ngos:
            st.subheader(f"{name} ({country})")
            st.markdown(f"🌐 [Website]({website})")
            st.markdown(desc)
            if st.button(f"💳 Donate to {name}", key=f"donate_{ngo_id}"):
                st.success(f"Mock donation processed for {name}. Thank you!")
            st.markdown("---")
    else:
        st.info("No NGOs found in database.")

elif tab == "📊 Dashboard":
    st.header("📊 Dashboard")
    st.markdown("📈 This section will show boycott impact, user statistics, and engagement in future updates.")
elif tab == "📖 About & Impact":
    st.header("📖 About Baynah & Impact of Boycotting")
    st.markdown("""
    ---
    > *“The greatest threat to justice is not cruelty, but indifference.”*  
    > – Inspired by the global solidarity movement

    ---

    ## 🌍 **Why Baynah Exists**
    We built Baynah because ethical choices should be simple and powerful.  
    Every product you scan, every NGO you support, adds a pixel to a picture of freedom.  
    Our name "**Baynah**" (بَيِّنَة) comes from Arabic, meaning **"clear evidence" or "proof."**  
    Because injustice thrives on confusion, Baynah exists to **make truth undeniable**.

    ---

    ## 🧠 **How Boycotts Work**
    - 💸 They **cut funding** to oppressive corporations.
    - 📉 They **signal mass resistance**.
    - 🌱 They **grow local alternatives**.

    ---

    ## 🤝 **Real Impact**
    > - Over 50+ NGOs curated for Gaza  
    > - Thousands of products flagged as harmful  
    > - A growing network of conscious users

    ---

    ## 🇵🇸 **In Honor of Palestine**
    > "*To exist is to resist.*" – Palestinian proverb

    The people of Palestine have endured **over 75 years of apartheid, land theft, and military occupation**.  
    But no matter the bombs or borders, they have **never surrendered their dignity**.

    ### 🧒 The Children of Gaza

    Since 2023, over **15,000 children** have been killed in Gaza.  
    They:
    - Slept in rubble.
    - Wrote their names on their arms so their bodies could be identified.
    - Asked, *"Will I become a picture too?"*

    > *"There is no safe place in Gaza."*  
    > – UN Secretary-General António Guterres

    Every time you scan a product or donate to Gaza through Baynah,  
    you're **refusing complicity and amplifying their stories**.

    ---

    ## 🕊️ Their Stories Must Live On

    - **Ahed**, age 7, wanted to be a doctor. She died holding her brother’s hand.
    - **Yazan**, 13, filmed drones with a broken phone. That clip was found beside his torn backpack.
    - **Mariam**, 10, asked her mother, *"Will I grow up or become a hashtag?"*

    **We will not let them be statistics.**

    ---

    ## 🧭 Our Ethical Compass

    Baynah is not neutral.  
    We stand against genocide, apartheid, and settler colonialism.  
    Like BDS, we use **nonviolent tools** to disrupt oppression.

    We believe:
    - Code is a weapon for justice.
    - Your wallet is a ballot.
    - Resistance lives in your choices.

    ---

    ## ✊ **Join the Resistance**
    Every act of refusal is an act of courage.  
    Choose wisely. Buy consciously. Act collectively.

    🕊️ *Let your wallet speak truth to power.*
    """)


elif tab == "🚪 Logout":
    st.session_state.clear()
    st.success("✅ Logged out successfully.")
    st.stop()

# THE END FOOTERR:)
st.markdown("""
<footer>
    Developed with ❤️ by Muqaddas Fatima | © 2025 | <a href="#">https://github.com/MuqaddasFatima24</a>
</footer>
""", unsafe_allow_html=True)
