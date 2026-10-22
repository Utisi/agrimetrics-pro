<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kayunga Farm Management System</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="style.css">
</head>
<body class="dark-mode">

    <!-- Top Bar Navigation -->
    <header class="top-nav">
        <div class="brand">
            <i class="fa-solid fa-leaf brand-icon"></i>
            <div>
                <h1>KAYUNGA<span>FARM</span></h1>
                <p class="subtitle">Kayunga, Uganda • Operational Dashboard</p>
            </div>
        </div>

        <div class="header-actions">
            <!-- Dynamic HD Theme Toggle -->
            <button id="themeToggleBtn" class="glass-btn primary-btn">
                <i class="fa-solid fa-sun" id="themeIcon"></i>
                <span id="themeLabel">Light Mode</span>
            </button>

            <!-- Passkey Security Status -->
            <button id="lockStatusBtn" class="glass-btn lock-btn locked">
                <i class="fa-solid fa-lock" id="lockIcon"></i>
                <span id="lockText">Locked</span>
            </button>
        </div>
    </header>

    <div class="main-container">
        <!-- Sidebar Navigation -->
        <aside class="sidebar">
            <nav class="nav-menu">
                <button class="nav-item active" data-target="dashboard">
                    <i class="fa-solid fa-chart-line"></i> <span>Dashboard</span>
                </button>
                <button class="nav-item" data-target="coffee">
                    <i class="fa-solid fa-seedling"></i> <span>Coffee (789)</span>
                </button>
                <button class="nav-item" data-target="piggery">
                    <i class="fa-solid fa-piggy-bank"></i> <span>Piggery</span>
                </button>
                <button class="nav-item" data-target="poultry">
                    <i class="fa-solid fa-egg"></i> <span>Poultry & Bananas</span>
                </button>
                <button class="nav-item" data-target="goats">
                    <i class="fa-solid fa-cubes-stacked"></i> <span>Goat Herd</span>
                </button>
                <button class="nav-item" data-target="logs">
                    <i class="fa-solid fa-list-check"></i> <span>Manage Records</span>
                </button>
            </nav>
            <div class="sidebar-footer">
                <div class="location-badge">
                    <i class="fa-solid fa-location-dot"></i>
                    <span>Kayunga, Uganda</span>
                </div>
            </div>
        </aside>

        <!-- Main Workspace -->
        <main class="content-area">

            <!-- Security Passkey Modal -->
            <div id="authOverlay" class="auth-overlay active">
                <div class="glass-card auth-card">
                    <i class="fa-solid fa-shield-halved auth-shield"></i>
                    <h2>Master Access Required</h2>
                    <p>Enter passkey to view private records for Kayunga Farm.</p>
                    <div class="input-group">
                        <input type="password" id="passkeyInput" placeholder="Enter master passkey..." />
                        <button id="togglePassVisibility" class="icon-only-btn"><i class="fa-solid fa-eye"></i></button>
                    </div>
                    <div class="auth-buttons">
                        <button id="unlockBtn" class="action-btn glow-btn">Unlock Private Records</button>
                        <button id="demoModeBtn" class="action-btn secondary-btn">Public Demo Mode</button>
                    </div>
                    <p id="authError" class="error-msg"></p>
                </div>
            </div>

            <!-- Dashboard Overview Panel -->
            <section id="dashboard" class="panel active">
                <div class="stats-grid">
                    <div class="glass-card stat-card">
                        <div class="stat-header">
                            <i class="fa-solid fa-mug-hot stat-icon coffee-color"></i>
                            <span class="badge">Active Plantation</span>
                        </div>
                        <h3>Coffee Trees</h3>
                        <div class="stat-value">789 Plants</div>
                        <p class="stat-sub">NPK 17-17-17 / Nordox Spray</p>
                    </div>

                    <div class="glass-card stat-card">
                        <div class="stat-header">
                            <i class="fa-solid fa-piggy-bank stat-icon pig-color"></i>
                            <span class="badge">Fermented Feed</span>
                        </div>
                        <h3>Piggery Unit</h3>
                        <div class="stat-value">2 Active Pens</div>
                        <p class="stat-sub">Broken Maize & Yeast Feed</p>
                    </div>

                    <div class="glass-card stat-card">
                        <div class="stat-header">
                            <i class="fa-solid fa-feather stat-icon poultry-color"></i>
                            <span class="badge">Flock & Bananas</span>
                        </div>
                        <h3>Poultry & Crops</h3>
                        <div class="stat-value">39 Head / 53 Matooke & Mevu</div>
                        <p class="stat-sub">26 Hens | 13 Cocks</p>
                    </div>

                    <div class="glass-card stat-card">
                        <div class="stat-header">
                            <i class="fa-solid fa-vault stat-icon ugx-color"></i>
                            <span class="badge">UGX Currency</span>
                        </div>
                        <h3>Financial Status</h3>
                        <div class="stat-value" id="financialBalance">UGX 4,850,000</div>
                        <p class="stat-sub">Operational Balance</p>
                    </div>
                </div>

                <div class="dashboard-grid">
                    <div class="glass-card chart-card">
                        <div class="card-header">
                            <h3><i class="fa-solid fa-chart-area"></i> Yield & Revenue Telemetry</h3>
                        </div>
                        <div class="chart-wrapper">
                            <canvas id="yieldChart"></canvas>
                        </div>
                    </div>

                    <div class="glass-card action-hub">
                        <h3><i class="fa-solid fa-bolt"></i> Quick Operational Logging</h3>
                        <div class="quick-inputs">
                            <input type="text" id="logDescription" placeholder="Description (e.g. Sold eggs, Spray treatment)">
                            <input type="number" id="logAmount" placeholder="Amount in UGX">
                            <div class="quick-buttons">
                                <button class="pulse-btn success" id="addIncomeBtn"><i class="fa-solid fa-plus"></i> Add Revenue</button>
                                <button class="pulse-btn danger" id="addExpenseBtn"><i class="fa-solid fa-minus"></i> Add Expense</button>
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Coffee Module -->
            <section id="coffee" class="panel">
                <div class="glass-card module-card">
                    <h2><i class="fa-solid fa-seedling"></i> Coffee Management Protocols</h2>
                    <div class="module-details">
                        <div class="detail-box">
                            <h4>Total Purchased Plants</h4>
                            <p class="big-number">789 Trees</p>
                        </div>
                        <div class="detail-box">
                            <h4>Soil Fertilizer</h4>
                            <p>NPK 17-17-17</p>
                        </div>
                        <div class="detail-box">
                            <h4>Foliar Spray Formula</h4>
                            <p>24-24-20</p>
                        </div>
                        <div class="detail-box">
                            <h4>Protection Protocol</h4>
                            <p>Nordox Copper Fungicide, Calcium & Boron</p>
                        </div>
                    </div>
                </div>
            </section>

            <!-- Piggery Module -->
            <section id="piggery" class="panel">
                <div class="glass-card module-card">
                    <h2><i class="fa-solid fa-piggy-bank"></i> Piggery Unit Management</h2>
                    <p><strong>Feed Recipe:</strong> Fermented mixture of broken maize (not broken rice), rice bran, yeast, water, and banana stalks.</p>
                </div>
            </section>

            <!-- Poultry & Bananas Module -->
            <section id="poultry" class="panel">
                <div class="glass-card module-card">
                    <h2><i class="fa-solid fa-egg"></i> Poultry & Banana Plantations</h2>
                    <p><strong>Flock Inventory:</strong> 26 Hens, 13 Cocks, plus growing chicks.</p>
                    <p><strong>Banana Crops:</strong> 43 Matooke and 10 Mevu plants.</p>
                </div>
            </section>

            <!-- Goats Module -->
            <section id="goats" class="panel">
                <div class="glass-card module-card">
                    <h2><i class="fa-solid fa-cubes-stacked"></i> Livestock Goat Registry</h2>
                    <p>Breeding herd tracking including twin kids born on August 18, 2026.</p>
                </div>
            </section>

            <!-- Records & Deletion Manager Panel -->
            <section id="logs" class="panel">
                <div class="glass-card module-card">
                    <h2><i class="fa-solid fa-list-check"></i> Operational Log & Data Management</h2>
                    <p class="sub-text">Select items using checkboxes to delete or manage entries.</p>
                    <table class="log-table">
                        <thead>
                            <tr>
                                <th>Select</th>
                                <th>Date</th>
                                <th>Description</th>
                                <th>Category</th>
                                <th>Amount (UGX)</th>
                            </tr>
                        </thead>
                        <tbody id="logTableBody">
                            <!-- Injected dynamically by JavaScript -->
                        </tbody>
                    </table>
                    <button class="pulse-btn danger" id="deleteSelectedBtn"><i class="fa-solid fa-trash"></i> Delete Selected Entries</button>
                </div>
            </section>

        </main>
    </div>

    <script src="script.js"></script>
