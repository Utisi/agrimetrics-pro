import datetime
import os
import pandas as pd
import streamlit as st

# --- PAGE CONFIGURATION & CUSTOM UI STYLING ---
st.set_page_config(
    page_title="AgriMetrics Pro | Commercial Farm Intelligence",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS injection for a sleek, modern commercial SaaS look
st.markdown("""
<style>
    /* Global styling */
    .main {
        background-color: #f8fafc;
    }
    /* Metric card styling */
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        padding: 15px 20px;
        border-radius: 12px;
        box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }
    div[data-testid="stMetric"] label {
        color: #64748b;
        font-weight: 600;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        color: #0f172a;
        font-weight: 700;
    }
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: #ffffff;
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        font-weight: 600;
        color: #1e293b;
    }
    /* Premium interaction polish */
    .stApp {
        background: radial-gradient(circle at 12% 0%, rgba(16,185,129,.08), transparent 28%),
                    linear-gradient(180deg, #f8fafc 0%, #f1f5f9 100%);
    }
    h1, h2, h3 { letter-spacing: -0.035em; }
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid rgba(16,185,129,.28);
        font-weight: 650;
        transition: transform .15s ease, box-shadow .15s ease;
    }
    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 22px rgba(16,185,129,.16);
    }
    div[data-testid="stMetric"] {
        transition: transform .18s ease, box-shadow .18s ease;
    }
    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 26px rgba(15,23,42,.09);
    }
    .save-pill {
        display:inline-block; padding:6px 11px; border-radius:999px;
        background:#dcfce7; color:#166534; font-size:12px; font-weight:700;
        border:1px solid #bbf7d0;
    }
</style>
""", unsafe_allow_html=True)

# --- MASTER ADMIN PASSKEY ---
ADMIN_PASSKEY = "Kayunga2026!"

# --- DURABLE SQLITE STORAGE ---
# Set AGRIMETRICS_DATA_DIR to a persistent mounted directory in production.
# Example: /var/lib/agrimetrics (do not use an ephemeral deployment folder).
import sqlite3
import io
import tempfile
import shutil

DATA_DIR = os.environ.get("AGRIMETRICS_DATA_DIR", os.path.abspath("agrimetrics_data"))
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "agrimetrics_pro.db")

TABLES = {
    "inventory": "inventory",
    "past_logs": "farm_logs",
    "expenses": "expenses",
    "sales": "sales",
    "tasks": "tasks",
    "losses": "losses",
    "treatments": "treatments",
    "employees": "employees",
}
EMPTY_DATA = {
    "inventory": ["Item Name", "Enterprise", "Quantity", "Unit", "Status"],
    "past_logs": ["Date", "Enterprise", "Log Details"],
    "expenses": ["Date", "Enterprise", "Description", "Cost (UGX)"],
    "sales": ["Date", "Enterprise", "Item / Produce Sold", "Quantity Sold", "Unit", "Unit Price (UGX)", "Total Revenue (UGX)", "Customer / Buyer"],
    "tasks": ["Date", "Enterprise", "Task", "Status"],
    "losses": ["Date", "Enterprise", "Item Name", "Quantity Lost", "Reason / Cause"],
    "treatments": ["Date", "Enterprise", "Medicine / Chemical Used", "Target Issue / Purpose", "Dosage / Notes", "Administered By"],
    "employees": ["Employee Name", "Role", "Daily Wage (UGX)", "Status"],
}

def db_connect():
    conn = sqlite3.connect(DB_PATH, timeout=30, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=FULL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def db_has_data():
    with db_connect() as conn:
        tables = {r[0] for r in conn.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )}
        return "inventory" in tables and conn.execute(
            "SELECT COUNT(*) FROM inventory"
        ).fetchone()[0] > 0

def load_database_into_session():
    with db_connect() as conn:
        for state_key, table in TABLES.items():
            try:
                df = pd.read_sql_query(f'SELECT * FROM "{table}"', conn)
            except (sqlite3.OperationalError, pd.errors.DatabaseError):
                df = pd.DataFrame(columns=EMPTY_DATA[state_key])
            st.session_state[state_key] = df

def save_all_data():
    """Persist live farm datasets in one SQLite transaction; demo edits stay isolated."""
    if st.session_state.get("demo_active", not st.session_state.get("logged_in", False)) and not st.session_state.get("_seed_write", False):
        st.session_state.last_saved = "Demo session · not written to live database"
        return
    try:
        with db_connect() as conn:
            for state_key, table in TABLES.items():
                df = st.session_state.get(state_key, pd.DataFrame(columns=EMPTY_DATA[state_key]))
                df.to_sql(table, conn, if_exists="replace", index=False)
            conn.execute(
                "CREATE TABLE IF NOT EXISTS app_metadata "
                "(key TEXT PRIMARY KEY, value TEXT NOT NULL)"
            )
            conn.execute(
                "INSERT OR REPLACE INTO app_metadata(key, value) VALUES (?, ?)",
                ("last_saved_utc", datetime.datetime.now(datetime.timezone.utc).isoformat()),
            )
        st.session_state.last_saved = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        st.session_state.save_error = None
    except Exception as exc:
        st.session_state.save_error = str(exc)
        raise

def make_database_backup():
    """Create a consistent SQLite snapshot, including WAL changes."""
    with db_connect() as source:
        target = sqlite3.connect(":memory:")
        source.backup(target)
        data = target.serialize()
        target.close()
    return data

# --- SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "demo_active" not in st.session_state:
    st.session_state.demo_active = True
if "current_page" not in st.session_state:
    st.session_state.current_page = "📈 Executive Dashboard"
if "last_saved" not in st.session_state:
    st.session_state.last_saved = None
if "save_error" not in st.session_state:
    st.session_state.save_error = None

