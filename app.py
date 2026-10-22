import datetime
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
        border: 1px solid #e2e8f0;
    }
</style>
""", unsafe_allow_html=True)

# --- MASTER ADMIN PASSKEY ---
ADMIN_PASSKEY = "Kayunga2026!"

# --- SESSION STATE INITIALIZATION ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# Function to load sample/demo data for public visitors
def get_demo_data():
    demo_inv = pd.DataFrame([
        {
            "Item Name": "Sample Coffee Crop",
            "Enterprise": "☕ Coffee",
            "Quantity": 100.0,
            "Unit": "Plants",
            "Status": "Demo",
        },
        {
            "Item Name": "Demo Bananas",
            "Enterprise": "🍌 Bananas",
            "Quantity": 20.0,
            "Unit": "Stools",
            "Status": "Demo",
        },
    ])
    demo_logs = pd.DataFrame([
        {
            "Date": str(datetime.date.today()),
            "Enterprise": "☕ Coffee",
            "Log Details": "Demo Activity: Applied sample organic fertilizer.",
        }
    ])
    demo_exp = pd.DataFrame(
        columns=["Date", "Enterprise", "Description", "Cost (UGX)"]
    )
    demo_tasks = pd.DataFrame([
        {
            "Date": str(datetime.date.today()),
            "Enterprise": "☕ Coffee",
            "Task": "Sample Scheduled Spraying Task",
            "Status": "Pending",
        }
    ])
    return demo_inv, demo_logs, demo_exp, demo_tasks

# Function to load your REAL private farm data
def get_real_farm_data():
    real_inv = pd.DataFrame([
        {
            "Item Name": "Coffee Plantation",
            "Enterprise": "☕ Coffee",
            "Quantity": 789.0,
            "Unit": "Plants",
            "Status": "Optimal",
        },
        {
            "Item Name": "Matooke & Mevu Bananas",
            "Enterprise": "🍌 Bananas",
            "Quantity": 53.0,
            "Unit": "Stools",
            "Status": "Optimal",
        },
        {
            "Item Name": "Pigs (Breeding Stock)",
            "Enterprise": "🐖 Pigs",
            "Quantity": 2.0,
            "Unit": "Heads",
            "Status": "Active",
        },
        {
            "Item Name": "Poultry Flock (26 hens, 13 cocks, chicks)",
            "Enterprise": "🐔 Poultry",
            "Quantity": 39.0,
            "Unit": "Birds",
            "Status": "Active",
        },
        {
            "Item Name": "Goats (Adults + Twin Kids)",
            "Enterprise": "🐐 Goats",
            "Quantity": 4.0,
            "Unit": "Heads",
            "Status": "Active",
        },
        {
            "Item Name": "NPK 17-17-17 Fertilizer",
            "Enterprise": "🧪 Inputs",
            "Quantity": 2.0,
            "Unit": "Bags",
            "Status": "In Stock",
        },
        {
            "Item Name": "24-24-20 Foliar Spray",
            "Enterprise": "🧪 Inputs",
            "Quantity": 1.0,
            "Unit": "Litres",
            "Status": "In Stock",
        },
        {
            "Item Name": "Nordox Copper Fungicide",
            "Enterprise": "🧪 Inputs",
            "Quantity": 1.0,
            "Unit": "Packets",
            "Status": "In Stock",
        },
    ])

    real_logs = pd.DataFrame([
        {
            "Date": "2026-05-09",
            "Enterprise": "🐖 Pigs",
            "Log Details": "Acquired 2 piglets and established housing setup.",
        },
        {
            "Date": "2026-06-02",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied Nordox copper fungicide to the 789 plants.",
        },
        {
            "Date": "2026-07-14",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied Calcium and Boron root/foliar treatment.",
        },
        {
            "Date": "2026-07-17",
            "Enterprise": "🍌 Bananas",
            "Log Details": "Planted 23 matooke and 10 mevu banana plants.",
        },
        {
            "Date": "2026-07-21",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied liquid NPK 17-17-17.",
        },
        {
            "Date": "2026-07-28",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied Vanol with Power Jelly.",
        },
        {
            "Date": "2026-08-14",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied Nordox copper fungicide second round.",
        },
        {
            "Date": "2026-08-18",
            "Enterprise": "🐐 Goats",
            "Log Details": "Goat gave birth to twin kids successfully.",
        },
        {
            "Date": "2026-08-31",
            "Enterprise": "☕ Coffee",
            "Log Details": "Applied insecticide treatment for leaf-eating pests.",
        },
        {
            "Date": "2026-09-18",
            "Enterprise": "🍌 Bananas",
            "Log Details": "Planted 20 additional matooke banana suckers.",
        },
    ])

    real_exp = pd.DataFrame(
        columns=["Date", "Enterprise", "Description", "Cost (UGX)"]
    )

    real_tasks = pd.DataFrame([
        {
            "Date": "2026-10-25",
            "Enterprise": "☕ Coffee",
            "Task": "Scheduled Nordox fungicide spray & canopy check",
            "Status": "Pending",
        },
        {
            "Date": "2026-10-28",
            "Enterprise": "🐖 Pigs",
            "Task": "Batch fermented feed mix (Broken maize, rice bran, yeast, banana stalks)",
            "Status": "In Progress",
        },
        {
            "Date": "2026-11-02",
            "Enterprise": "🍌 Bananas",
            "Task": "Desuckering and organic mulching for Matooke & Mevu blocks",
            "Status": "Pending",
        },
    ])
    return real_inv, real_logs, real_exp, real_tasks

# Load active session memory based on login status
if "inventory" not in st.session_state:
    if st.session_state.logged_in:
        (
            st.session_state.inventory,
            st.session_state.past_logs,
            st.session_state.expenses,
            st.session_state.tasks,
        ) = get_real_farm_data()
    else:
        (
            st.session_state.inventory,
            st.session_state.past_logs,
            st.session_state.expenses,
            st.session_state.tasks,
        ) = get_demo_data()

if "losses" not in st.session_state:
    st.session_state.losses = pd.DataFrame(
        columns=[
            "Date",
            "Enterprise",
            "Item Name",
            "Quantity Lost",
            "Reason / Cause",
        ]
    )

if "treatments" not in st.session_state:
    st.session_state.treatments = pd.DataFrame(
        columns=[
            "Date",
            "Enterprise",
            "Medicine / Chemical Used",
            "Target Issue / Purpose",
            "Dosage / Notes",
            "Administered By",
        ]
    )

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
    st.sidebar.subheader("🔒 Owner / Subscriber Login")
    passkey_input = st.sidebar.text_input("Enter Passkey", type="password")
    if st.sidebar.button("Log In", use_container_width=True):
        if passkey_input == ADMIN_PASSKEY:
            st.session_state.logged_in = True
            (
                st.session_state.inventory,
                st.session_state.past_logs,
                st.session_state.expenses,
                st.session_state.tasks,
            ) = get_real_farm_data()
            st.sidebar.success("Welcome back! Live Farm Loaded.")
            st.rerun()
        else:
            st.sidebar.error("Invalid Passkey.")
else:
    st.sidebar.success("🟢 Connected to Live Kayunga Farm")
    if st.sidebar.button("Log Out", use_container_width=True):
        st.session_state.logged_in = False
        (
            st.session_state.inventory,
            st.session_state.past_logs,
            st.session_state.expenses,
            st.session_state.tasks,
        ) = get_demo_data()
        st.rerun()

st.sidebar.markdown("---")

menu = st.sidebar.selectbox(
    "Navigation Hub",
    [
        "📈 Executive Dashboard",
        "🔍 Enterprise Inspector",
        "🥀 Plant & Livestock Loss Tracker",
        "💊 Self-Medication & Treatment Log",
        "📜 Operational Audit Logs",
        "💰 Financial Ledger & Expenses",
        "📦 Asset & Inventory Control",
        "🗓️ Spraying & Protocol Roadmap",
    ],
)

# --- PUBLIC DEMO BANNER ---
if not st.session_state.logged_in:
    st.warning(
        "👋 **PUBLIC DEMO MODE:** You are viewing the sandbox demo version of **AgriMetrics Pro**.\n\n"
        "🔒 **To access your live farm data, enter passkey `Kayunga2026!` in the sidebar.**"
    )

# ====================================================
# 1. EXECUTIVE DASHBOARD
# ====================================================
if menu == "📈 Executive Dashboard":
    st.title("📈 Executive Farm Dashboard")
    st.write("Real-time operational overview across farm enterprises.")

    total_spent = (
        st.session_state.expenses["Cost (UGX)"].sum()
        if not st.session_state.expenses.empty
        else 0.0
    )
    pending_tasks_count = len(
        st.session_state.tasks[st.session_state.tasks["Status"] != "Completed"]
    )

    coffee_row = st.session_state.inventory[
        st.session_state.inventory["Enterprise"] == "☕ Coffee"
    ]
    coffee_count = (
        int(coffee_row["Quantity"].sum()) if not coffee_row.empty else 0
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Expenses", f"UGX {total_spent:,.2f}")
    col2.metric("Assets Tracked", len(st.session_state.inventory))
    col3.metric("Coffee Stems Active", f"{coffee_count} Plants")
    col4.metric("Pending Protocols", f"{pending_tasks_count} Actions")

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
        st.subheader("💡 Recent Financial Transactions")
        if not st.session_state.expenses.empty:
            st.dataframe(
                st.session_state.expenses.tail(5),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.info("No financial records logged yet.")

# ====================================================
# 2. ENTERPRISE INSPECTOR
# ====================================================
elif menu == "🔍 Enterprise Inspector":
    st.title("🔍 Enterprise Drill-down Inspector")
    st.write(
        "Select an enterprise below to inspect its history, stock levels, losses, and treatments."
    )

    selected_ent = st.selectbox(
        "Choose Enterprise to Inspect",
        ["☕ Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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
# 3. PLANT & LIVESTOCK LOSS TRACKER
# ====================================================
elif menu == "🥀 Plant & Livestock Loss Tracker":
    st.title("🥀 Plant Drying & Animal Mortality Tracker")
    st.write(
        "Log dried coffee stems, diseased banana suckers, or animal mortalities with reasons."
    )

    with st.form("loss_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            loss_date = st.date_input("Date of Occurrence", datetime.date.today())
            loss_enterprise = st.selectbox(
                "Enterprise",
                ["☕ Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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
                st.success("Selected loss records erased!")
                st.rerun()
    else:
        st.info("No losses recorded yet.")

# ====================================================
# 4. SELF-MEDICATION & TREATMENT LOG
# ====================================================
elif menu == "💊 Self-Medication & Treatment Log":
    st.title("💊 Self-Medication & Chemical Treatment Log")
    st.write("Record all internal treatments, sprays, and medicines used.")

    with st.form("med_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            med_date = st.date_input("Treatment Date", datetime.date.today())
            med_enterprise = st.selectbox(
                "Enterprise",
                ["☕ Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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
                st.success("Selected records deleted!")
                st.rerun()
    else:
        st.info("No medication records logged yet.")

# ====================================================
# 5. OPERATIONAL AUDIT LOGS
# ====================================================
elif menu == "📜 Operational Audit Logs":
    st.title("📜 Enterprise Audit Trail")
    st.write("Chronological ledger of farm activities and milestones.")

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
                st.success("Selected logs deleted!")
                st.rerun()
    else:
        st.info("No operational logs recorded.")

    st.markdown("---")
    with st.expander("➕ Log New Activity"):
        with st.form("new_audit_form", clear_on_submit=True):
            col_a, col_b = st.columns(2)
            with col_a:
                log_date = st.date_input("Date", datetime.date.today())
                log_enterprise = st.selectbox(
                    "Enterprise",
                    ["☕ Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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
                st.success("Activity logged!")
                st.rerun()

# ====================================================
# 6. FINANCIAL LEDGER & EXPENSES
# ====================================================
elif menu == "💰 Financial Ledger & Expenses":
    st.title("💰 Financial Ledger & Expense Tracking (UGX)")
    st.write("Monitor input costs and enterprise expenditures.")

    with st.form("expense_entry_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            exp_date = st.date_input("Transaction Date", datetime.date.today())
            enterprise = st.selectbox(
                "Enterprise Category",
                [
                    "☕ Coffee",
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
                st.success("Selected expenses deleted!")
                st.rerun()
    else:
        st.info("Ledger is currently empty.")

# ====================================================
# 7. ASSET & INVENTORY CONTROL
# ====================================================
elif menu == "📦 Asset & Inventory Control":
    st.title("📦 Asset & Inventory Management")
    st.write("Track livestock counts, plant stocks, and supplies.")

    with st.expander(
        "🌱 Add New Plant Inflow / New Suckers / Livestock", expanded=True
    ):
        with st.form("quick_inflow_form", clear_on_submit=True):
            c_in1, c_in2 = st.columns(2)
            with c_in1:
                inflow_date = st.date_input("Acquisition Date", datetime.date.today())
                inflow_ent = st.selectbox(
                    "Enterprise",
                    ["🍌 Bananas", "☕ Coffee", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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

            if st.form_submit_button("➕ Record New Stock / Planting Inflow"):
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

                    st.success(
                        f"Added {int(inflow_qty)} {inflow_name} to stock successfully!"
                    )
                    st.rerun()
                else:
                    st.error("Please enter a name for the item or variety.")

    st.markdown("---")
    st.subheader("Current Inventory Levels")
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
                st.success("Selected items deleted!")
                st.rerun()
    else:
        st.info("Inventory is empty.")

# ====================================================
# 8. SPRAYING & PROTOCOL ROADMAP
# ====================================================
elif menu == "🗓️ Spraying & Protocol Roadmap":
    st.title("🗓️ Spraying Schedule & Operational Roadmap")
    st.write("Manage biological treatments and spraying routines.")

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
                st.success("Selected tasks deleted!")
                st.rerun()
    else:
        st.info("No active tasks found.")

    st.markdown("---")
    with st.expander("📅 Schedule New Protocol / Task"):
        with st.form("task_add_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                task_date = st.date_input("Target Date", datetime.date.today())
                enterprise = st.selectbox(
                    "Enterprise",
                    ["☕ Coffee", "🍌 Bananas", "🐖 Pigs", "🐔 Poultry", "🐐 Goats"],
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
                st.success("Protocol scheduled!")
                st.rerun()