</body>
</html>
:root {
    --bg-primary: #0a0e17;
    --bg-secondary: #121826;
    --card-bg: rgba(22, 30, 46, 0.75);
    --card-border: rgba(255, 255, 255, 0.12);
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --accent-glow: #3b82f6;
    --btn-primary-bg: #3b82f6;
    --btn-primary-text: #ffffff;
    --accent-success: #10b981;
    --accent-danger: #ef4444;
    --glass-blur: blur(16px);
    --shadow-hd: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
}

body.light-mode {
    --bg-primary: #f8fafc;
    --bg-secondary: #e2e8f0;
    --card-bg: rgba(255, 255, 255, 0.85);
    --card-border: rgba(0, 0, 0, 0.08);
    --text-primary: #0f172a;
    --text-secondary: #475569;
    --accent-glow: #2563eb;
    --btn-primary-bg: #0f172a;
    --btn-primary-text: #ffffff;
    --shadow-hd: 0 10px 30px -10px rgba(0, 0, 0, 0.1);
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
    font-family: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
}

body {
    background-color: var(--bg-primary);
    color: var(--text-primary);
    min-height: 100vh;
    transition: background-color 0.4s ease, color 0.4s ease;
    overflow-x: hidden;
}

.top-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 2rem;
    background: var(--card-bg);
    backdrop-filter: var(--glass-blur);
    border-bottom: 1px solid var(--card-border);
    position: sticky;
    top: 0;
    z-index: 100;
}

