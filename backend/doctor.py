import csv
import os
from pathlib import Path

# Data directory path
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "doctors.csv"

# Fallback path if data/ doesn't exist yet
if not CSV_PATH.exists() and (BASE_DIR / "doctors.csv").exists():
    CSV_PATH = BASE_DIR / "doctors.csv"

FIELDNAMES = [
    "Doctor ID",
    "Doctor Name",
    "Gender",
    "Age",
    "Contact No",
    "Specialization",
    "Years of Experience",
    "License No",
    "Salary (₹)",
]

def ensure_file_exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    target = DATA_DIR / "doctors.csv"
    if not target.exists():
        with open(target, mode="w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
    return target

def load_doctors(path=None):
    if path is None:
        path = CSV_PATH if CSV_PATH.exists() else DATA_DIR / "doctors.csv"
    if not path.exists():
        return []
    doctors = []
    with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean string keys and values
            clean_row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items() if k}
            doctors.append(clean_row)
    return doctors

def save_doctors(doctors, path=None):
    if path is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "doctors.csv"
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for doc in doctors:
            row = {}
            for field in FIELDNAMES:
                row[field] = doc.get(field, "")
            writer.writerow(row)

# Mapping functions for REST API
def row_to_dict(row):
    return {
        "id": row.get("Doctor ID", ""),
        "name": row.get("Doctor Name", ""),
        "gender": row.get("Gender", ""),
        "age": row.get("Age", ""),
        "contactNo": row.get("Contact No", ""),
        "specialization": row.get("Specialization", ""),
        "experience": row.get("Years of Experience", ""),
        "licenseNo": row.get("License No", ""),
        "salary": row.get("Salary (₹)", "")
    }

def dict_to_row(data):
    return {
        "Doctor ID": str(data.get("id", "")).strip(),
        "Doctor Name": str(data.get("name", "")).strip(),
        "Gender": str(data.get("gender", "")).strip(),
        "Age": str(data.get("age", "")).strip(),
        "Contact No": str(data.get("contactNo", "")).strip(),
        "Specialization": str(data.get("specialization", "")).strip(),
        "Years of Experience": str(data.get("experience", "")).strip(),
        "License No": str(data.get("licenseNo", "")).strip(),
        "Salary (₹)": str(data.get("salary", "")).strip()
    }

def get_all_doctors():
    rows = load_doctors()
    return [row_to_dict(r) for r in rows]

def get_doctor_by_id(doc_id):
    rows = load_doctors()
    for r in rows:
        if r.get("Doctor ID", "").strip().upper() == str(doc_id).strip().upper():
            return row_to_dict(r)
    return None

def add_doctor_api(data):
    doc_id = str(data.get("id", "")).strip()
    if not doc_id:
        return False, "Doctor ID is required."
    if not data.get("name", "").strip():
        return False, "Doctor Name is required."
    
    rows = load_doctors()
    for r in rows:
        if r.get("Doctor ID", "").strip().upper() == doc_id.upper():
            return False, f"Doctor with ID '{doc_id}' already exists."
    
    new_row = dict_to_row(data)
    rows.append(new_row)
    save_doctors(rows)
    return True, row_to_dict(new_row)

def update_doctor_api(doc_id, data):
    rows = load_doctors()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("Doctor ID", "").strip().upper() == str(doc_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Doctor ID '{doc_id}' not found."
    
    current = rows[found_idx]
    new_id = str(data.get("id", doc_id)).strip()
    
    # Check for duplicate ID if ID is being changed
    if new_id.upper() != str(doc_id).strip().upper():
        for r in rows:
            if r.get("Doctor ID", "").strip().upper() == new_id.upper():
                return False, f"Doctor with ID '{new_id}' already exists."

    updated_dict = {
        "id": new_id,
        "name": data.get("name", current.get("Doctor Name")),
        "gender": data.get("gender", current.get("Gender")),
        "age": data.get("age", current.get("Age")),
        "contactNo": data.get("contactNo", current.get("Contact No")),
        "specialization": data.get("specialization", current.get("Specialization")),
        "experience": data.get("experience", current.get("Years of Experience")),
        "licenseNo": data.get("licenseNo", current.get("License No")),
        "salary": data.get("salary", current.get("Salary (₹)"))
    }
    
    rows[found_idx] = dict_to_row(updated_dict)
    save_doctors(rows)
    return True, row_to_dict(rows[found_idx])

def delete_doctor_api(doc_id):
    rows = load_doctors()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("Doctor ID", "").strip().upper() == str(doc_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Doctor ID '{doc_id}' not found."
    
    removed = rows.pop(found_idx)
    save_doctors(rows)
    return True, row_to_dict(removed)

# Backward-compatible CLI functions
def find_by_id(doctors, doc_id):
    for d in doctors:
        if d.get("Doctor ID") == doc_id:
            return d
    return None

def print_all(doctors):
    if not doctors:
        print("No records found.")
        return
    for d in doctors:
        print("-" * 60)
        for k in FIELDNAMES:
            print(f"{k}: {d.get(k, '')}")
    print("-" * 60)

def main():
    while True:
        print("\nDOCTOR MENU")
        print("1. Read all doctors")
        print("2. Add new doctor")
        print("3. Remove doctor by ID")
        print("0. Exit")

        choice = input("Enter choice: ").strip()
        if choice == "0":
            break
        doctors = load_doctors()
        if choice == "1":
            print_all(doctors)
        elif choice == "2":
            new_doc = {}
            for f in FIELDNAMES:
                new_doc[f] = input(f"{f}: ")
            doctors.append(new_doc)
            save_doctors(doctors)
            print("Doctor added.")
        elif choice == "3":
            did = input("Doctor ID: ")
            d = find_by_id(doctors, did)
            if d:
                doctors.remove(d)
                save_doctors(doctors)
                print("Doctor deleted.")
            else:
                print("Not found.")

if __name__ == "__main__":
    main()
