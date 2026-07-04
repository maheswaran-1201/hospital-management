# 🏥 Hospital Management System (Python + CSV)

## 📌 Overview
This is a **console-based Hospital Management System** built using Python.  
It simulates real-world hospital operations using modular programming and CSV files for data storage.

The system supports full **CRUD operations (Create, Read, Update, Delete)** for multiple modules like Doctors, Patients, Staff, Medicines, and Machinery.

---

## ✨ Features

### 👨‍⚕️ Doctor Management
- Add new doctor records
- View all doctors
- Update doctor details
- Modify contact number and salary
- Delete doctor by ID

### 🧑‍⚕️ Patient Management
- Add new patients
- View all patient records
- Update patient details
- Modify disease and contact information
- Remove patient by ID

### 👨‍🔧 Staff Management
- Add new staff members
- View all staff records
- Update full or partial staff data
- Modify salary, contact number, and designation
- Delete staff by ID

### 💊 Medicine Management
- Add medicines
- Track expiry date and price
- Update medicine details
- Remove medicine records

### ⚙️ Machinery Management
- Add hospital machinery details
- View inventory
- Update quantity and price
- Remove machinery by ID

---

## 🛠️ Tech Stack
- Python 🐍
- CSV File Handling
- pathlib & os modules
- Modular Programming

---

## 📁 Project Structure
Hospital-Management-System/
│
├── main.py
├── doctor.py
├── patient.py
├── staff.py
├── medicine.py
├── machinery.py
│
├── doctors.csv
├── patient.csv
├── staff.csv
├── medicine.csv
├── machinery.csv
│
└── README.md


---

## ▶️ How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/hospital-management-system.git
cd hospital-management-system
python main.py

