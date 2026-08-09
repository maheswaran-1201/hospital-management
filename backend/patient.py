import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "patient.csv"

if not CSV_PATH.exists() and (BASE_DIR / "patient.csv").exists():
    CSV_PATH = BASE_DIR / "patient.csv"

FIELDNAMES = [
    "PATIENT ID",
    "PATIENT NAME",
    "GENDER",
    "AGE",
    "CONTACT NO",
    "DATE OF ADMISSION",
    "DISEASE",
]

def load_patients(path=None):
    if path is None:
        path = CSV_PATH if CSV_PATH.exists() else DATA_DIR / "patient.csv"
    if not path.exists():
        return []
    patients = []
    with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items() if k}
            patients.append(clean_row)
    return patients

def save_patients(patients, path=None):
    if path is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "patient.csv"
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for p in patients:
            row = {}
            for field in FIELDNAMES:
                row[field] = p.get(field, "")
            writer.writerow(row)

def row_to_dict(row):
    return {
        "id": row.get("PATIENT ID", ""),
        "name": row.get("PATIENT NAME", ""),
        "gender": row.get("GENDER", ""),
        "age": row.get("AGE", ""),
        "contactNo": row.get("CONTACT NO", ""),
        "dateOfAdmission": row.get("DATE OF ADMISSION", ""),
        "disease": row.get("DISEASE", "")
    }

def dict_to_row(data):
    return {
        "PATIENT ID": str(data.get("id", "")).strip(),
        "PATIENT NAME": str(data.get("name", "")).strip(),
        "GENDER": str(data.get("gender", "")).strip(),
        "AGE": str(data.get("age", "")).strip(),
        "CONTACT NO": str(data.get("contactNo", "")).strip(),
        "DATE OF ADMISSION": str(data.get("dateOfAdmission", "")).strip(),
        "DISEASE": str(data.get("disease", "")).strip()
    }

def get_all_patients():
    rows = load_patients()
    return [row_to_dict(r) for r in rows]

def get_patient_by_id(pat_id):
    rows = load_patients()
    for r in rows:
        if r.get("PATIENT ID", "").strip().upper() == str(pat_id).strip().upper():
            return row_to_dict(r)
    return None

def add_patient_api(data):
    pat_id = str(data.get("id", "")).strip()
    if not pat_id:
        return False, "Patient ID is required."
    if not data.get("name", "").strip():
        return False, "Patient Name is required."
    
    rows = load_patients()
    for r in rows:
        if r.get("PATIENT ID", "").strip().upper() == pat_id.upper():
            return False, f"Patient with ID '{pat_id}' already exists."
    
    new_row = dict_to_row(data)
    rows.append(new_row)
    save_patients(rows)
    return True, row_to_dict(new_row)

def update_patient_api(pat_id, data):
    rows = load_patients()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("PATIENT ID", "").strip().upper() == str(pat_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Patient ID '{pat_id}' not found."
    
    current = rows[found_idx]
    new_id = str(data.get("id", pat_id)).strip()
    
    if new_id.upper() != str(pat_id).strip().upper():
        for r in rows:
            if r.get("PATIENT ID", "").strip().upper() == new_id.upper():
                return False, f"Patient with ID '{new_id}' already exists."

    updated_dict = {
        "id": new_id,
        "name": data.get("name", current.get("PATIENT NAME")),
        "gender": data.get("gender", current.get("GENDER")),
        "age": data.get("age", current.get("AGE")),
        "contactNo": data.get("contactNo", current.get("CONTACT NO")),
        "dateOfAdmission": data.get("dateOfAdmission", current.get("DATE OF ADMISSION")),
        "disease": data.get("disease", current.get("DISEASE"))
    }
    
    rows[found_idx] = dict_to_row(updated_dict)
    save_patients(rows)
    return True, row_to_dict(rows[found_idx])

def delete_patient_api(pat_id):
    rows = load_patients()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("PATIENT ID", "").strip().upper() == str(pat_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Patient ID '{pat_id}' not found."
    
    removed = rows.pop(found_idx)
    save_patients(rows)
    return True, row_to_dict(removed)

def main():
    print("Patient Management Module")

if __name__ == "__main__":
    main()