.brand {
    display: flex;
    align-items: center;
    gap: 1rem;
}

.brand-icon {
    font-size: 2rem;
    color: var(--accent-success);
}

.brand h1 {
    font-size: 1.4rem;
    font-weight: 800;
}

.brand h1 span {
    color: var(--accent-glow);
}

.subtitle {
    font-size: 0.75rem;
    color: var(--text-secondary);
}

.header-actions {
    display: flex;
    gap: 1rem;
}

.glass-btn {
    display: inline-flex;
    align-items: center;
    gap: 0.6rem;
    padding: 0.6rem 1.2rem;
    border-radius: 12px;
    border: 1px solid var(--card-border);
    background: var(--card-bg);
    color: var(--text-primary);
    font-weight: 600;
    cursor: pointer;
    backdrop-filter: var(--glass-blur);
    transition: all 0.2s ease;
    box-shadow: var(--shadow-hd);
}

.glass-btn:hover {
    transform: translateY(-2px);
    border-color: var(--accent-glow);
}

.glass-btn:active {
    transform: translateY(1px);
}

.primary-btn {
    background: var(--btn-primary-bg);
    color: var(--btn-primary-text);
}

.main-container {
    display: flex;
    min-height: calc(100vh - 75px);
}

.sidebar {
    width: 260px;
    background: var(--card-bg);
    backdrop-filter: var(--glass-blur);
    border-right: 1px solid var(--card-border);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 1.5rem 1rem;
}

.nav-menu {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
}

.nav-item {
    display: flex;
    align-items: center;
    gap: 1rem;
    padding: 0.9rem 1.2rem;
    border-radius: 12px;
    border: none;
    background: transparent;
    color: var(--text-secondary);
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s ease;
    text-align: left;
}

.nav-item:hover, .nav-item.active {
    background: var(--btn-primary-bg);
    color: var(--btn-primary-text);
}

