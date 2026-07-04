import csv
from pathlib import Path


CSV_PATH = Path("medicines.csv")

FIELDNAMES = [
    "MEDICINE ID",
    "MEDICINE NAME",
    "GENIRIC NAME ",
    "CATEGORY",
    "EXPIRY DATE",
    "MANNUFACTURER",
    "PRICE",
]



def load_medicines(path: Path):
    medicines = []
    if not path.exists():
        return medicines
    with path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            medicines.append(row)
    return medicines



def save_medicines(path: Path, medicines):
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(medicines)


def print_all(medicines):
    if not medicines:
        print("No records found.")
        return
    for m in medicines:
        print("-" * 60)
        for k in FIELDNAMES:
            print(f"{k}: {m.get(k, '')}")
    print("-" * 60)


def find_by_id(medicines, mid):
    for m in medicines:
        if m.get("MEDICINE ID") == mid:
            return m
    return None



def add_medicine(medicines):
    print("Enter new medicine details:")
    new_m = {}
    for field in FIELDNAMES:
        new_m[field] = input(f"{field}: ")
    medicines.append(new_m)
    print("New medicine added:")
    for k in FIELDNAMES:
        print(f"{k}: {new_m[k]}")


def delete_medicine(medicines):
    mid = input("Enter MEDICINE ID to delete: ")
    medicine = find_by_id(medicines, mid)
    if not medicine:
        print("MEDICINE ID not found.")
        return
    medicines.remove(medicine)
    print("Medicine deleted:")
    for k in FIELDNAMES:
        print(f"{k}: {medicine[k]}")


def modify_medicine(medicines):
    mid = input("Enter MEDICINE ID to modify: ")
    medicine = find_by_id(medicines, mid)
    if not medicine:
        print("MEDICINE ID not found.")
        return

    print("Current data:")
    for k in FIELDNAMES:
        print(f"{k}: {medicine.get(k, '')}")

    print("\nEnter new data (leave blank to keep old value):")
    for field in FIELDNAMES:
        new_val = input(f"{field} ({medicine.get(field, '')}): ")
        if new_val.strip() != "":
            medicine[field] = new_val

    print("Medicine updated:")
    for k in FIELDNAMES:
        print(f"{k}: {medicine[k]}")


def modify_price_and_expiry(medicines):
    mid = input("Enter MEDICINE ID to modify price and expiry date: ")
    medicine = find_by_id(medicines, mid)
    if not medicine:
        print("MEDICINE ID not found.")
        return

    print("Current data:")
    print(f"EXPIRY DATE: {medicine.get('EXPIRY DATE', '')}")
    print(f"PRICE: {medicine.get('PRICE', '')}")

    new_expiry = input(f"New EXPIRY DATE ({medicine.get('EXPIRY DATE', '')}): ")
    new_price = input(f"New PRICE ({medicine.get('PRICE', '')}): ")

    if new_expiry.strip() != "":
        medicine["EXPIRY DATE"] = new_expiry
    if new_price.strip() != "":
        medicine["PRICE"] = new_price

    print("Medicine updated:")
    print(f"MEDICINE ID: {medicine.get('MEDICINE ID')}")
    print(f"EXPIRY DATE: {medicine.get('EXPIRY DATE')}")
    print(f"PRICE: {medicine.get('PRICE')}")


def main():
    while True:
        print("\nMENU")
        print("1. Read all medicines")
        print("2. Add new medicine")
        print("3. Remove medicine by ID")
        print("4. Modify medicine data")
        print("5. Modify price and expiry date only")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Exiting program.")
            break

        medicines = load_medicines(CSV_PATH)

        if choice == "1":
            print_all(medicines)

        elif choice == "2":
            add_medicine(medicines)
            save_medicines(CSV_PATH, medicines)

        elif choice == "3":
            delete_medicine(medicines)
            save_medicines(CSV_PATH, medicines)

        elif choice == "4":
            modify_medicine(medicines)
            save_medicines(CSV_PATH, medicines)

        elif choice == "5":
            modify_price_and_expiry(medicines)
            save_medicines(CSV_PATH, medicines)

        else:
            print("Invalid choice. Please enter 0–5.")


if __name__ == "__main__":
    main()