def get_default_real_data():
    inv = pd.DataFrame([
        {"Item Name": "Coffee Plantation", "Enterprise": "🫘 Coffee", "Quantity": 789.0, "Unit": "Plants", "Status": "Optimal"},
        {"Item Name": "Matooke & Mevu Bananas", "Enterprise": "🍌 Bananas", "Quantity": 53.0, "Unit": "Stools", "Status": "Optimal"},
        {"Item Name": "Pigs (Breeding Stock)", "Enterprise": "🐖 Pigs", "Quantity": 2.0, "Unit": "Heads", "Status": "Active"},
        {"Item Name": "Poultry Flock (26 hens, 13 cocks, chicks)", "Enterprise": "🐔 Poultry", "Quantity": 39.0, "Unit": "Birds", "Status": "Active"},
        {"Item Name": "Goats (Adults + Twin Kids)", "Enterprise": "🐐 Goats", "Quantity": 4.0, "Unit": "Heads", "Status": "Active"},
        {"Item Name": "NPK 17-17-17 Fertilizer", "Enterprise": "🧪 Inputs", "Quantity": 2.0, "Unit": "Bags", "Status": "In Stock"},
        {"Item Name": "24-24-20 Foliar Spray", "Enterprise": "🧪 Inputs", "Quantity": 1.0, "Unit": "Litres", "Status": "In Stock"},
        {"Item Name": "Nordox Copper Fungicide", "Enterprise": "🧪 Inputs", "Quantity": 1.0, "Unit": "Packets", "Status": "In Stock"},
    ])
    logs = pd.DataFrame([
        {"Date": "2026-05-09", "Enterprise": "🐖 Pigs", "Log Details": "Acquired 2 piglets and established housing setup."},
        {"Date": "2026-06-02", "Enterprise": "🫘 Coffee", "Log Details": "Applied Nordox copper fungicide to the 789 plants."},
        {"Date": "2026-07-14", "Enterprise": "🫘 Coffee", "Log Details": "Applied Calcium and Boron root/foliar treatment."},
        {"Date": "2026-07-17", "Enterprise": "🍌 Bananas", "Log Details": "Planted 23 matooke and 10 mevu banana plants."},
        {"Date": "2026-07-21", "Enterprise": "🫘 Coffee", "Log Details": "Applied liquid NPK 17-17-17."},
        {"Date": "2026-07-28", "Enterprise": "🫘 Coffee", "Log Details": "Applied Vanol with Power Jelly."},
        {"Date": "2026-08-14", "Enterprise": "🫘 Coffee", "Log Details": "Applied Nordox copper fungicide second round."},
        {"Date": "2026-08-18", "Enterprise": "🐐 Goats", "Log Details": "Goat gave birth to twin kids successfully."},
        {"Date": "2026-08-31", "Enterprise": "🫘 Coffee", "Log Details": "Applied insecticide treatment for leaf-eating pests."},
        {"Date": "2026-09-18", "Enterprise": "🍌 Bananas", "Log Details": "Planted 20 additional matooke banana suckers."},
    ])
    exp = pd.DataFrame(columns=EMPTY_DATA["expenses"])
    sales = pd.DataFrame(columns=EMPTY_DATA["sales"])
    tasks = pd.DataFrame([
        {"Date": "2026-10-25", "Enterprise": "🫘 Coffee", "Task": "Scheduled Nordox fungicide spray & canopy check", "Status": "Pending"},
        {"Date": "2026-10-28", "Enterprise": "🐖 Pigs", "Task": "Batch fermented feed mix (Broken maize, rice bran, yeast, banana stalks)", "Status": "In Progress"},
        {"Date": "2026-11-02", "Enterprise": "🍌 Bananas", "Task": "Desuckering and organic mulching for Matooke & Mevu blocks", "Status": "Pending"},
    ])
    losses = pd.DataFrame(columns=EMPTY_DATA["losses"])
    treatments = pd.DataFrame(columns=EMPTY_DATA["treatments"])
    employees = pd.DataFrame([
        {"Employee Name": "Farm Hand 1", "Role": "General Worker", "Daily Wage (UGX)": 15000.0, "Status": "Active"},
        {"Employee Name": "Farm Supervisor", "Role": "Operations Manager", "Daily Wage (UGX)": 30000.0, "Status": "Active"}
    ])
    return inv, logs, exp, sales, tasks, losses, treatments, employees

def get_demo_data():
    inv = pd.DataFrame([
        {"Item Name": "Sample Coffee Crop", "Enterprise": "🫘 Coffee", "Quantity": 100.0, "Unit": "Plants", "Status": "Demo"},
        {"Item Name": "Demo Bananas", "Enterprise": "🍌 Bananas", "Quantity": 20.0, "Unit": "Stools", "Status": "Demo"},
    ])
    logs = pd.DataFrame([{"Date": str(datetime.date.today()), "Enterprise": "🫘 Coffee", "Log Details": "Demo Activity: Applied sample organic fertilizer."}])
    exp = pd.DataFrame(columns=EMPTY_DATA["expenses"])
    sales = pd.DataFrame(columns=EMPTY_DATA["sales"])
    tasks = pd.DataFrame([{"Date": str(datetime.date.today()), "Enterprise": "🫘 Coffee", "Task": "Sample Scheduled Spraying Task", "Status": "Pending"}])
    losses = pd.DataFrame(columns=EMPTY_DATA["losses"])
    treatments = pd.DataFrame(columns=EMPTY_DATA["treatments"])
    employees = pd.DataFrame(columns=EMPTY_DATA["employees"])
    return inv, logs, exp, sales, tasks, losses, treatments, employees

# Existing CSV data is imported once only if the SQLite store is empty.
if not db_has_data():
    legacy_csvs = {
        "inventory": "farm_inventory.csv", "past_logs": "farm_logs.csv",
        "expenses": "farm_expenses.csv", "sales": "farm_sales.csv",
        "tasks": "farm_tasks.csv", "losses": "farm_losses.csv",
        "treatments": "farm_treatments.csv", "employees": "farm_employees.csv",
    }
    legacy_found = any(os.path.exists(path) for path in legacy_csvs.values())
    if legacy_found:
        for key, path in legacy_csvs.items():
            if os.path.exists(path):
                try:
                    st.session_state[key] = pd.read_csv(path)
                except Exception:
                    st.session_state[key] = pd.DataFrame(columns=EMPTY_DATA[key])
            else:
                st.session_state[key] = pd.DataFrame(columns=EMPTY_DATA[key])
        st.session_state["_seed_write"] = True
        save_all_data()
        st.session_state["_seed_write"] = False
    else:
        # First-run store: seed with farm's initial live records once.
        initial = get_default_real_data()
        for key, df in zip(TABLES.keys(), initial):
            st.session_state[key] = df
        st.session_state["_seed_write"] = True
        save_all_data()
        st.session_state["_seed_write"] = False
        # The public, unauthenticated view remains a separate demo dataset.
        if not st.session_state.logged_in:
            demo = get_demo_data()
            for key, df in zip(TABLES.keys(), demo):
                st.session_state[key] = df

if "inventory" not in st.session_state:
    demo = get_demo_data()
    for key, df in zip(TABLES.keys(), demo):
        st.session_state[key] = df

# --- SIDEBAR LOG-IN & NAVIGATION ---
st.sidebar.image(
    "https://img.icons8.com/color/96/artificial-intelligence.png", width=50
)
st.sidebar.markdown(
    "### **AgriMetrics Pro**\n*Commercial Farm Intelligence Suite*"
)
st.sidebar.markdown("---")

