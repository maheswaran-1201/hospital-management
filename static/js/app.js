/* ==========================================================================
   MEDICARE - HOSPITAL ADMINISTRATION DASHBOARD JAVASCRIPT
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
    initApp();
});

// Global Application State
const state = {
    currentTab: 'dashboard',
    doctors: [],
    patients: [],
    staff: [],
    medicines: [],
    machinery: [],
    dashboard: null,
    editingEntity: null,
    editingId: null,
    deletingTarget: null
};

// Field Definitions for Dynamic Modal Forms
const entityFields = {
    doctors: [
        { key: 'id', label: 'Doctor ID', type: 'text', placeholder: 'e.g. D001', required: true },
        { key: 'name', label: 'Doctor Name', type: 'text', placeholder: 'Dr. John Doe', required: true },
        { key: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other'], required: true },
        { key: 'age', label: 'Age', type: 'number', placeholder: 'e.g. 42', required: true },
        { key: 'contactNo', label: 'Contact No', type: 'text', placeholder: 'e.g. 9876543210', required: true },
        { key: 'specialization', label: 'Specialization', type: 'text', placeholder: 'e.g. Cardiology', required: true },
        { key: 'experience', label: 'Years of Experience', type: 'number', placeholder: 'e.g. 15', required: true },
        { key: 'licenseNo', label: 'License No', type: 'text', placeholder: 'e.g. DL-2015-12345', required: true },
        { key: 'salary', label: 'Salary (₹)', type: 'text', placeholder: 'e.g. 120000', required: true }
    ],
    patients: [
        { key: 'id', label: 'Patient ID', type: 'text', placeholder: 'e.g. PAT001', required: true },
        { key: 'name', label: 'Patient Name', type: 'text', placeholder: 'e.g. Rajesh Kumar', required: true },
        { key: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other'], required: true },
        { key: 'age', label: 'Age', type: 'number', placeholder: 'e.g. 35', required: true },
        { key: 'contactNo', label: 'Contact No', type: 'text', placeholder: 'e.g. 9876543210', required: true },
        { key: 'dateOfAdmission', label: 'Date of Admission', type: 'text', placeholder: 'dd-mm-yyyy', required: true },
        { key: 'disease', label: 'Disease / Diagnosis', type: 'text', placeholder: 'e.g. Diabetes Type 2', required: true }
    ],
    staff: [
        { key: 'id', label: 'Staff ID', type: 'text', placeholder: 'e.g. ST001', required: true },
        { key: 'name', label: 'Staff Name', type: 'text', placeholder: 'e.g. Priya Sharma', required: true },
        { key: 'gender', label: 'Gender', type: 'select', options: ['Male', 'Female', 'Other'], required: true },
        { key: 'age', label: 'Age', type: 'number', placeholder: 'e.g. 30', required: true },
        { key: 'contactNo', label: 'Contact No', type: 'text', placeholder: 'e.g. 9876543210', required: true },
        { key: 'designation', label: 'Designation', type: 'text', placeholder: 'e.g. Nurse / Lab Tech', required: true },
        { key: 'dateJoined', label: 'Date Joined', type: 'text', placeholder: 'dd-mm-yyyy', required: true },
        { key: 'salary', label: 'Salary (₹)', type: 'text', placeholder: 'e.g. 35000', required: true }
    ],
    medicines: [
        { key: 'id', label: 'Medicine ID', type: 'text', placeholder: 'e.g. MED001', required: true },
        { key: 'name', label: 'Medicine Name', type: 'text', placeholder: 'e.g. Dolo 650', required: true },
        { key: 'genericName', label: 'Generic Name', type: 'text', placeholder: 'e.g. Paracetamol', required: true },
        { key: 'category', label: 'Category', type: 'text', placeholder: 'e.g. Analgesic / Antibiotic', required: true },
        { key: 'expiryDate', label: 'Expiry Date', type: 'text', placeholder: 'dd-mm-yyyy', required: true },
        { key: 'manufacturer', label: 'Manufacturer', type: 'text', placeholder: 'e.g. Micro Labs', required: true },
        { key: 'price', label: 'Price (₹)', type: 'text', placeholder: 'e.g. 30', required: true }
    ],
    machinery: [
        { key: 'id', label: 'Machinery ID', type: 'text', placeholder: 'e.g. M001', required: true },
        { key: 'name', label: 'Machinery Name', type: 'text', placeholder: 'e.g. Patient Monitor', required: true },
        { key: 'manufacturer', label: 'Manufacturer', type: 'text', placeholder: 'e.g. Philips', required: true },
        { key: 'category', label: 'Category', type: 'text', placeholder: 'e.g. Diagnostic Equipment', required: true },
        { key: 'quantity', label: 'Quantity', type: 'number', placeholder: 'e.g. 10', required: true },
        { key: 'dateOfPurchase', label: 'Date of Purchase', type: 'text', placeholder: 'dd-mm-yyyy', required: true },
        { key: 'price', label: 'Price (₹)', type: 'text', placeholder: 'e.g. 150000', required: true }
    ]
};

// Initialize Application
function initApp() {
    setupNavigation();
    setupEventListeners();
    loadDashboardData();
    loadAllModuleData();
}

// Setup Sidebar Navigation
function setupNavigation() {
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const targetTab = item.getAttribute('data-tab');
            switchTab(targetTab);
        });
    });

    // Stat card quick clicks to switch tab
    document.querySelectorAll('.stat-card').forEach(card => {
        card.addEventListener('click', () => {
            const target = card.getAttribute('data-target-tab');
            if (target) switchTab(target);
        });
    });
}

function switchTab(tabName) {
    state.currentTab = tabName;
    
    // Update active nav link
    document.querySelectorAll('.nav-item').forEach(el => {
        el.classList.toggle('active', el.getAttribute('data-tab') === tabName);
    });

    // Update active view
    document.querySelectorAll('.tab-view').forEach(view => {
        view.classList.toggle('active', view.id === `view-${tabName}`);
    });

    // Update Header Text
    const pageTitle = document.getElementById('page-title');
    const pageSubtitle = document.getElementById('page-subtitle');

    const headers = {
        dashboard: { title: 'Dashboard Overview', subtitle: 'Real-time hospital statistics and analytics' },
        doctors: { title: 'Doctors Directory', subtitle: 'Manage medical specialists and license details' },
        patients: { title: 'Patients Management', subtitle: 'Manage patient admissions, contacts, and diseases' },
        staff: { title: 'Hospital Staff Directory', subtitle: 'Manage nurses, technicians, and administrative staff' },
        medicines: { title: 'Pharmaceutical Inventory', subtitle: 'Monitor medicine stock, categories, and expiry dates' },
        machinery: { title: 'Medical Equipment & Machinery', subtitle: 'Track hospital devices, stock levels, and purchase dates' }
    };

    if (headers[tabName]) {
        pageTitle.textContent = headers[tabName].title;
        pageSubtitle.textContent = headers[tabName].subtitle;
    }

    // Refresh tab data
    if (tabName === 'dashboard') {
        loadDashboardData();
    } else {
        fetchEntityData(tabName);
    }
}

// Global & Dynamic Event Listeners
function setupEventListeners() {
    // Refresh Button
    document.getElementById('btn-refresh').addEventListener('click', () => {
        loadDashboardData();
        fetchEntityData(state.currentTab);
        showToast('Data refreshed successfully', 'info');
    });

    // Global Search Input
    document.getElementById('global-search-input').addEventListener('input', (e) => {
        const query = e.target.value.toLowerCase().trim();
        if (state.currentTab !== 'dashboard') {
            filterTable(state.currentTab, query);
        }
    });

    // Delete confirm button
    document.getElementById('btn-confirm-delete').addEventListener('click', () => {
        executeDelete();
    });
}

// =========================================================================
// FETCH API METHODS
// =========================================================================

// Load Dashboard Summary Data
async function loadDashboardData() {
    try {
        const res = await fetch('/api/dashboard');
        const json = await res.json();
        if (!json.success) throw new Error(json.message);

        const d = json.data;
        state.dashboard = d;

        // Render Stat Numbers
        document.getElementById('stat-doctors').textContent = d.doctorsCount || 0;
        document.getElementById('stat-patients').textContent = d.patientsCount || 0;
        document.getElementById('stat-staff').textContent = d.staffCount || 0;
        document.getElementById('stat-medicines').textContent = d.medicinesCount || 0;
        document.getElementById('stat-machinery').textContent = d.machineryCount || 0;

        // Badges
        const expBadge = document.getElementById('stat-expiring-badge');
        expBadge.textContent = `${d.expiringMedicinesCount} Alert`;
        expBadge.className = `stat-badge ${d.expiringMedicinesCount > 0 ? 'alert' : 'success'}`;

        const macBadge = document.getElementById('stat-machinery-badge');
        macBadge.textContent = `${d.lowStockMachineryCount} Low Stock`;
        macBadge.className = `stat-badge ${d.lowStockMachineryCount > 0 ? 'warning' : 'success'}`;

        // Render Recent Patients Widget Table
        renderRecentPatientsTable(d.recentPatients || []);
        renderDashboardAlerts(d);
    } catch (err) {
        showToast(`Failed to load dashboard: ${err.message}`, 'error');
    }
}

// Render Recent Patients Widget
function renderRecentPatientsTable(patients) {
    const tbody = document.getElementById('recent-patients-tbody');
    if (!patients.length) {
        tbody.innerHTML = `<tr><td colspan="7" class="text-center">No patient admissions recorded.</td></tr>`;
        return;
    }

    tbody.innerHTML = patients.map(p => `
        <tr>
            <td><strong>${escapeHtml(p.id)}</strong></td>
            <td>${escapeHtml(p.name)}</td>
            <td>${escapeHtml(p.gender)}</td>
            <td>${escapeHtml(p.age)}</td>
            <td>${escapeHtml(p.contactNo)}</td>
            <td><span class="badge badge-secondary">${escapeHtml(p.dateOfAdmission)}</span></td>
            <td><span class="badge badge-warning">${escapeHtml(p.disease)}</span></td>
        </tr>
    `).join('');
}

// Render Dashboard Inventory Alerts
function renderDashboardAlerts(d) {
    const container = document.getElementById('dashboard-alerts');
    let html = `
        <div class="alert-item info">
            <span class="alert-icon">📊</span>
            <div class="alert-text">
                <strong>CSV Database Connected</strong>
                <p>All hospital data synced directly with data/*.csv files.</p>
            </div>
        </div>
    `;

    if (d.expiringMedicinesCount > 0) {
        html += `
            <div class="alert-item danger">
                <span class="alert-icon">⚠️</span>
                <div class="alert-text">
                    <strong>${d.expiringMedicinesCount} Medicines Require Attention</strong>
                    <p>Medicines are expired or expiring within 90 days.</p>
                </div>
            </div>
        `;
    }

    if (d.lowStockMachineryCount > 0) {
        html += `
            <div class="alert-item warning">
                <span class="alert-icon">⚙️</span>
                <div class="alert-text">
                    <strong>${d.lowStockMachineryCount} Equipment Low Stock</strong>
                    <p>Machinery items have quantity ≤ 5 units.</p>
                </div>
            </div>
        `;
    }

    container.innerHTML = html;
}

// Pre-fetch all module data
function loadAllModuleData() {
    ['doctors', 'patients', 'staff', 'medicines', 'machinery'].forEach(entity => fetchEntityData(entity));
}

// Fetch Specific Entity Data
async function fetchEntityData(entity) {
    if (!entity || entity === 'dashboard') return;

    const tbody = document.querySelector(`#table-${entity} tbody`);
    if (tbody) {
        tbody.innerHTML = `<tr><td colspan="10" class="text-center">Loading ${entity}...</td></tr>`;
    }

    try {
        const res = await fetch(`/api/${entity}`);
        const json = await res.json();
        if (!json.success) throw new Error(json.message);

        state[entity] = json.data;
        renderEntityTable(entity, json.data);
    } catch (err) {
        showToast(`Failed to load ${entity}: ${err.message}`, 'error');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="10" class="text-center text-danger">Error loading data.</td></tr>`;
        }
    }
}

// Render Entity Data Tables
function renderEntityTable(entity, items) {
    const tbody = document.querySelector(`#table-${entity} tbody`);
    if (!tbody) return;

    if (!items || items.length === 0) {
        tbody.innerHTML = `<tr><td colspan="10" class="text-center">No ${entity} records found.</td></tr>`;
        return;
    }

    let rowsHtml = '';
    items.forEach(item => {
        rowsHtml += `<tr>`;

        if (entity === 'doctors') {
            rowsHtml += `
                <td><strong>${escapeHtml(item.id)}</strong></td>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.gender)}</td>
                <td>${escapeHtml(item.age)}</td>
                <td>${escapeHtml(item.contactNo)}</td>
                <td><span class="badge badge-secondary">${escapeHtml(item.specialization)}</span></td>
                <td>${escapeHtml(item.experience)} yrs</td>
                <td><code>${escapeHtml(item.licenseNo)}</code></td>
                <td>₹${escapeHtml(item.salary)}</td>
            `;
        } else if (entity === 'patients') {
            rowsHtml += `
                <td><strong>${escapeHtml(item.id)}</strong></td>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.gender)}</td>
                <td>${escapeHtml(item.age)}</td>
                <td>${escapeHtml(item.contactNo)}</td>
                <td><span class="badge badge-secondary">${escapeHtml(item.dateOfAdmission)}</span></td>
                <td><span class="badge badge-warning">${escapeHtml(item.disease)}</span></td>
            `;
        } else if (entity === 'staff') {
            rowsHtml += `
                <td><strong>${escapeHtml(item.id)}</strong></td>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.gender)}</td>
                <td>${escapeHtml(item.age)}</td>
                <td>${escapeHtml(item.contactNo)}</td>
                <td><span class="badge badge-secondary">${escapeHtml(item.designation)}</span></td>
                <td>${escapeHtml(item.dateJoined)}</td>
                <td>₹${escapeHtml(item.salary)}</td>
            `;
        } else if (entity === 'medicines') {
            const expStatus = getExpiryStatus(item.expiryDate);
            rowsHtml += `
                <td><strong>${escapeHtml(item.id)}</strong></td>
                <td>${escapeHtml(item.name)}</td>
                <td><em>${escapeHtml(item.genericName)}</em></td>
                <td><span class="badge badge-secondary">${escapeHtml(item.category)}</span></td>
                <td>${escapeHtml(item.expiryDate)}</td>
                <td>${escapeHtml(item.manufacturer)}</td>
                <td>₹${escapeHtml(item.price)}</td>
                <td>${expStatus.badgeHtml}</td>
            `;
        } else if (entity === 'machinery') {
            const stockStatus = getStockStatus(item.quantity);
            rowsHtml += `
                <td><strong>${escapeHtml(item.id)}</strong></td>
                <td>${escapeHtml(item.name)}</td>
                <td>${escapeHtml(item.manufacturer)}</td>
                <td><span class="badge badge-secondary">${escapeHtml(item.category)}</span></td>
                <td><strong>${escapeHtml(item.quantity)}</strong></td>
                <td>${escapeHtml(item.dateOfPurchase)}</td>
                <td>₹${escapeHtml(item.price)}</td>
                <td>${stockStatus.badgeHtml}</td>
            `;
        }

        // Action Buttons
        rowsHtml += `
            <td class="text-right">
                <div class="table-actions">
                    <button class="action-btn edit" title="Edit" onclick="openEditModal('${entity}', '${escapeHtml(item.id)}')">✏️</button>
                    <button class="action-btn delete" title="Delete" onclick="confirmDelete('${entity}', '${escapeHtml(item.id)}')">🗑️</button>
                </div>
            </td>
        </tr>`;
    });

    tbody.innerHTML = rowsHtml;
}

// Calculate Expiry Status for Medicine Visual Indicators
function getExpiryStatus(dateStr) {
    if (!dateStr) return { status: 'valid', badgeHtml: '<span class="badge badge-secondary">Unknown</span>' };

    let expDate = null;
    const formats = [
        /^(\d{1,2})-(\d{1,2})-(\d{4})$/,
        /^(\d{4})-(\d{1,2})-(\d{1,2})$/,
        /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/
    ];

    for (let regex of formats) {
        const match = dateStr.match(regex);
        if (match) {
            if (regex.source.startsWith('^(\\d{4})')) {
                expDate = new Date(match[1], match[2] - 1, match[3]);
            } else {
                expDate = new Date(match[3], match[2] - 1, match[1]);
            }
            break;
        }
    }

    if (!expDate || isNaN(expDate.getTime())) {
        return { status: 'valid', badgeHtml: '<span class="badge badge-secondary">Valid</span>' };
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);

    const diffDays = Math.ceil((expDate - today) / (1000 * 60 * 60 * 24));

    if (diffDays < 0) {
        return { status: 'expired', badgeHtml: '<span class="badge badge-danger">Expired</span>' };
    } else if (diffDays <= 90) {
        return { status: 'expiring', badgeHtml: `<span class="badge badge-warning">Expiring in ${diffDays}d</span>` };
    } else {
        return { status: 'valid', badgeHtml: '<span class="badge badge-success">Valid</span>' };
    }
}

// Calculate Stock Status for Machinery Visual Indicators
function getStockStatus(qtyStr) {
    const qty = parseInt(qtyStr, 10);
    if (isNaN(qty) || qty <= 5) {
        return { status: 'low', badgeHtml: `<span class="badge badge-danger">Low Stock (${isNaN(qty)?0:qty})</span>` };
    } else {
        return { status: 'normal', badgeHtml: `<span class="badge badge-success">In Stock (${qty})</span>` };
    }
}

// Filter Medicines by Expiry Status
function filterMedicinesByExpiry(filterVal) {
    if (filterVal === 'all') {
        renderEntityTable('medicines', state.medicines);
        return;
    }

    const filtered = state.medicines.filter(m => {
        const statusObj = getExpiryStatus(m.expiryDate);
        return statusObj.status === filterVal;
    });

    renderEntityTable('medicines', filtered);
}

// Search Table Filter
function filterTable(entity, query) {
    query = query.toLowerCase().trim();
    if (!query) {
        renderEntityTable(entity, state[entity]);
        return;
    }

    const filtered = state[entity].filter(item => {
        return Object.values(item).some(val => 
            String(val).toLowerCase().includes(query)
        );
    });

    renderEntityTable(entity, filtered);
}

// =========================================================================
// MODAL FORMS & CRUD OPERATIONS
// =========================================================================

// Open Modal to Add Record
function openAddModal(entity) {
    state.editingEntity = entity;
    state.editingId = null;

    document.getElementById('modal-title').textContent = `Add New ${capitalize(entity.slice(0, -1))}`;
    buildFormFields(entity, null);
    
    document.getElementById('crud-modal').classList.add('active');
}

// Open Modal to Edit Record
function openEditModal(entity, id) {
    state.editingEntity = entity;
    state.editingId = id;

    const item = state[entity].find(x => String(x.id).toUpperCase() === String(id).toUpperCase());
    if (!item) {
        showToast('Record not found', 'error');
        return;
    }

    document.getElementById('modal-title').textContent = `Edit ${capitalize(entity.slice(0, -1))} (${id})`;
    buildFormFields(entity, item);

    document.getElementById('crud-modal').classList.add('active');
}

// Close CRUD Modal
function closeModal() {
    document.getElementById('crud-modal').classList.remove('active');
    state.editingEntity = null;
    state.editingId = null;
}

// Build Dynamic Input Controls for Entity
function buildFormFields(entity, existingData) {
    const fields = entityFields[entity];
    const container = document.getElementById('modal-form-fields');
    if (!fields || !container) return;

    let html = '';
    fields.forEach(field => {
        const value = existingData ? (existingData[field.key] || '') : '';
        const isIdField = field.key === 'id';
        const disabledAttr = (isIdField && existingData) ? 'readonly style="background:#f1f5f9;"' : '';

        html += `<div class="form-group">`;
        html += `<label for="field-${field.key}">${field.label} ${field.required ? '<span class="required">*</span>' : ''}</label>`;

        if (field.type === 'select') {
            html += `<select class="form-control" id="field-${field.key}" name="${field.key}" ${field.required ? 'required' : ''}>`;
            field.options.forEach(opt => {
                const selected = value.toLowerCase() === opt.toLowerCase() ? 'selected' : '';
                html += `<option value="${opt}" ${selected}>${opt}</option>`;
            });
            html += `</select>`;
        } else {
            html += `<input type="${field.type}" class="form-control" id="field-${field.key}" name="${field.key}" value="${escapeHtml(value)}" placeholder="${field.placeholder || ''}" ${disabledAttr} ${field.required ? 'required' : ''}>`;
        }

        html += `</div>`;
    });

    container.innerHTML = html;
}

// Handle Add / Edit Form Submit
async function handleFormSubmit(e) {
    e.preventDefault();
    const entity = state.editingEntity;
    const isEdit = !!state.editingId;

    if (!entity) return;

    const formData = new FormData(e.target);
    const payload = {};
    formData.forEach((val, key) => {
        payload[key] = val.trim();
    });

    // Frontend Validations
    if (!payload.id) {
        showToast('ID field cannot be empty.', 'error');
        return;
    }
    if (!payload.name) {
        showToast('Name field cannot be empty.', 'error');
        return;
    }

    const saveBtn = document.getElementById('btn-modal-save');
    saveBtn.disabled = true;
    saveBtn.textContent = 'Saving...';

    try {
        const url = isEdit ? `/api/${entity}/${encodeURIComponent(state.editingId)}` : `/api/${entity}`;
        const method = isEdit ? 'PUT' : 'POST';

        const res = await fetch(url, {
            method: method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const json = await res.json();
        if (!res.ok || !json.success) {
            throw new Error(json.message || 'Error saving record');
        }

        showToast(json.message || 'Record saved successfully!', 'success');
        closeModal();

        // Refresh Data
        await fetchEntityData(entity);
        loadDashboardData();
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        saveBtn.disabled = false;
        saveBtn.textContent = 'Save Record';
    }
}

// =========================================================================
// DELETE CONFIRMATION MODAL & EXECUTION
// =========================================================================

function confirmDelete(entity, id) {
    state.deletingTarget = { entity, id };
    document.getElementById('delete-modal-text').textContent = `Are you sure you want to delete ${capitalize(entity.slice(0, -1))} ID '${id}'? This will modify data/*.csv.`;
    document.getElementById('delete-modal').classList.add('active');
}

function closeDeleteModal() {
    document.getElementById('delete-modal').classList.remove('active');
    state.deletingTarget = null;
}

async function executeDelete() {
    if (!state.deletingTarget) return;

    const { entity, id } = state.deletingTarget;
    const btn = document.getElementById('btn-confirm-delete');
    btn.disabled = true;
    btn.textContent = 'Deleting...';

    try {
        const res = await fetch(`/api/${entity}/${encodeURIComponent(id)}`, {
            method: 'DELETE'
        });

        const json = await res.json();
        if (!res.ok || !json.success) {
            throw new Error(json.message || 'Error deleting record');
        }

        showToast(json.message || 'Record deleted successfully!', 'success');
        closeDeleteModal();

        // Refresh Data
        await fetchEntityData(entity);
        loadDashboardData();
    } catch (err) {
        showToast(err.message, 'error');
    } finally {
        btn.disabled = false;
        btn.textContent = 'Delete';
    }
}

// =========================================================================
// UTILITY HELPERS & TOAST SYSTEM
// =========================================================================

function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    
    const icon = type === 'success' ? '✅' : (type === 'error' ? '❌' : (type === 'warning' ? '⚠️' : 'ℹ️'));
    
    toast.innerHTML = `
        <span style="font-size: 18px;">${icon}</span>
        <span class="toast-message">${escapeHtml(message)}</span>
    `;

    container.appendChild(toast);

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateX(100%)';
        toast.style.transition = 'all 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

function capitalize(str) {
    if (!str) return '';
    return str.charAt(0).toUpperCase() + str.slice(1);
}

function escapeHtml(str) {
    if (str === null || str === undefined) return '';
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}
