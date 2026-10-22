import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Kayunga Farm Management System",
    page_icon="🌾",
    layout="wide"
)

# 1. Initialize Session States & Full Farm Data
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "balance" not in st.session_state:
    st.session_state.balance = 4850000

if "logs" not in st.session_state:
    st.session_state.logs = [
        {"id": 1, "date": "2026-06-02", "desc": "Nordox Copper Fungicide Application", "cat": "Coffee", "amount": -120000},
        {"id": 2, "date": "2026-07-21", "desc": "Liquid NPK 17-17-17 Spray", "cat": "Coffee", "amount": -150000},
        {"id": 3, "date": "2026-08-18", "desc": "Goat Twin Kids Birth Milestone", "cat": "Goats", "amount": 0},
        {"id": 4, "date": "2026-08-31", "desc": "Leaf-Eating Pest Insecticide Treatment", "cat": "Coffee", "amount": -85000},
        {"id": 5, "date": "2026-09-18", "desc": "Planted 20 Matooke Banana Suckers", "cat": "Bananas", "amount": -100000},
        {"id": 6, "date": "2026-10-15", "desc": "Poultry Egg Sales Batch #4", "cat": "Poultry", "amount": 320000}
    ]

if "coffee_data" not in st.session_state:
    st.session_state.coffee_data = {
        "total_trees": 789,
        "soil_fertilizer": "NPK 17-17-17",
        "foliar_spray": "24-24-20",
        "fungicide": "Nordox Copper Fungicide",
        "micronutrients": "Calcium & Boron"
    }

if "piggery_data" not in st.session_state:
    st.session_state.piggery_data = {
        "pens_active": 2,
        "feed_formula": "Fermented mixture: Broken maize, rice bran, yeast, water, and banana stalks"
    }

if "poultry_data" not in st.session_state:
    st.session_state.poultry_data = {
        "hens": 26,
        "cocks": 13,
        "status": "Active laying & brooding inventory"
    }

if "banana_data" not in st.session_state:
    st.session_state.banana_data = {
        "matooke": 43, # 23 initial + 20 added September
        "mevu": 10
    }

# 2. Modern HD Theme Injection (Dark vs Light Mode Styles)
dark_theme_css = """
<style>
    .stApp {
        background-color: #0a0e17;
        color: #f1f5f9;
        transition: background-color 0.4s ease, color 0.4s ease;
    }
    .stButton>button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border-radius: 12px;
        font-weight: 700;
        border: none;
    }
</style>
"""

light_theme_css = """
<style>
    .stApp {
        background-color: #f8fafc;
        color: #0f172a;
        transition: background-color 0.4s ease, color 0.4s ease;
    }
    .stButton>button {
        background-color: #0f172a !important;
        color: #ffffff !important;
        border-radius: 12px;
        font-weight: 700;
        border: none;
    }
</style>
"""

if st.session_state.dark_mode:
    st.markdown(dark_theme_css, unsafe_allow_html=True)
else:
    st.markdown(light_theme_css, unsafe_allow_html=True)

# 3. Sidebar Controls & Navigation
st.sidebar.title("🌾 Kayunga Farm")
st.sidebar.write("Location: Kayunga, Uganda")

# Theme Toggle Button
theme_label = "☀️ Switch to Light Mode" if st.session_state.dark_mode else "🌙 Switch to Dark Mode"
if st.sidebar.button(theme_label):
    st.session_state.dark_mode = not st.session_state.dark_mode
    st.rerun()

st.sidebar.markdown("---")
nav_selection = st.sidebar.radio("Operational Menu", [
    "Telemetry Dashboard", 
    "Coffee Plantation", 
    "Piggery Unit", 
    "Poultry & Bananas", 
    "Goat Herd Registry", 
    "Financial & Records Manager"
])

# 4. Master Passkey Security Check
MASTER_PASSKEY = "Kayunga2026!"

