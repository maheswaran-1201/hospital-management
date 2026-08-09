import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "staff.csv"

if not CSV_PATH.exists() and (BASE_DIR / "staff.csv").exists():
    CSV_PATH = BASE_DIR / "staff.csv"

FIELDNAMES = [
    "STAFF ID",
    "STAFF NAME",
    "GENDER",
    "AGE",
    "CONTACT NO",
    "DESIGNNATION",
    "DATE JOINED",
    "salary",
]

def load_staff(path=None):
    if path is None:
        path = CSV_PATH if CSV_PATH.exists() else DATA_DIR / "staff.csv"
    if not path.exists():
        return []
    staff_list = []
    with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items() if k}
            staff_list.append(clean_row)
    return staff_list

def save_staff(staff_list, path=None):
    if path is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "staff.csv"
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for s in staff_list:
            row = {}
            for field in FIELDNAMES:
                row[field] = s.get(field, "")
            writer.writerow(row)

def row_to_dict(row):
    return {
        "id": row.get("STAFF ID", ""),
        "name": row.get("STAFF NAME", ""),
        "gender": row.get("GENDER", ""),
        "age": row.get("AGE", ""),
        "contactNo": row.get("CONTACT NO", ""),
        "designation": row.get("DESIGNNATION", row.get("DESIGNATION", "")),
        "dateJoined": row.get("DATE JOINED", ""),
        "salary": row.get("salary", row.get("SALARY", ""))
    }

def dict_to_row(data):
    return {
        "STAFF ID": str(data.get("id", "")).strip(),
        "STAFF NAME": str(data.get("name", "")).strip(),
        "GENDER": str(data.get("gender", "")).strip(),
        "AGE": str(data.get("age", "")).strip(),
        "CONTACT NO": str(data.get("contactNo", "")).strip(),
        "DESIGNNATION": str(data.get("designation", "")).strip(),
        "DATE JOINED": str(data.get("dateJoined", "")).strip(),
        "salary": str(data.get("salary", "")).strip()
    }

def get_all_staff():
    rows = load_staff()
    return [row_to_dict(r) for r in rows]

def get_staff_by_id(staff_id):
    rows = load_staff()
    for r in rows:
        if r.get("STAFF ID", "").strip().upper() == str(staff_id).strip().upper():
            return row_to_dict(r)
    return None

def add_staff_api(data):
    staff_id = str(data.get("id", "")).strip()
    if not staff_id:
        return False, "Staff ID is required."
    if not data.get("name", "").strip():
        return False, "Staff Name is required."
    
    rows = load_staff()
    for r in rows:
        if r.get("STAFF ID", "").strip().upper() == staff_id.upper():
            return False, f"Staff member with ID '{staff_id}' already exists."
    
    new_row = dict_to_row(data)
    rows.append(new_row)
    save_staff(rows)
    return True, row_to_dict(new_row)

def update_staff_api(staff_id, data):
    rows = load_staff()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("STAFF ID", "").strip().upper() == str(staff_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Staff ID '{staff_id}' not found."
    
    current = rows[found_idx]
    new_id = str(data.get("id", staff_id)).strip()
    
    if new_id.upper() != str(staff_id).strip().upper():
        for r in rows:
            if r.get("STAFF ID", "").strip().upper() == new_id.upper():
                return False, f"Staff with ID '{new_id}' already exists."

    updated_dict = {
        "id": new_id,
        "name": data.get("name", current.get("STAFF NAME")),
        "gender": data.get("gender", current.get("GENDER")),
        "age": data.get("age", current.get("AGE")),
        "contactNo": data.get("contactNo", current.get("CONTACT NO")),
        "designation": data.get("designation", current.get("DESIGNNATION")),
        "dateJoined": data.get("dateJoined", current.get("DATE JOINED")),
        "salary": data.get("salary", current.get("salary"))
    }
    
    rows[found_idx] = dict_to_row(updated_dict)
    save_staff(rows)
    return True, row_to_dict(rows[found_idx])

def delete_staff_api(staff_id):
    rows = load_staff()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("STAFF ID", "").strip().upper() == str(staff_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Staff ID '{staff_id}' not found."
    
    removed = rows.pop(found_idx)
    save_staff(rows)
    return True, row_to_dict(removed)

def main():
    print("Staff Management Module")

if __name__ == "__main__":
    main()
