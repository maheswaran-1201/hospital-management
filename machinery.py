import csv
from pathlib import Path

CSV_PATH = Path("machinery.csv")
FIELDNAMES = [
    "MACHINERY ID",
    "MACHINERY NAME",
    "MANUFACTURER",
    "CATEGORY",
    "QUANTITY",
    "DATE OF PURCHASE",
    "PRICE",
]


def load_machinery(path: Path):
    machines = []
    if not path.exists():
        return machines
    with path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            machines.append(row)
    return machines


def save_machinery(path: Path, machines):
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(machines)


def print_all(machines):
    if not machines:
        print("No records found.")
        return
    for m in machines:
        print("-" * 60)
        for k in FIELDNAMES:
            print(f"{k}: {m.get(k, '')}")
    print("-" * 60)


def find_by_id(machines, mid):
    for m in machines:
        if m.get("MACHINERY ID") == mid:
            return m
    return None


def add_machinery(machines):
    print("Enter new machinery details:")
    new_m = {}
    for field in FIELDNAMES:
        new_m[field] = input(f"{field}: ")
    machines.append(new_m)
    print("New machinery added:")
    for k in FIELDNAMES:
        print(f"{k}: {new_m[k]}")


def delete_machinery(machines):
    mid = input("Enter MACHINERY ID to delete: ")
    machine = find_by_id(machines, mid)
    if not machine:
        print("MACHINERY ID not found.")
        return
    machines.remove(machine)
    print("Machinery deleted:")
    for k in FIELDNAMES:
        print(f"{k}: {machine[k]}")


def modify_machinery(machines):
    mid = input("Enter MACHINERY ID to modify: ")
    machine = find_by_id(machines, mid)
    if not machine:
        print("MACHINERY ID not found.")
        return

    print("Current data:")
    for k in FIELDNAMES:
        print(f"{k}: {machine.get(k, '')}")

    print("\nEnter new data (leave blank to keep old value):")
    for field in FIELDNAMES:
        new_val = input(f"{field} ({machine.get(field, '')}): ")
        if new_val.strip() != "":
            machine[field] = new_val

    print("Machinery updated:")
    for k in FIELDNAMES:
        print(f"{k}: {machine[k]}")


def modify_price_and_quantity(machines):
    mid = input("Enter MACHINERY ID to modify price and quantity: ")
    machine = find_by_id(machines, mid)
    if not machine:
        print("MACHINERY ID not found.")
        return

    print("Current data:")
    print(f"QUANTITY: {machine.get('QUANTITY', '')}")
    print(f"PRICE: {machine.get('PRICE', '')}")

    new_qty = input(f"New QUANTITY ({machine.get('QUANTITY', '')}): ")
    new_price = input(f"New PRICE ({machine.get('PRICE', '')}): ")

    if new_qty.strip() != "":
        machine["QUANTITY"] = new_qty
    if new_price.strip() != "":
        machine["PRICE"] = new_price

    print("Machinery updated:")
    print(f"MACHINERY ID: {machine.get('MACHINERY ID')}")
    print(f"QUANTITY: {machine.get('QUANTITY')}")
    print(f"PRICE: {machine.get('PRICE')}")


def main():
    while True:
        print("\nMENU")
        print("1. Read all machinery")
        print("2. Add new machinery")
        print("3. Remove machinery by ID")
        print("4. Modify machinery data")
        print("5. Modify price and quantity only")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Exiting program.")
            break

        machines = load_machinery(CSV_PATH)

        if choice == "1":
            print_all(machines)

        elif choice == "2":
            add_machinery(machines)
            save_machinery(CSV_PATH, machines)

        elif choice == "3":
            delete_machinery(machines)
            save_machinery(CSV_PATH, machines)

        elif choice == "4":
            modify_machinery(machines)
            save_machinery(CSV_PATH, machines)

        elif choice == "5":
            modify_price_and_quantity(machines)
            save_machinery(CSV_PATH, machines)

        else:
            print("Invalid choice. Please enter 0–5.")


if __name__ == "__main__":
    main()