# Authentication Widget in Sidebar
if not st.session_state.logged_in:
    st.sidebar.subheader("🔒 Owner Login")
    passkey_input = st.sidebar.text_input("Enter Passkey", type="password")
    if st.sidebar.button("Log In", use_container_width=True):
        if passkey_input == ADMIN_PASSKEY:
            st.session_state.logged_in = True
            st.session_state.demo_active = False
            # Login must LOAD saved records, never reset them to seed/demo values.
            load_database_into_session()
            st.sidebar.success("Welcome back! Your saved farm records are loaded.")
            st.rerun()
        else:
            st.sidebar.error("Invalid Passkey.")
else:
    st.sidebar.success("🟢 Connected to Live Kayunga Farm")
    if st.sidebar.button("Switch to Demo Mode", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.demo_active = True
        (
            st.session_state.inventory,
            st.session_state.past_logs,
            st.session_state.expenses,
            st.session_state.sales,
            st.session_state.tasks,
            st.session_state.losses,
            st.session_state.treatments,
            st.session_state.employees,
        ) = get_demo_data()
        st.rerun()

st.sidebar.markdown("---")

# Visible save status, consistent database backup, and restore controls.
if st.session_state.get("save_error"):
    st.sidebar.error("Save issue: " + str(st.session_state.save_error))
elif st.session_state.get("last_saved"):
    st.sidebar.markdown(
        f'<span class="save-pill">✓ Saved · {st.session_state.last_saved}</span>',
        unsafe_allow_html=True,
    )
else:
    st.sidebar.caption("💾 Data store ready · SQLite")

with st.sidebar.expander("🛡️ Backup & Recovery", expanded=False):
    st.caption("Download a consistent snapshot before deploying an upgrade.")
    try:
        backup_bytes = make_database_backup()
        st.download_button(
            "⬇️ Download Full Farm Backup",
            data=backup_bytes,
            file_name=f"agrimetrics_backup_{datetime.date.today().isoformat()}.db",
            mime="application/x-sqlite3",
            use_container_width=True,
        )
    except Exception as backup_exc:
        st.error(f"Backup could not be prepared: {backup_exc}")

    uploaded_backup = st.file_uploader(
        "Restore from a .db backup",
        type=["db", "sqlite", "sqlite3"],
        key="database_restore_upload",
    )
    if uploaded_backup is not None and st.button(
        "⚠️ Restore Backup (replace current records)", use_container_width=True
    ):
        try:
            candidate = sqlite3.connect(":memory:")
            candidate.deserialize(uploaded_backup.getvalue())
            required = set(TABLES.values())
            available = {row[0] for row in candidate.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
            if not required.issubset(available):
                raise ValueError("This file does not contain all AgriMetrics data tables.")
            candidate.close()
            temp_path = DB_PATH + ".restore"
            with open(temp_path, "wb") as temp_file:
                temp_file.write(uploaded_backup.getvalue())
            # Keep a safety snapshot of the current database before replacement.
            shutil.copy2(DB_PATH, DB_PATH + ".before_restore.bak")
            os.replace(temp_path, DB_PATH)
            load_database_into_session()
            st.session_state.logged_in = True
            st.session_state.demo_active = False
            st.success("Backup restored successfully.")
            st.rerun()
        except Exception as restore_exc:
            st.error(f"Restore failed: {restore_exc}")

nav_options = [
    "📈 Executive Dashboard",
    "🫘 Coffee Plantation Block",
    "🐐 Goats Enterprise",
    "🐖 Pigs Enterprise",
    "👨‍🌾 HR & Payroll Management",
    "📊 Analytics & Business Intelligence",
    "🔍 Enterprise Inspector",
    "💵 Sales & Revenue Tracker",
    "💰 Financial Ledger & Expenses",
    "📦 Asset & Inventory Control",
    "🥀 Plant & Livestock Loss Tracker",
    "💊 Self-Medication & Treatment Log",
    "📜 Operational Audit Logs",
    "🗓️ Spraying & Protocol Roadmap",
]

menu = st.sidebar.selectbox(
    "Navigation Hub",
    nav_options,
    index=nav_options.index(st.session_state.current_page) if st.session_state.current_page in nav_options else 0,
    key="nav_selectbox"
)
st.session_state.current_page = menu

# --- PUBLIC DEMO BANNER ---
if not st.session_state.logged_in:
    st.warning(
        "👋 **DEMO MODE:** You are viewing the sandbox demo version of **AgriMetrics Pro**.\n\n"
        "🔒 **To access your live farm data, enter your owner passkey in the sidebar.**"
    )

# Keep the sidebar navigation widget and the active page in sync.
def navigate_to(page_name: str) -> None:
    st.session_state.current_page = page_name
    st.session_state.nav_selectbox = page_name
    st.rerun()


# ====================================================
# 1. EXECUTIVE DASHBOARD (INTERACTIVE NAVIGATION)
# ====================================================
if menu == "📈 Executive Dashboard":
    st.title("📈 Executive Farm Dashboard")
    st.write("Real-time operational overview across farm enterprises. Click any metric card to jump to its page.")

    total_spent = (
        st.session_state.expenses["Cost (UGX)"].sum()
        if not st.session_state.expenses.empty
        else 0.0
    )
    total_revenue = (
        st.session_state.sales["Total Revenue (UGX)"].sum()
        if not st.session_state.sales.empty
        else 0.0
    )
    net_profit = total_revenue - total_spent

    coffee_row = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🫘 Coffee"
    ]
    coffee_count = (
        int(coffee_row["Quantity"].sum()) if not coffee_row.empty else 0
    )

    goats_row = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🐐 Goats"
    ]
    goats_count = int(goats_row["Quantity"].sum()) if not goats_row.empty else 0

    pigs_row = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🐖 Pigs"
    ]
    pigs_count = int(pigs_row["Quantity"].sum()) if not pigs_row.empty else 0

    emp_count = len(
        st.session_state.employees[st.session_state.employees["Status"] == "Active"]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric("Total Expenses", f"UGX {total_spent:,.0f}")
        if st.button("👉 View Ledger", key="dash_exp", use_container_width=True):
            navigate_to("💰 Financial Ledger & Expenses")

    with col2:
        st.metric("Coffee Stems Active", f"{coffee_count} Plants")
        if st.button("👉 View Coffee Block", key="dash_coffee", use_container_width=True):
            navigate_to("🫘 Coffee Plantation Block")

    with col3:
        st.metric("Goats Stock", f"{goats_count} Heads")
        if st.button("👉 View Goats Block", key="dash_goats", use_container_width=True):
            navigate_to("🐐 Goats Enterprise")

    with col4:
        st.metric("Pigs Stock", f"{pigs_count} Heads")
        if st.button("👉 View Pigs Block", key="dash_pigs", use_container_width=True):
            navigate_to("🐖 Pigs Enterprise")

    with col5:
        st.metric("Active Staff", f"{emp_count} Workers")
        if st.button("👉 View HR & Payroll", key="dash_hr", use_container_width=True):
            navigate_to("👨‍🌾 HR & Payroll Management")

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🚨 Priority Next Protocols")
        if not st.session_state.tasks.empty:
            st.dataframe(
                st.session_state.tasks, use_container_width=True, hide_index=True
            )
        else:
            st.success("All operational protocols are up to date!")

    with c2:
        st.subheader("💵 Recent Sales & Revenue Transactions")
        if not st.session_state.sales.empty:
            st.dataframe(
                st.session_state.sales.tail(5),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No sales transactions recorded yet.")

# ====================================================
# 2. COFFEE PLANTATION BLOCK
# ====================================================
elif menu == "🫘 Coffee Plantation Block":
    st.title("🫘 Coffee Enterprise Management")
    st.write("Track coffee plant population, chemical spray protocols, and coffee health records.")

    coffee_assets = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🫘 Coffee"
    ]
    coffee_qty = int(coffee_assets["Quantity"].sum()) if not coffee_assets.empty else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Coffee Plants", f"{coffee_qty} Stems")
    col2.metric("Target Soil Fertilizer", "NPK 17-17-17")
    col3.metric("Foliar Spray Standard", "24-24-20")

    st.markdown("---")
    st.subheader("🫘 Coffee Inventory")
    st.dataframe(coffee_assets, use_container_width=True, hide_index=True)

    with st.expander("➕ Click Here to Log Coffee Treatment / Activity", expanded=False):
        with st.form("coffee_log_form", clear_on_submit=True):
            c_date = st.date_input("Date", datetime.date.today())
            c_chem = st.text_input("Chemical / Treatment Used", placeholder="e.g., Nordox Copper, NPK 17-17-17, Insecticide")
            c_notes = st.text_input("Notes / Dosage", placeholder="e.g., Applied second round for leaf rust control")
            if st.form_submit_button("Save Coffee Protocol Log"):
                new_l = pd.DataFrame([{"Date": str(c_date), "Enterprise": "🫘 Coffee", "Log Details": f"Applied {c_chem}: {c_notes}"}])
                st.session_state.past_logs = pd.concat([st.session_state.past_logs, new_l], ignore_index=True)
                save_all_data()
                st.success("Coffee activity logged!")
                st.rerun()

# ====================================================
# 3. GOATS ENTERPRISE
# ====================================================
elif menu == "🐐 Goats Enterprise":
    st.title("🐐 Livestock Goats Enterprise")
    st.write("Manage goat herds, breeding pairs, newborn kids, and health logs.")

    goat_assets = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🐐 Goats"
    ]
    goat_qty = int(goat_assets["Quantity"].sum()) if not goat_assets.empty else 0

    m1, m2 = st.columns(2)
    m1.metric("Total Goat Stock", f"{goat_qty} Heads")
    m2.metric("Herd Status", "Adults + Twin Kids Active")

    st.markdown("---")
    st.subheader("📋 Goats Inventory")
    st.dataframe(goat_assets, use_container_width=True, hide_index=True)

    with st.expander("🐐 Click Here to Record Goat Birth / Inflow", expanded=False):
        with st.form("goat_inflow_form", clear_on_submit=True):
            g_date = st.date_input("Date", datetime.date.today())
            g_desc = st.text_input("Event Description", placeholder="e.g., Goat gave birth to twin kids successfully")
            g_add = st.number_input("Head Count Added", min_value=1.0, step=1.0)
            if st.form_submit_button("Record Head Count Increase"):
                idx = st.session_state.inventory[
                    st.session_state.inventory["Enterprise"] == "🐐 Goats"
                ].index
                if len(idx) > 0:
                    st.session_state.inventory.loc[idx[0], "Quantity"] += g_add
                new_l = pd.DataFrame([{"Date": str(g_date), "Enterprise": "🐐 Goats", "Log Details": g_desc}])
                st.session_state.past_logs = pd.concat([st.session_state.past_logs, new_l], ignore_index=True)
                save_all_data()
                st.success("Goat herd updated!")
                st.rerun()