if not st.session_state.authenticated:
    st.markdown("## 🔒 Master Access Required")
    st.write("Enter the master passkey to access secure private operational records for Kayunga Farm.")
    
    col_pass1, col_pass2 = st.columns(2)
    with col_pass1:
        entered_passkey = st.text_input("Enter Passkey", type="password")
        if st.button("Unlock System"):
            if entered_passkey == MASTER_PASSKEY:
                st.session_state.authenticated = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Incorrect Passkey. Access Denied.")
    with col_pass2:
        st.write("")
        st.write("")
        if st.button("Enter Public Demo Mode"):
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# 5. Main Content Panels with Full Farm Details
if nav_selection == "Telemetry Dashboard":
    st.title("🚀 Kayunga Farm Telemetry & Operations")
    st.write("Real-time summary metrics across all commercial agricultural assets in Kayunga, Uganda.")

    # Stat Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Coffee Plantation", value=f"{st.session_state.coffee_data['total_trees']} Trees", delta="Active NPK Protocol")
    with col2:
        st.metric(label="Piggery Unit", value=f"{st.session_state.piggery_data['pens_active']} Pens Active", delta="Fermented Maize Mix")
    with col3:
        total_poultry = st.session_state.poultry_data['hens'] + st.session_state.poultry_data['cocks']
        total_bananas = st.session_state.banana_data['matooke'] + st.session_state.banana_data['mevu']
        st.metric(label="Poultry & Crops", value=f"{total_poultry} Flock / {total_bananas} Crops", delta="Growing")
    with col4:
        current_balance = st.session_state.balance + sum([log['amount'] for log in st.session_state.logs])
        st.metric(label="Net Financial Position", value=f"UGX {current_balance:,}", delta="Operational")

    st.markdown("---")
    
    # Quick Operational Logging Hub
    st.subheader("⚡ Quick Operational Logging")
    with st.form("quick_log_form"):
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1:
            log_date = st.date_input("Date")
        with col_f2:
            log_cat = st.selectbox("Category", ["Coffee", "Piggery", "Poultry", "Bananas", "Goats", "General"])
        with col_f3:
            log_amount = st.number_input("Amount in UGX", min_value=0, step=1000)
            
        log_desc = st.text_input("Operational Description (e.g., Purchased fertilizer, Egg sales, Veterinary check)")
        
        col_inc, col_exp = st.columns(2)
        with col_inc:
            submit_income = st.form_submit_button("➕ Record Revenue")
        with col_exp:
            submit_expense = st.form_submit_button("➖ Record Expense")
            
        if submit_income and log_amount > 0:
            st.session_state.logs.append({
                "id": len(st.session_state.logs) + 1,
                "date": str(log_date),
                "desc": log_desc or "Revenue Entry",
                "cat": log_cat,
                "amount": log_amount
            })
            st.success("Revenue logged successfully!")
            st.rerun()
            
        if submit_expense and log_amount > 0:
            st.session_state.logs.append({
                "id": len(st.session_state.logs) + 1,
                "date": str(log_date),
                "desc": log_desc or "Expense Entry",
                "cat": log_cat,
                "amount": -log_amount
            })
            st.success("Expense logged successfully!")
            st.rerun()

elif nav_selection == "Coffee Plantation":
    st.title("🌱 Coffee Plantation Management")
    st.write("Detailed management protocols for your commercial coffee block.")
    
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.info(f"**Total Verified Plants:** {st.session_state.coffee_data['total_trees']} Trees")
        st.write(f"- **Soil Fertilizer:** {st.session_state.coffee_data['soil_fertilizer']}")
        st.write(f"- **Foliar Spray Formula:** {st.session_state.coffee_data['foliar_spray']}")
    with col_c2:
        st.write(f"- **Fungicide Shield:** {st.session_state.coffee_data['fungicide']}")
        st.write(f"- **Micronutrients:** {st.session_state.coffee_data['micronutrients']}")
        st.success("All spray and nutritional schedules are actively monitored.")

elif nav_selection == "Piggery Unit":
    st.title("🐖 Piggery Unit Operations")
    st.write("Dedicated housing facilities and specialized feeding protocols.")
    st.markdown(f"""
    * **Active Housing:** {st.session_state.piggery_data['pens_active']} dedicated pens.
    * **Daily Feeding Routine:** {st.session_state.piggery_data['feed_formula']}.
    * **Operational Note:** Strictly utilizes broken maize (not broken rice) combined with rice bran, yeast, water, and banana stalks for optimal fermentation and growth.
    """)

elif nav_selection == "Poultry & Bananas":
    st.title("🐔 Poultry Flock & Banana Plantations")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.subheader("Poultry Inventory")
        st.write(f"- **Hens:** {st.session_state.poultry_data['hens']}")
        st.write(f"- **Cocks:** {st.session_state.poultry_data['cocks']}")
        st.write(f"- **Total Flock:** {st.session_state.poultry_data['hens'] + st.session_state.poultry_data['cocks']} birds plus growing chicks and daily egg yields.")
    
    with col_p2:
        st.subheader("Banana Crop Inventory")
        st.write(f"- **Matooke Plants:** {st.session_state.banana_data['matooke']} (including 20 suckers added in September)")
        st.write(f"- **Mevu Plants:** {st.session_state.banana_data['mevu']}")
        st.write(f"- **Total Banana Stands:** {st.session_state.banana_data['matooke'] + st.session_state.banana_data['mevu']}")

elif nav_selection == "Goat Herd Registry":
    st.title("🐐 Livestock Goat Herd")
    st.write("Breeding pair tracking, health monitoring, and herd expansion records.")
    st.success("🌟 **Recent Milestone:** Twin goat kids born on Tuesday, August 18, 2026!")
    st.write("Herd management protocols, deworming schedules, and browsing pasture rotation are fully active.")

elif nav_selection == "Financial & Records Manager":
    st.title("📋 Financial Ledger & Records Manager")
    st.write("Review, filter, and selectively delete operational entries or incorrect logs. Your net financial balance adjusts automatically.")

    if not st.session_state.logs:
        st.info("No logs currently recorded.")
    else:
        logs_to_delete = []
        for log in st.session_state.logs:
            col_chk, col_info = st.columns([1, 10])
            with col_chk:
                if st.checkbox("", key=f"del_{log['id']}"):
                    logs_to_delete.append(log['id'])
            with col_info:
                amt_str = f"UGX {log['amount']:,}" if log['amount'] >= 0 else f"-UGX {abs(log['amount']):,}"
                st.write(f"**{log['date']}** | **[{log['cat']}]** {log['desc']} — `{amt_str}`")

        if logs_to_delete:
            if st.button("🗑️ Delete Selected Records", type="primary"):
                st.session_state.logs = [log for log in st.session_state.logs if log['id'] not in logs_to_delete]
                st.success("Selected records removed successfully!")
                st.rerun()