.content-area {
    flex: 1;
    padding: 2rem;
    position: relative;
    overflow-y: auto;
}

.glass-card {
    background: var(--card-bg);
    backdrop-filter: var(--glass-blur);
    border: 1px solid var(--card-border);
    border-radius: 20px;
    padding: 1.5rem;
    box-shadow: var(--shadow-hd);
    margin-bottom: 1.5rem;
}

.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.stat-value {
    font-size: 1.6rem;
    font-weight: 800;
    margin: 0.4rem 0;
}

.badge {
    background: rgba(16, 185, 129, 0.2);
    color: var(--accent-success);
    padding: 0.2rem 0.6rem;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 700;
}

.panel {
    display: none;
}

.panel.active {
    display: block;
}

.auth-overlay {
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: rgba(10, 14, 23, 0.85);
    backdrop-filter: blur(20px);
    display: none;
    justify-content: center;
    align-items: center;
    z-index: 500;
}

.auth-overlay.active {
    display: flex;
}

.auth-card {
    width: 100%;
    max-width: 400px;
    text-align: center;
}

.auth-shield {
    font-size: 3rem;
    color: var(--accent-glow);
    margin-bottom: 1rem;
}

.input-group {
    display: flex;
    margin: 1.5rem 0;
    background: var(--bg-secondary);
    border-radius: 12px;
    border: 1px solid var(--card-border);
    overflow: hidden;
}

.input-group input {
    flex: 1;
    padding: 0.8rem 1rem;
    border: none;
    background: transparent;
    color: var(--text-primary);
    outline: none;
}

.action-btn, .pulse-btn {
    padding: 0.8rem 1.2rem;
    border-radius: 12px;
    border: none;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.2s ease;
}