# ====================================================
# 4. PIGS ENTERPRISE
# ====================================================
elif menu == "🐖 Pigs Enterprise":
    st.title("🐖 Piggery & Breeding Management")
    st.write("Track breeding pigs, housing setups, and fermented feed mixing routines.")

    pig_assets = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "🐖 Pigs"
    ]
    pig_qty = int(pig_assets["Quantity"].sum()) if not pig_assets.empty else 0

    p1, p2 = st.columns(2)
    p1.metric("Total Pigs Stock", f"{pig_qty} Heads")
    p2.metric("Standard Feed Formula", "Broken Maize + Rice Bran + Yeast + Banana Stalks")

    st.markdown("---")
    st.subheader("📋 Piggery Inventory")
    st.dataframe(pig_assets, use_container_width=True, hide_index=True)

    with st.expander("🥣 Click Here to Log Fermented Feed Batching / Pen Activity", expanded=False):
        with st.form("pig_log_form", clear_on_submit=True):
            p_date = st.date_input("Date", datetime.date.today())
            p_details = st.text_input("Log Summary", placeholder="e.g., Batched fermented feed (broken maize, rice bran, yeast, banana stalks)")
            if st.form_submit_button("Record Pig Log"):
                new_l = pd.DataFrame([{"Date": str(p_date), "Enterprise": "🐖 Pigs", "Log Details": p_details}])
                st.session_state.past_logs = pd.concat([st.session_state.past_logs, new_l], ignore_index=True)
                save_all_data()
                st.success("Piggery log saved!")
                st.rerun()

