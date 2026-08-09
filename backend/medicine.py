import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
# Check both medicine.csv and medicines.csv for robustness
CSV_PATH = DATA_DIR / "medicine.csv"
if not CSV_PATH.exists() and (DATA_DIR / "medicines.csv").exists():
    CSV_PATH = DATA_DIR / "medicines.csv"
elif not CSV_PATH.exists() and (BASE_DIR / "medicine.csv").exists():
    CSV_PATH = BASE_DIR / "medicine.csv"

FIELDNAMES = [
    "MEDICINE ID",
    "MEDICINE NAME",
    "GENIRIC NAME ",
    "CATEGORY",
    "EXPIRY DATE",
    "MANNUFACTURER",
    "PRICE",
]

def load_medicines(path=None):
    if path is None:
        path = CSV_PATH if CSV_PATH.exists() else DATA_DIR / "medicine.csv"
    if not path.exists():
        return []
    medicines = []
    with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items() if k}
            medicines.append(clean_row)
    return medicines

def save_medicines(medicines, path=None):
    if path is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "medicine.csv"
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for m in medicines:
            row = {}
            for field in FIELDNAMES:
                row[field] = m.get(field, "")
            writer.writerow(row)

def row_to_dict(row):
    # Handle variations in header names seamlessly
    generic = row.get("GENIRIC NAME ") or row.get("GENIRIC NAME") or row.get("GENERIC NAME") or ""
    manufacturer = row.get("MANNUFACTURER") or row.get("MANUFACTURER") or ""
    return {
        "id": row.get("MEDICINE ID", ""),
        "name": row.get("MEDICINE NAME", ""),
        "genericName": generic,
        "category": row.get("CATEGORY", ""),
        "expiryDate": row.get("EXPIRY DATE", ""),
        "manufacturer": manufacturer,
        "price": row.get("PRICE", "")
    }

def dict_to_row(data):
    return {
        "MEDICINE ID": str(data.get("id", "")).strip(),
        "MEDICINE NAME": str(data.get("name", "")).strip(),
        "GENIRIC NAME ": str(data.get("genericName", "")).strip(),
        "CATEGORY": str(data.get("category", "")).strip(),
        "EXPIRY DATE": str(data.get("expiryDate", "")).strip(),
        "MANNUFACTURER": str(data.get("manufacturer", "")).strip(),
        "PRICE": str(data.get("price", "")).strip()
    }

def get_all_medicines():
    rows = load_medicines()
    return [row_to_dict(r) for r in rows]

def get_medicine_by_id(med_id):
    rows = load_medicines()
    for r in rows:
        if r.get("MEDICINE ID", "").strip().upper() == str(med_id).strip().upper():
            return row_to_dict(r)
    return None

def add_medicine_api(data):
    med_id = str(data.get("id", "")).strip()
    if not med_id:
        return False, "Medicine ID is required."
    if not data.get("name", "").strip():
        return False, "Medicine Name is required."
    
    rows = load_medicines()
    for r in rows:
        if r.get("MEDICINE ID", "").strip().upper() == med_id.upper():
            return False, f"Medicine with ID '{med_id}' already exists."
    
    new_row = dict_to_row(data)
    rows.append(new_row)
    save_medicines(rows)
    return True, row_to_dict(new_row)

def update_medicine_api(med_id, data):
    rows = load_medicines()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("MEDICINE ID", "").strip().upper() == str(med_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Medicine ID '{med_id}' not found."
    
    current = rows[found_idx]
    new_id = str(data.get("id", med_id)).strip()
    
    if new_id.upper() != str(med_id).strip().upper():
        for r in rows:
            if r.get("MEDICINE ID", "").strip().upper() == new_id.upper():
                return False, f"Medicine with ID '{new_id}' already exists."

    curr_dict = row_to_dict(current)
    updated_dict = {
        "id": new_id,
        "name": data.get("name", curr_dict["name"]),
        "genericName": data.get("genericName", curr_dict["genericName"]),
        "category": data.get("category", curr_dict["category"]),
        "expiryDate": data.get("expiryDate", curr_dict["expiryDate"]),
        "manufacturer": data.get("manufacturer", curr_dict["manufacturer"]),
        "price": data.get("price", curr_dict["price"])
    }
    
    rows[found_idx] = dict_to_row(updated_dict)
    save_medicines(rows)
    return True, row_to_dict(rows[found_idx])

def delete_medicine_api(med_id):
    rows = load_medicines()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("MEDICINE ID", "").strip().upper() == str(med_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Medicine ID '{med_id}' not found."
    
    removed = rows.pop(found_idx)
    save_medicines(rows)
    return True, row_to_dict(removed)

def main():
    print("Medicine Management Module")

if __name__ == "__main__":
    main()