.pulse-btn.success { background: var(--accent-success); color: #fff; }
.pulse-btn.danger { background: var(--accent-danger); color: #fff; }

.quick-inputs {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    margin-top: 1rem;
}

.quick-inputs input {
    padding: 0.8rem;
    border-radius: 10px;
    border: 1px solid var(--card-border);
    background: var(--bg-secondary);
    color: var(--text-primary);
}

.log-table {
    width: 100%;
    border-collapse: collapse;
    margin: 1.5rem 0;
}

.log-table th, .log-table td {
    padding: 0.8rem;
    text-align: left;
    border-bottom: 1px solid var(--card-border);
}

@media (max-width: 900px) {
    .main-container { flex-direction: column; }
    .sidebar { width: 100%; border-right: none; }
    .nav-menu { flex-direction: row; overflow-x: auto; }
    .nav-item span { display: none; }
}
document.addEventListener('DOMContentLoaded', () => {

    // 1. Initial Data Store (Preserving All User Inputs)
    let initialBalance = 4850000;
    let logs = [
        { id: 1, date: '2026-08-31', desc: 'Insecticide Spray Treatment', cat: 'Coffee Plantation', amount: -150000 },
        { id: 2, date: '2026-09-18', desc: 'Planted 20 Matooke Suckers', cat: 'Bananas', amount: -80000 },
        { id: 3, date: '2026-10-15', desc: 'Egg Sales Batch #4', cat: 'Poultry', amount: 320000 }
    ];

    // 2. Dynamic Theme Morphing
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeIcon = document.getElementById('themeIcon');
    const themeLabel = document.getElementById('themeLabel');

    themeToggleBtn.addEventListener('click', () => {
        document.body.classList.toggle('light-mode');
        const isLight = document.body.classList.contains('light-mode');
        themeIcon.className = isLight ? 'fa-solid fa-moon' : 'fa-solid fa-sun';
        themeLabel.textContent = isLight ? 'Dark Mode' : 'Light Mode';
        updateChartColors(isLight);
    });

    // 3. Navigation
    const navItems = document.querySelectorAll('.nav-item');
    const panels = document.querySelectorAll('.panel');

    navItems.forEach(item => {
        item.addEventListener('click', () => {
            navItems.forEach(nav => nav.classList.remove('active'));
            panels.forEach(panel => panel.classList.remove('active'));
            item.classList.add('active');
            document.getElementById(item.getAttribute('data-target')).classList.add('active');
        });
    });

    // 4. Passkey Authentication
    const authOverlay = document.getElementById('authOverlay');
    const unlockBtn = document.getElementById('unlockBtn');
    const passkeyInput = document.getElementById('passkeyInput');
    const authError = document.getElementById('authError');
    const demoModeBtn = document.getElementById('demoModeBtn');
    const lockStatusBtn = document.getElementById('lockStatusBtn');
    const lockText = document.getElementById('lockText');

    const MASTER_PASSKEY = "Kayunga2026!";

    unlockBtn.addEventListener('click', () => {
        if (passkeyInput.value === MASTER_PASSKEY) {
            authOverlay.classList.remove('active');
            lockStatusBtn.classList.remove('locked');
            lockText.textContent = "Unlocked";
            authError.textContent = "";
            passkeyInput.value = "";
        } else {
            authError.textContent = "Incorrect Passkey. Access Denied.";
        }
    });

    demoModeBtn.addEventListener('click', () => {
        authOverlay.classList.remove('active');
        lockText.textContent = "Demo Mode";
        authError.textContent = "";
    });

    lockStatusBtn.addEventListener('click', () => {
        authOverlay.classList.add('active');
    });

    // 5. Render Log Records & Data Deletion
    const logTableBody = document.getElementById('logTableBody');
    const financialBalance = document.getElementById('financialBalance');

    function renderLogs() {
        logTableBody.innerHTML = '';
        let total = initialBalance;

        logs.forEach(log => {
            total += log.amount;
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><input type="checkbox" class="log-checkbox" data-id="${log.id}"></td>
                <td>${log.date}</td>
                <td>${log.desc}</td>
                <td>${log.cat}</td>
                <td style="color: ${log.amount >= 0 ? '#10b981' : '#ef4444'}">UGX ${log.amount.toLocaleString()}</td>
            `;
            logTableBody.appendChild(tr);
        });

        financialBalance.textContent = `UGX ${total.toLocaleString()}`;
    }

    renderLogs();

    // Add Income / Expense Controls
    document.getElementById('addIncomeBtn').addEventListener('click', () => addTransaction(true));
    document.getElementById('addExpenseBtn').addEventListener('click', () => addTransaction(false));

    function addTransaction(isIncome) {
        const desc = document.getElementById('logDescription').value || 'General Operation';
        const amt = parseFloat(document.getElementById('logAmount').value) || 0;
        if (amt <= 0) return;

        logs.push({
            id: Date.now(),
            date: new Date().toISOString().split('T')[0],
            desc: desc,
            cat: 'General',
            amount: isIncome ? amt : -amt
        });

        document.getElementById('logDescription').value = '';
        document.getElementById('logAmount').value = '';
        renderLogs();
    }

    // Delete Selected Entries
    document.getElementById('deleteSelectedBtn').addEventListener('click', () => {
        const checkedBoxes = document.querySelectorAll('.log-checkbox:checked');
        const idsToDelete = Array.from(checkedBoxes).map(cb => parseInt(cb.getAttribute('data-id')));
        logs = logs.filter(log => !idsToDelete.includes(log.id));
        renderLogs();
    });

    // 6. Chart Telemetry Rendering
    const ctx = document.getElementById('yieldChart').getContext('2d');
    let yieldChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
            datasets: [{
                label: 'Harvest Telemetry (Kg)',
                data: [120, 190, 300, 250, 220, 310, 400],
                borderColor: '#10b981',
                backgroundColor: 'rgba(16, 185, 129, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8' } } },
            scales: {
                x: { ticks: { color: '#94a3b8' }, grid: { display: false } },
                y: { ticks: { color: '#94a3b8' }, grid: { color: 'rgba(255, 255, 255, 0.05)' } }
            }
        }
    });

    function updateChartColors(isLight) {
        const color = isLight ? '#0f172a' : '#94a3b8';
        yieldChart.options.plugins.legend.labels.color = color;
        yieldChart.options.scales.x.ticks.color = color;
        yieldChart.options.scales.y.ticks.color = color;
        yieldChart.update();
    }
});
