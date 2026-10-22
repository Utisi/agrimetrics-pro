import streamlit as st

# Page Configuration
st.set_page_config(
    page_title="Kayunga Farm Management System",
    page_icon="🌾",
    layout="wide"
)

# 1. Initialize Session States
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "balance" not in st.session_state:
    st.session_state.balance = 4850000
if "logs" not in st.session_state:
    st.session_state.logs = [
        {"id": 1, "date": "2026-08-31", "desc": "Insecticide Spray Treatment", "cat": "Coffee Plantation", "amount": -150000},
        {"id": 2, "date": "2026-09-18", "desc": "Planted 20 Matooke Suckers", "cat": "Bananas", "amount": -80000},
        {"id": 3, "date": "2026-10-15", "desc": "Egg Sales Batch #4", "cat": "Poultry", "amount": 320000}
    ]

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
nav_selection = st.sidebar.radio("Navigation Menu", [
    "Dashboard", 
    "Coffee (789 Trees)", 
    "Piggery Unit", 
    "Poultry & Bananas", 
    "Goat Herd", 
    "Manage & Delete Records"
])

# 4. Master Passkey Security Check
MASTER_PASSKEY = "Kayunga2026!"

if not st.session_state.authenticated:
    st.markdown("## 🔒 Master Access Required")
    st.write("Enter the passkey to view private records for Kayunga Farm, or use Public Demo Mode.")
    
    col1, col2 = st.columns(2)
    with col1:
        entered_passkey = st.text_input("Enter Passkey", type="password")
        if st.button("Unlock System"):
            if entered_passkey == MASTER_PASSKEY:
                st.session_state.authenticated = True
                st.success("Access Granted!")
                st.rerun()
            else:
                st.error("Incorrect Passkey. Access Denied.")
    with col2:
        st.write("")
        st.write("")
        if st.button("Enter Public Demo Mode"):
            st.session_state.authenticated = True
            st.rerun()
    st.stop()

# 5. Main Content Panels
if nav_selection == "Dashboard":
    st.title("🚀 Kayunga Farm Telemetry Dashboard")
    st.write("Welcome back, manager. Real-time operational metrics across your agricultural assets.")

    # Stat Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Coffee Plantation", value="789 Trees", delta="NPK 17-17-17")
    with col2:
        st.metric(label="Piggery Unit", value="2 Pens", delta="Fermented Maize Mix")
    with col3:
        st.metric(label="Poultry & Bananas", value="39 Head / 53 Crops", delta="26 Hens | 13 Cocks")
    with col4:
        # Calculate active balance
        current_balance = st.session_state.balance + sum([log['amount'] for log in st.session_state.logs])
        st.metric(label="Financial Balance", value=f"UGX {current_balance:,}", delta="Operational")

    st.markdown("---")
    
    # Quick Logging Hub
    st.subheader("⚡ Quick Operational Logging")
    with st.form("quick_log_form"):
        log_desc = st.text_input("Description (e.g. Sold eggs, Spray treatment)")
        log_amount = st.number_input("Amount in UGX", min_value=0, step=1000)
        
        col_inc, col_exp = st.columns(2)
        with col_inc:
            submit_income = st.form_submit_button("➕ Add Revenue")
        with col_exp:
            submit_expense = st.form_submit_button("➖ Add Expense")
            
        if submit_income and log_amount > 0:
            st.session_state.logs.append({
                "id": len(st.session_state.logs) + 1,
                "date": "2026-10-22",
                "desc": log_desc or "Revenue Entry",
                "cat": "General",
                "amount": log_amount
            })
            st.success("Revenue logged successfully!")
            st.rerun()
            
        if submit_expense and log_amount > 0:
            st.session_state.logs.append({
                "id": len(st.session_state.logs) + 1,
                "date": "2026-10-22",
                "desc": log_desc or "Expense Entry",
                "cat": "General",
                "amount": -log_amount
            })
            st.success("Expense logged successfully!")
            st.rerun()

elif nav_selection == "Coffee (789 Trees)":
    st.title("🌱 Coffee Plantation Protocols")
    st.write("Managing your dedicated commercial coffee block.")
    st.info("**Total Purchased Plants:** 789 Trees")
    st.write("- **Soil Fertilizer:** NPK 17-17-17")
    st.write("- **Foliar Spray Code:** 24-24-20")
    st.write("- **Protection Shield:** Nordox Copper Fungicide, Calcium, and Boron applications.")

elif nav_selection == "Piggery Unit":
    st.title("🐖 Piggery Unit Management")
    st.write("Dedicated housing and optimized feeding routines.")
    st.write("- **Feed Formula:** Fermented mixture composed of **broken maize** (not broken rice), rice bran, yeast, water, and banana stalks.")

elif nav_selection == "Poultry & Bananas":
    st.title("🐔 Poultry & Banana Plantations")
    st.write("- **Poultry Flock:** 26 Hens, 13 Cocks, plus growing chicks and egg yield records.")
    st.write("- **Banana Crops:** Matooke and Mevu plant inventories.")

elif nav_selection == "Goat Herd":
    st.title("🐐 Livestock Goat Registry")
    st.write("Breeding pair tracking and newborn monitoring.")
    st.success("Recent Milestone: Twin goat kids born on August 18, 2026!")

elif nav_selection == "Manage & Delete Records":
    st.title("📋 Operational Records & Deletion Manager")
    st.write("Select and remove any incorrect entries or old logs below. Your financial balance adjusts automatically.")

    if not st.session_state.logs:
        st.info("No logs found.")
    else:
        logs_to_delete = []
        for log in st.session_state.logs:
            col_chk, col_info = st.columns([1, 10])
            with col_chk:
                if st.checkbox("", key=f"del_{log['id']}"):
                    logs_to_delete.append(log['id'])
            with col_info:
                amt_str = f"UGX {log['amount']:,}" if log['amount'] >= 0 else f"-UGX {abs(log['amount']):,}"
                st.write(f"**{log['date']}** | {log['desc']} ({log['cat']}) — `{amt_str}`")

        if logs_to_delete:
            if st.button("🗑️ Delete Selected Entries", type="primary"):
                st.session_state.logs = [log for log in st.session_state.logs if log['id'] not in logs_to_delete]
                st.success("Selected records deleted successfully!")
                st.rerun()
