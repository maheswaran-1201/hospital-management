import csv
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CSV_PATH = DATA_DIR / "machinery.csv"

if not CSV_PATH.exists() and (BASE_DIR / "machinery.csv").exists():
    CSV_PATH = BASE_DIR / "machinery.csv"

FIELDNAMES = [
    "MACHINERY ID",
    "MACHINERY NAME",
    "MANUFACTURER",
    "CATEGORY",
    "QUANTITY",
    "DATE OF PURCHASE",
    "PRICE",
]

def load_machinery(path=None):
    if path is None:
        path = CSV_PATH if CSV_PATH.exists() else DATA_DIR / "machinery.csv"
    if not path.exists():
        return []
    machines = []
    with path.open(mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() if isinstance(v, str) else v for k, v in row.items() if k}
            machines.append(clean_row)
    return machines

def save_machinery(machines, path=None):
    if path is None:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        path = DATA_DIR / "machinery.csv"
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for m in machines:
            row = {}
            for field in FIELDNAMES:
                row[field] = m.get(field, "")
            writer.writerow(row)

def row_to_dict(row):
    return {
        "id": row.get("MACHINERY ID", ""),
        "name": row.get("MACHINERY NAME", ""),
        "manufacturer": row.get("MANUFACTURER", ""),
        "category": row.get("CATEGORY", ""),
        "quantity": row.get("QUANTITY", ""),
        "dateOfPurchase": row.get("DATE OF PURCHASE", ""),
        "price": row.get("PRICE", "")
    }

def dict_to_row(data):
    return {
        "MACHINERY ID": str(data.get("id", "")).strip(),
        "MACHINERY NAME": str(data.get("name", "")).strip(),
        "MANUFACTURER": str(data.get("manufacturer", "")).strip(),
        "CATEGORY": str(data.get("category", "")).strip(),
        "QUANTITY": str(data.get("quantity", "")).strip(),
        "DATE OF PURCHASE": str(data.get("dateOfPurchase", "")).strip(),
        "PRICE": str(data.get("price", "")).strip()
    }

def get_all_machinery():
    rows = load_machinery()
    return [row_to_dict(r) for r in rows]

def get_machinery_by_id(mac_id):
    rows = load_machinery()
    for r in rows:
        if r.get("MACHINERY ID", "").strip().upper() == str(mac_id).strip().upper():
            return row_to_dict(r)
    return None

def add_machinery_api(data):
    mac_id = str(data.get("id", "")).strip()
    if not mac_id:
        return False, "Machinery ID is required."
    if not data.get("name", "").strip():
        return False, "Machinery Name is required."
    
    rows = load_machinery()
    for r in rows:
        if r.get("MACHINERY ID", "").strip().upper() == mac_id.upper():
            return False, f"Machinery with ID '{mac_id}' already exists."
    
    new_row = dict_to_row(data)
    rows.append(new_row)
    save_machinery(rows)
    return True, row_to_dict(new_row)

def update_machinery_api(mac_id, data):
    rows = load_machinery()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("MACHINERY ID", "").strip().upper() == str(mac_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Machinery ID '{mac_id}' not found."
    
    current = rows[found_idx]
    new_id = str(data.get("id", mac_id)).strip()
    
    if new_id.upper() != str(mac_id).strip().upper():
        for r in rows:
            if r.get("MACHINERY ID", "").strip().upper() == new_id.upper():
                return False, f"Machinery with ID '{new_id}' already exists."

    curr_dict = row_to_dict(current)
    updated_dict = {
        "id": new_id,
        "name": data.get("name", curr_dict["name"]),
        "manufacturer": data.get("manufacturer", curr_dict["manufacturer"]),
        "category": data.get("category", curr_dict["category"]),
        "quantity": data.get("quantity", curr_dict["quantity"]),
        "dateOfPurchase": data.get("dateOfPurchase", curr_dict["dateOfPurchase"]),
        "price": data.get("price", curr_dict["price"])
    }
    
    rows[found_idx] = dict_to_row(updated_dict)
    save_machinery(rows)
    return True, row_to_dict(rows[found_idx])

def delete_machinery_api(mac_id):
    rows = load_machinery()
    found_idx = -1
    for i, r in enumerate(rows):
        if r.get("MACHINERY ID", "").strip().upper() == str(mac_id).strip().upper():
            found_idx = i
            break
            
    if found_idx == -1:
        return False, f"Machinery ID '{mac_id}' not found."
    
    removed = rows.pop(found_idx)
    save_machinery(rows)
    return True, row_to_dict(removed)

def main():
    print("Machinery Management Module")

if __name__ == "__main__":
    main()