# ====================================================
# 5. HR & PAYROLL MANAGEMENT
# ====================================================
elif menu == "👨‍🌾 HR & Payroll Management":
    st.title("👨‍🌾 Human Resources & Payroll Management")
    st.write("Manage workforce records, roles, daily wage tracking, and labor expenses.")

    total_wage = (
        st.session_state.employees["Daily Wage (UGX)"].sum()
        if not st.session_state.employees.empty
        else 0.0
    )
    st.metric("Total Active Daily Payroll", f"UGX {total_wage:,.2f}")

    st.markdown("---")
    with st.expander("➕ Click Here to Register New Employee / Worker", expanded=False):
        with st.form("emp_form", clear_on_submit=True):
            col_e1, col_e2 = st.columns(2)
            with col_e1:
                e_name = st.text_input("Employee Name", placeholder="e.g., John Mukasa")
                e_role = st.selectbox(
                    "Assign Role",
                    ["Farm Hand", "Casual Worker", "Sprayer Specialist", "Supervisor", "Operations Manager"]
                )
            with col_e2:
                e_wage = st.number_input("Daily Wage Rate (UGX)", min_value=0.0, step=1000.0)
                e_status = st.selectbox("Status", ["Active", "Inactive"])

            if st.form_submit_button("Register Employee"):
                if e_name:
                    new_e = pd.DataFrame([{
                        "Employee Name": e_name,
                        "Role": e_role,
                        "Daily Wage (UGX)": e_wage,
                        "Status": e_status
                    }])
                    st.session_state.employees = pd.concat(
                        [st.session_state.employees, new_e], ignore_index=True
                    )
                    save_all_data()
                    st.success("Worker registered successfully!")
                    st.rerun()
                else:
                    st.error("Please enter an employee name.")

    st.subheader("📋 Registered Farm Workers")
    if not st.session_state.employees.empty:
        emp_disp = st.session_state.employees.copy()
        emp_disp.insert(0, "Select", False)
        edited_emp = st.data_editor(
            emp_disp,
            use_container_width=True,
            hide_index=True,
            key="emp_editor"
        )

        if st.button("🗑️ Delete Selected Employees", type="primary"):
            drop_i = edited_emp[edited_emp["Select"] == True].index
            if len(drop_i) > 0:
                st.session_state.employees = (
                    st.session_state.employees.drop(drop_i).reset_index(drop=True)
                )
                save_all_data()
                st.success("Selected employee records deleted!")
                st.rerun()
    else:
        st.info("No employee records registered yet.")

# ====================================================
# 6. ANALYTICS & BUSINESS INTELLIGENCE
# ====================================================
elif menu == "📊 Analytics & Business Intelligence":
    st.title("📊 Commercial Data Analytics & Performance Metrics")
    st.write("In-depth visual analysis, profit margins, cost centers, and report exports.")

    total_spent = (
        st.session_state.expenses["Cost (UGX)"].sum()
        if not st.session_state.expenses.empty
        else 0.0
    )
    total_revenue = (
        st.session_state.sales["Total Revenue (UGX)"].sum()
        if not st.session_state.sales.empty
        else 0.0
    )
    net_profit = total_revenue - total_spent

    st.subheader("⚡ Key Financial Ratios")
    col_m1, col_m2, col_m3, col_m4 = st.columns(4)

    margin_pct = (net_profit / total_revenue * 100) if total_revenue > 0 else 0.0
    expense_ratio = (total_spent / total_revenue * 100) if total_revenue > 0 else 0.0
    total_losses_recorded = len(st.session_state.losses)
    total_treatments = len(st.session_state.treatments)

    col_m1.metric("Gross Profit Margin", f"{margin_pct:.1f}%")
    col_m2.metric("Expense-to-Revenue Ratio", f"{expense_ratio:.1f}%")
    col_m3.metric("Incidents & Losses Recorded", f"{total_losses_recorded} Events")
    col_m4.metric("Treatments Administered", f"{total_treatments} Protocols")

    st.markdown("---")

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("💸 Expense Distribution by Enterprise")
        if not st.session_state.expenses.empty:
            exp_by_ent = (
                st.session_state.expenses.groupby("Enterprise")["Cost (UGX)"]
                .sum()
                .reset_index()
            )
            st.bar_chart(exp_by_ent, x="Enterprise", y="Cost (UGX)", use_container_width=True)
        else:
            st.info("Log expenses in the Financial Ledger to generate cost breakdown charts.")

        st.subheader("📦 Asset Inventory Distribution")
        if not st.session_state.inventory.empty:
            inv_by_ent = (
                st.session_state.inventory.groupby("Enterprise")["Quantity"]
                .sum()
                .reset_index()
            )
            st.bar_chart(inv_by_ent, x="Enterprise", y="Quantity", use_container_width=True)
        else:
            st.info("No active inventory records.")

    with col_chart2:
        st.subheader("💰 Revenue Distribution by Enterprise")
        if not st.session_state.sales.empty:
            sales_by_ent = (
                st.session_state.sales.groupby("Enterprise")["Total Revenue (UGX)"]
                .sum()
                .reset_index()
            )
            st.bar_chart(
                sales_by_ent, x="Enterprise", y="Total Revenue (UGX)", use_container_width=True
            )
        else:
            st.info("Log sales in the Sales Tracker to generate revenue breakdown charts.")

        st.subheader("⚖️ Net Cash Flow (Revenue vs Expenses)")
        cf_data = pd.DataFrame({
            "Category": ["Revenue", "Expenses"],
            "Amount (UGX)": [total_revenue, total_spent],
        })
        st.bar_chart(cf_data, x="Category", y="Amount (UGX)", use_container_width=True)

    st.markdown("---")
    st.subheader("📥 Export Data Reports for Business Keeping")
    col_exp1, col_exp2, col_exp3, col_exp4 = st.columns(4)

    with col_exp1:
        if not st.session_state.expenses.empty:
            csv_exp = st.session_state.expenses.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Expenses (CSV)", csv_exp, "expenses_report.csv", "text/csv")
    with col_exp2:
        if not st.session_state.sales.empty:
            csv_sales = st.session_state.sales.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Sales (CSV)", csv_sales, "sales_report.csv", "text/csv")
    with col_exp3:
        if not st.session_state.inventory.empty:
            csv_inv = st.session_state.inventory.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Inventory (CSV)", csv_inv, "inventory_report.csv", "text/csv")
    with col_exp4:
        if not st.session_state.past_logs.empty:
            csv_logs = st.session_state.past_logs.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Audit Logs (CSV)", csv_logs, "audit_report.csv", "text/csv")

# ====================================================
# 7. ENTERPRISE INSPECTOR
# ====================================================
elif menu == "🔍 Enterprise Inspector":
    st.title("🔍 Enterprise Drill-down Inspector")
    st.write("Select an enterprise below to inspect its history, stock levels, losses, treatments, and sales.")

    selected_ent = st.selectbox(
        "Choose Enterprise to Inspect",
        ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
    )

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.subheader(f"📦 Active Assets for {selected_ent}")
        ent_assets = st.session_state.inventory[
            st.session_state.inventory["Enterprise"] == selected_ent
        ]
        if not ent_assets.empty:
            st.dataframe(ent_assets, use_container_width=True, hide_index=True)
        else:
            st.info("No assets currently registered for this enterprise.")

        st.subheader(f"💵 Sales & Revenue for {selected_ent}")
        ent_sales = st.session_state.sales[
            st.session_state.sales["Enterprise"] == selected_ent
        ]
        if not ent_sales.empty:
            st.dataframe(ent_sales, use_container_width=True, hide_index=True)
        else:
            st.info("No sales revenue recorded for this enterprise.")

        st.subheader(f"🥀 Losses for {selected_ent}")
        ent_losses = st.session_state.losses[
            st.session_state.losses["Enterprise"] == selected_ent
        ]
        if not ent_losses.empty:
            st.dataframe(ent_losses, use_container_width=True, hide_index=True)
        else:
            st.success("No losses recorded for this enterprise!")

    with col_b:
        st.subheader(f"💊 Self-Medication for {selected_ent}")
        ent_meds = st.session_state.treatments[
            st.session_state.treatments["Enterprise"] == selected_ent
        ]
        if not ent_meds.empty:
            st.dataframe(ent_meds, use_container_width=True, hide_index=True)
        else:
            st.info("No treatments logged for this enterprise.")

        st.subheader(f"📜 Audit History for {selected_ent}")
        ent_logs = st.session_state.past_logs[
            st.session_state.past_logs["Enterprise"] == selected_ent
        ]
        if not ent_logs.empty:
            st.dataframe(ent_logs, use_container_width=True, hide_index=True)
        else:
            st.info("No historical logs found for this enterprise.")

