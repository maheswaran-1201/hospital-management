# MediCare - Hospital Management System

A modern, full-stack Hospital Administration Web Application built with Python Flask, HTML5, CSS3, Vanilla JavaScript, and CSV-based data storage.

This project upgrades a legacy Python CLI application into a modern web administration dashboard without replacing the underlying CSV data files or introducing external databases.

---

## 🌟 Features

- **Dynamic Admin Dashboard Overview**:
  - Live counts of Doctors, Patients, Staff, Medicines, and Machinery.
  - Automatic calculation of statistics from CSV data files.
  - Inventory alert panel for expiring medicines and low machinery stock.
  - Recent patient admission activity log.

- **Doctor Management**:
  - View, Add, Edit, Delete, and Search doctors.
  - Tracks Doctor ID, Name, Gender, Age, Contact No, Specialization, Experience, License No, and Salary.
  - Validation against duplicate Doctor IDs.

- **Patient Management**:
  - View, Add, Edit, Delete, and Search patient records.
  - Tracks Patient ID, Name, Gender, Age, Contact No, Date of Admission, and Disease.
  - Real-time search by ID, Name, or Disease.

- **Staff Management**:
  - View, Add, Edit, Delete, and Search hospital staff.
  - Tracks Staff ID, Name, Gender, Age, Contact No, Designation, Date Joined, and Salary.

- **Medicine Management**:
  - View, Add, Edit, Delete, and Search medicines.
  - Tracks Medicine ID, Name, Generic Name, Category, Expiry Date, Manufacturer, and Price.
  - **Visual Expiry Badges**: Expired (red), Expiring Soon (yellow), or Valid (green).

- **Machinery / Equipment Management**:
  - View, Add, Edit, Delete, and Search machinery.
  - Tracks Machinery ID, Name, Manufacturer, Category, Quantity, Date of Purchase, and Price.
  - **Stock Alert Badges**: Low Stock indicator for quantities $\le 5$.

- **Modern Responsive UI**:
  - Hospital-themed design system using HSL colors, smooth transitions, card layouts, and custom scrollbars.
  - Single-Page Application (SPA) experience using Fetch API without full page reloads.
  - Modal form dialogs for Add/Edit operations, delete confirmations, and toast notification queue.

---

## 🛠️ Technology Stack

- **Backend**: Python 3, Flask, REST API
- **Frontend**: HTML5, CSS3 (Vanilla CSS), JavaScript (ES6+, Fetch API)
- **Data Storage**: CSV files (`doctors.csv`, `patient.csv`, `staff.csv`, `medicine.csv`, `machinery.csv`)

---

## 📁 Project Structure

```
Hospital-Management-System/
├── app.py                      # Flask Application & REST API Endpoints
├── backend/                    # Python Modules for CSV operations
│   ├── __init__.py
│   ├── doctor.py               # Doctor CSV CRUD logic & validation
│   ├── patient.py              # Patient CSV CRUD logic & validation
│   ├── staff.py                # Staff CSV CRUD logic & validation
│   ├── medicine.py             # Medicine CSV CRUD logic & validation
│   └── machinery.py            # Machinery CSV CRUD logic & validation
├── data/                       # CSV Data Storage (Source of Truth)
│   ├── doctors.csv
│   ├── patient.csv
│   ├── staff.csv
│   ├── medicine.csv
│   └── machinery.csv
├── templates/
│   └── index.html              # Main Single Page Admin Dashboard
├── static/
│   ├── css/
│   │   └── style.css           # Modern hospital-themed dashboard stylesheet
│   └── js/
│       └── app.js              # Vanilla JS controller & REST API client
└── README.md                   # Documentation
```

---

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8+ installed on your system.

### Step 1: Install Dependencies
Install Flask:
```bash
pip install flask
```

### Step 2: Run the Web Application
Execute `app.py` from the project root directory:
```bash
python app.py
```

### Step 3: Open in Browser
Open your web browser and navigate to:
```
[https://hospital-management-14cbe.web.app](https://hospital-management-14cbe.web.app)
```

---

## 🔌 API Overview

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /` | `GET` | Renders the Admin Dashboard website interface |
| `GET /api/dashboard` | `GET` | Returns aggregated metrics & stats from CSV files |
| `GET /api/doctors` | `GET` | List all doctors |
| `POST /api/doctors` | `POST` | Add a new doctor record |
| `PUT /api/doctors/<id>` | `PUT` | Update an existing doctor record |
| `DELETE /api/doctors/<id>` | `DELETE` | Delete a doctor by ID |
| `GET /api/patients` | `GET` | List all patients |
| `POST /api/patients` | `POST` | Add a new patient record |
| `PUT /api/patients/<id>` | `PUT` | Update an existing patient record |
| `DELETE /api/patients/<id>` | `DELETE` | Delete a patient by ID |
| `GET /api/staff` | `GET` | List all staff members |
| `POST /api/staff` | `POST` | Add a new staff record |
| `PUT /api/staff/<id>` | `PUT` | Update an existing staff record |
| `DELETE /api/staff/<id>` | `DELETE` | Delete a staff member by ID |
| `GET /api/medicines` | `GET` | List all medicines |
| `POST /api/medicines` | `POST` | Add a new medicine record |
| `PUT /api/medicines/<id>` | `PUT` | Update an existing medicine record |
| `DELETE /api/medicines/<id>` | `DELETE` | Delete a medicine by ID |
| `GET /api/machinery` | `GET` | List all machinery / equipment |
| `POST /api/machinery` | `POST` | Add a new machinery record |
| `PUT /api/machinery/<id>` | `PUT` | Update an existing machinery record |
| `DELETE /api/machinery/<id>` | `DELETE` | Delete a machinery item by ID |

---

## 📊 CSV Data Explanation

The application reads and writes directly to the CSV files in `data/`:
- `data/doctors.csv`: Stores doctor details.
- `data/patient.csv`: Stores patient details.
- `data/staff.csv`: Stores hospital staff details.
- `data/medicine.csv`: Stores pharmaceutical stock details.
- `data/machinery.csv`: Stores medical device details.

Existing header column names and formatting are preserved for 100% backward compatibility.