# ====================================================
# 8. SALES & REVENUE TRACKER
# ====================================================
elif menu == "💵 Sales & Revenue Tracker":
    st.title("💵 Sales & Revenue Management (UGX)")
    st.write("Record sales of harvest, produce, milk, eggs, or livestock.")

    with st.expander("➕ Click Here to Add a New Sale Record", expanded=False):
        with st.form("sales_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                sale_date = st.date_input("Transaction Date", datetime.date.today())
                sale_ent = st.selectbox(
                    "Enterprise Category",
                    ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="sale_ent",
                )
                item_sold = st.text_input(
                    "Item / Produce Sold",
                    placeholder="e.g., Red Coffee Cherries, Matooke Bunches, Tray of Eggs",
                )
                customer = st.text_input(
                    "Customer / Buyer Name", placeholder="e.g., Local Trader, Kayunga Market Buyer"
                )

            with col2:
                sale_qty = st.number_input(
                    "Quantity Sold", min_value=0.1, step=1.0, format="%.1f"
                )
                sale_unit = st.selectbox(
                    "Unit of Measure",
                    ["KGs", "Bunches", "Trays", "Heads", "Birds", "Bags", "Litres", "Units"],
                )
                unit_price = st.number_input(
                    "Unit Price (UGX)", min_value=0.0, step=500.0, format="%.2f"
                )

            if st.form_submit_button("💰 Post Sale & Record Revenue"):
                if item_sold and sale_qty > 0 and unit_price > 0:
                    total_rev = sale_qty * unit_price
                    new_sale = pd.DataFrame({
                        "Date": [str(sale_date)],
                        "Enterprise": [sale_ent],
                        "Item / Produce Sold": [item_sold],
                        "Quantity Sold": [sale_qty],
                        "Unit": [sale_unit],
                        "Unit Price (UGX)": [unit_price],
                        "Total Revenue (UGX)": [total_rev],
                        "Customer / Buyer": [customer if customer else "Direct Cash Sale"],
                    })
                    st.session_state.sales = pd.concat(
                        [st.session_state.sales, new_sale], ignore_index=True
                    )

                    new_audit = pd.DataFrame({
                        "Date": [str(sale_date)],
                        "Enterprise": [sale_ent],
                        "Log Details": (
                            f"Sold {sale_qty} {sale_unit} of {item_sold} for UGX {total_rev:,.2f} "
                            f"to {customer if customer else 'Direct Buyer'}."
                        ),
                    })
                    st.session_state.past_logs = pd.concat(
                        [st.session_state.past_logs, new_audit], ignore_index=True
                    )
                    
                    save_all_data()
                    st.success(f"Sale recorded! Generated UGX {total_rev:,.2f} in revenue.")
                    st.rerun()
                else:
                    st.error("Please enter item name, quantity, and unit price.")

    st.markdown("### 📋 Sales & Revenue Ledger")
    if not st.session_state.sales.empty:
        sales_display = st.session_state.sales.copy()
        sales_display.insert(0, "Select", False)
        edited_sales = st.data_editor(
            sales_display,
            use_container_width=True,
            hide_index=True,
            key="sales_editor",
        )

        if st.button("🗑️ Delete Selected Sales Records", type="primary"):
            indices_to_drop = edited_sales[edited_sales["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.sales = (
                    st.session_state.sales.drop(indices_to_drop).reset_index(drop=True)
                )
                save_all_data()
                st.success("Selected sales records deleted!")
                st.rerun()
    else:
        st.info("Sales ledger is currently empty.")

# ====================================================
# 9. FINANCIAL LEDGER & EXPENSES
# ====================================================
elif menu == "💰 Financial Ledger & Expenses":
    st.title("💰 Financial Ledger & Expense Tracking (UGX)")
    st.write("Monitor input costs and enterprise expenditures.")

    with st.expander("➕ Click Here to Add a New Expense", expanded=False):
        with st.form("expense_entry_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                exp_date = st.date_input("Transaction Date", datetime.date.today())
                enterprise = st.selectbox(
                    "Enterprise Category",
                    [
                        "🫘 Coffee",
                        "🍌 Bananas",
                        "🐖 Pigs",
                        "🐔 Poultry",
                        "🐐 Goats",
                        "🧪 Chemicals & Inputs",
                        "👨‍🌾 Labor & Wages",
                        "🚜 Operations & Fuel",
                    ],
                )
            with col2:
                cost_val = st.number_input(
                    "Amount (UGX)", min_value=0.0, step=1000.0, format="%.2f"
                )
                description = st.text_input(
                    "Item Description", placeholder="e.g., 2 bags of broken maize feed"
                )

            if st.form_submit_button("💾 Post Expense"):
                new_exp = pd.DataFrame({
                    "Date": [str(exp_date)],
                    "Enterprise": [enterprise],
                    "Description": [description],
                    "Cost (UGX)": [cost_val],
                })
                st.session_state.expenses = pd.concat(
                    [st.session_state.expenses, new_exp], ignore_index=True
                )
                save_all_data()
                st.success("Expense posted!")
                st.rerun()

    st.markdown("### Expense Records")
    if not st.session_state.expenses.empty:
        exp_display = st.session_state.expenses.copy()
        exp_display.insert(0, "Select", False)
        edited_exp = st.data_editor(
            exp_display,
            use_container_width=True,
            hide_index=True,
            key="exp_editor",
        )

        if st.button("🗑️ Delete Selected Expenses", type="primary"):
            indices_to_drop = edited_exp[edited_exp["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.expenses = (
                    st.session_state.expenses.drop(indices_to_drop).reset_index(
                        drop=True
                    )
                )
                save_all_data()
                st.success("Selected expenses deleted!")
                st.rerun()
    else:
        st.info("Ledger is currently empty.")

# ====================================================
# 10. ASSET & INVENTORY CONTROL
# ====================================================
elif menu == "📦 Asset & Inventory Control":
    st.title("📦 Asset & Inventory Management")
    st.write("Track livestock counts, plant stocks, and supplies.")

    with st.expander("🌱 Click Here to Add New Stock / Livestock / Crops", expanded=False):
        with st.form("quick_inflow_form", clear_on_submit=True):
            c_in1, c_in2 = st.columns(2)
            with c_in1:
                inflow_date = st.date_input("Acquisition Date", datetime.date.today())
                inflow_ent = st.selectbox(
                    "Enterprise",
                    ["🍌 Bananas", "🫘 Coffee", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="inflow_ent",
                )
                inflow_name = st.text_input(
                    "Item / Variety Name",
                    placeholder="e.g., Matooke Suckers, Mevu Suckers",
                )
            with c_in2:
                inflow_qty = st.number_input(
                    "Quantity Added", min_value=1.0, step=1.0, format="%.1f"
                )
                inflow_unit = st.selectbox(
                    "Unit",
                    [
                        "Stools",
                        "Suckers",
                        "Plants",
                        "Heads",
                        "Birds",
                        "Bags",
                        "KGs",
                        "Litres",
                        "Packets",
                    ],
                )

            if st.form_submit_button("➕ Record New Stock Inflow"):
                if inflow_name:
                    existing_idx = st.session_state.inventory[
                        st.session_state.inventory["Item Name"].str.lower()
                        == inflow_name.lower()
                    ].index
                    if len(existing_idx) > 0:
                        current_q = st.session_state.inventory.loc[
                            existing_idx[0], "Quantity"
                        ]
                        st.session_state.inventory.loc[existing_idx[0], "Quantity"] = (
                            current_q + inflow_qty
                        )
                    else:
                        new_inv_item = pd.DataFrame({
                            "Item Name": [inflow_name],
                            "Enterprise": [inflow_ent],
                            "Quantity": [inflow_qty],
                            "Unit": [inflow_unit],
                            "Status": ["Optimal"],
                        })
                        st.session_state.inventory = pd.concat(
                            [st.session_state.inventory, new_inv_item], ignore_index=True
                        )

                    new_audit = pd.DataFrame({
                        "Date": [str(inflow_date)],
                        "Enterprise": [inflow_ent],
                        "Log Details": (
                            f"Added {int(inflow_qty)} {inflow_unit} of {inflow_name} to stock."
                        ),
                    })
                    st.session_state.past_logs = pd.concat(
                        [st.session_state.past_logs, new_audit], ignore_index=True
                    )

                    save_all_data()
                    st.success(
                        f"Added {int(inflow_qty)} {inflow_name} to stock successfully!"
                    )
                    st.rerun()
                else:
                    st.error("Please enter a name for the item or variety.")

    st.markdown("### Current Inventory Levels")
    if not st.session_state.inventory.empty:
        inv_display = st.session_state.inventory.copy()
        inv_display.insert(0, "Select", False)
        edited_inv = st.data_editor(
            inv_display,
            use_container_width=True,
            hide_index=True,
            key="inv_editor",
        )

        if st.button("🗑️ Delete Selected Assets", type="primary"):
            indices_to_drop = edited_inv[edited_inv["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.inventory = (
                    st.session_state.inventory.drop(indices_to_drop).reset_index(
                        drop=True
                    )
                )
                save_all_data()
                st.success("Selected items deleted!")
                st.rerun()
    else:
        st.info("Inventory is empty.")

# ====================================================
# 11. PLANT & LIVESTOCK LOSS TRACKER
# ====================================================
elif menu == "🥀 Plant & Livestock Loss Tracker":
    st.title("🥀 Plant Drying & Animal Mortality Tracker")
    st.write("Log dried coffee stems, diseased banana suckers, or animal mortalities with reasons.")

    with st.expander("🚨 Click Here to Record a Loss / Mortality Incident", expanded=False):
        with st.form("loss_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                loss_date = st.date_input("Date of Occurrence", datetime.date.today())
                loss_enterprise = st.selectbox(
                    "Enterprise",
                    ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="loss_ent",
                )
                item_list = st.session_state.inventory[
                    st.session_state.inventory["Enterprise"] == loss_enterprise
                ]["Item Name"].tolist()
                selected_item = (
                    st.selectbox("Select Asset / Crop Affected", item_list)
                    if item_list
                    else st.text_input("Asset / Crop Affected")
                )

            with col2:
                loss_qty = st.number_input(
                    "Quantity Lost / Dried / Died", min_value=1.0, step=1.0
                )
                loss_reason = st.text_input(
                    "Reason / Cause",
                    placeholder="e.g., Drought, Coffee wilt, Swine fever",
                )

            if st.form_submit_button("🚨 Record Loss & Automatically Deduct Stock"):
                if selected_item and loss_reason:
                    new_loss = pd.DataFrame({
                        "Date": [str(loss_date)],
                        "Enterprise": [loss_enterprise],
                        "Item Name": [selected_item],
                        "Quantity Lost": [loss_qty],
                        "Reason / Cause": [loss_reason],
                    })
                    st.session_state.losses = pd.concat(
                        [st.session_state.losses, new_loss], ignore_index=True
                    )

                    idx = st.session_state.inventory[
                        st.session_state.inventory["Item Name"] == selected_item
                    ].index
                    if len(idx) > 0:
                        curr_qty = st.session_state.inventory.loc[idx[0], "Quantity"]
                        st.session_state.inventory.loc[idx[0], "Quantity"] = max(
                            0.0, curr_qty - loss_qty
                        )

                    new_log = pd.DataFrame({
                        "Date": [str(loss_date)],
                        "Enterprise": [loss_enterprise],
                        "Log Details": (
                            f"Lost {int(loss_qty)} of {selected_item} due to: {loss_reason}."
                        ),
                    })
                    st.session_state.past_logs = pd.concat(
                        [st.session_state.past_logs, new_log], ignore_index=True
                    )

                    save_all_data()
                    st.success(
                        f"Recorded loss of {int(loss_qty)} {selected_item}! Stock level adjusted."
                    )
                    st.rerun()
                else:
                    st.error("Please enter/select an affected item and give a reason.")

    st.markdown("### 📋 Recorded Losses Ledger")
    if not st.session_state.losses.empty:
        loss_display = st.session_state.losses.copy()
        loss_display.insert(0, "Select", False)
        edited_loss = st.data_editor(
            loss_display,
            use_container_width=True,
            hide_index=True,
            key="loss_editor",
        )

        if st.button("🗑️ Delete Selected Loss Records", type="primary"):
            indices_to_drop = edited_loss[edited_loss["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.losses = (
                    st.session_state.losses.drop(indices_to_drop).reset_index(drop=True)
                )
                save_all_data()
                st.success("Selected loss records erased!")
                st.rerun()
    else:
        st.info("No losses recorded yet.")

# ====================================================
# 12. SELF-MEDICATION & TREATMENT LOG
# ====================================================
elif menu == "💊 Self-Medication & Treatment Log":
    st.title("💊 Self-Medication & Chemical Treatment Log")
    st.write("Record all internal treatments, sprays, and medicines used.")

    with st.expander("💊 Click Here to Add a New Medication / Treatment Record", expanded=False):
        with st.form("med_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                med_date = st.date_input("Treatment Date", datetime.date.today())
                med_enterprise = st.selectbox(
                    "Enterprise",
                    ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="med_ent",
                )
                med_name = st.text_input(
                    "Medicine / Fungicide / Chemical Used",
                    placeholder="e.g., Nordox Copper, Dewormer, Oxytetracycline",
                )
            with col2:
                med_purpose = st.text_input(
                    "Target Issue / Purpose", placeholder="e.g., Coffee rust, Deworming"
                )
                med_dosage = st.text_input(
                    "Dosage / Mixing Ratio", placeholder="e.g., 50g per 20L sprayer"
                )

            if st.form_submit_button("💾 Save Treatment Record"):
                if med_name and med_purpose:
                    new_med = pd.DataFrame({
                        "Date": [str(med_date)],
                        "Enterprise": [med_enterprise],
                        "Medicine / Chemical Used": [med_name],
                        "Target Issue / Purpose": [med_purpose],
                        "Dosage / Notes": [med_dosage],
                        "Administered By": ["Self / Internal"],
                    })
                    st.session_state.treatments = pd.concat(
                        [st.session_state.treatments, new_med], ignore_index=True
                    )

                    new_log = pd.DataFrame({
                        "Date": [str(med_date)],
                        "Enterprise": [med_enterprise],
                        "Log Details": (
                            f"Administered {med_name} for {med_purpose} ({med_dosage})."
                        ),
                    })
                    st.session_state.past_logs = pd.concat(
                        [st.session_state.past_logs, new_log], ignore_index=True
                    )

                    save_all_data()
                    st.success("Treatment record saved!")
                    st.rerun()

    st.markdown("### 📋 Treatment History")
    if not st.session_state.treatments.empty:
        treat_display = st.session_state.treatments.copy()
        treat_display.insert(0, "Select", False)
        edited_treat = st.data_editor(
            treat_display,
            use_container_width=True,
            hide_index=True,
            key="treat_editor",
        )

        if st.button("🗑️ Delete Selected Treatment Records", type="primary"):
            indices_to_drop = edited_treat[edited_treat["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.treatments = (
                    st.session_state.treatments.drop(indices_to_drop).reset_index(
                        drop=True
                    )
                )
                save_all_data()
                st.success("Selected records deleted!")
                st.rerun()
    else:
        st.info("No medication records logged yet.")

# ====================================================
# 13. OPERATIONAL AUDIT LOGS
# ====================================================
elif menu == "📜 Operational Audit Logs":
    st.title("📜 Enterprise Audit Trail")
    st.write("Chronological ledger of farm activities and milestones.")

    with st.expander("➕ Click Here to Add a New Activity Log", expanded=False):
        with st.form("new_audit_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                log_date = st.date_input("Date", datetime.date.today())
                log_enterprise = st.selectbox(
                    "Enterprise",
                    ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="audit_ent",
                )
            with col_b:
                log_details = st.text_input(
                    "Activity Summary", placeholder="e.g., Planted suckers, harvested"
                )

            if st.form_submit_button("Record Audit Entry"):
                new_entry = pd.DataFrame({
                    "Date": [str(log_date)],
                    "Enterprise": [log_enterprise],
                    "Log Details": [log_details],
                })
                st.session_state.past_logs = pd.concat(
                    [st.session_state.past_logs, new_entry], ignore_index=True
                )
                save_all_data()
                st.success("Activity logged!")
                st.rerun()

    st.markdown("### 📋 Activity Records")
    if not st.session_state.past_logs.empty:
        df_display = st.session_state.past_logs.copy()
        df_display.insert(0, "Select", False)
        edited_df = st.data_editor(
            df_display,
            use_container_width=True,
            hide_index=True,
            key="audit_editor",
        )

        if st.button("🗑️ Delete Selected Audit Logs", type="primary"):
            indices_to_drop = edited_df[edited_df["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.past_logs = (
                    st.session_state.past_logs.drop(indices_to_drop).reset_index(
                        drop=True
                    )
                )
                save_all_data()
                st.success("Selected logs deleted!")
                st.rerun()
    else:
        st.info("No operational logs recorded.")

# ====================================================
# 14. SPRAYING & PROTOCOL ROADMAP
# ====================================================
elif menu == "🗓️ Spraying & Protocol Roadmap":
    st.title("🗓️ Spraying Schedule & Operational Roadmap")
    st.write("Manage biological treatments and spraying routines.")

    with st.expander("📅 Click Here to Schedule a New Task / Protocol", expanded=False):
        with st.form("task_add_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                task_date = st.date_input("Target Date", datetime.date.today())
                enterprise = st.selectbox(
                    "Enterprise",
                    ["🫘 Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
                    key="task_ent",
                )
            with col2:
                task_desc = st.text_input(
                    "Protocol / Task Specification",
                    placeholder="e.g., Apply Nordox fungicide, Mix fermented feed",
                )
                task_status = st.selectbox(
                    "Execution Status", ["Pending", "In Progress", "Completed"]
                )

            if st.form_submit_button("📅 Schedule Protocol"):
                new_task = pd.DataFrame({
                    "Date": [str(task_date)],
                    "Enterprise": [enterprise],
                    "Task": [task_desc],
                    "Status": [task_status],
                })
                st.session_state.tasks = pd.concat(
                    [st.session_state.tasks, new_task], ignore_index=True
                )
                save_all_data()
                st.success("Protocol scheduled!")
                st.rerun()

    st.markdown("### 📋 Protocol Tasks")
    if not st.session_state.tasks.empty:
        task_display = st.session_state.tasks.copy()
        task_display.insert(0, "Select", False)
        edited_task = st.data_editor(
            task_display,
            use_container_width=True,
            hide_index=True,
            key="task_editor",
        )

        if st.button("🗑️ Delete Selected Tasks", type="primary"):
            indices_to_drop = edited_task[edited_task["Select"] == True].index
            if len(indices_to_drop) > 0:
                st.session_state.tasks = (
                    st.session_state.tasks.drop(indices_to_drop).reset_index(
                        drop=True
                    )
                )
                save_all_data()
                st.success("Selected tasks deleted!")
                st.rerun()
    else:
        st.info("No active tasks found.")
