import csv
import os
from pathlib import Path

CSV_PATH = Path("staff.csv")

EXPECTED_FIELDS = [
    "STAFF ID",
    "STAFF NAME",
    "GENDER",
    "AGE",
    "CONTACT NO",
    "DESIGNNATION",
    "DATE JOINED",
    "salary"
]

def ensure_file_exists(path):
    if not os.path.exists(path):
        with open(path, mode="w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_FIELDS)
            writer.writeheader()

def load_staff(path):
    staff_list = []
    with open(path, mode="r", newline="") as f:
        reader = csv.DictReader(f)
        fieldnames = [h.strip() for h in reader.fieldnames]
        for row in reader:
            norm_row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
            staff_list.append(norm_row)
    return staff_list, fieldnames

def save_staff(path, staff_list, fieldnames):
    out_fields = EXPECTED_FIELDS if all(h in fieldnames for h in EXPECTED_FIELDS) else fieldnames
    with open(path, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for s in staff_list:
            row = {h: s.get(h, "") for h in out_fields}
            writer.writerow(row)

def print_all(staff_list, fieldnames):
    if not staff_list:
        print("No staff records found.")
        return
    print("\nAll staff:")
    print(" | ".join(fieldnames))
    for s in staff_list:
        print(" | ".join(str(s.get(h, "")) for h in fieldnames))
    print()

def find_index_by_id(staff_list, sid):
    for i, s in enumerate(staff_list):
        if s.get("STAFF ID", "").strip().upper() == sid.strip().upper():
            return i
    return -1

def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")

def add_staff(staff_list):
    print("\nEnter new staff details:")
    sid = input_nonempty("STAFF ID (e.g., ST051): ")
    if find_index_by_id(staff_list, sid) != -1:
        print("A staff member with this ID already exists.")
        return
    name = input_nonempty("STAFF NAME: ")
    gender = input_nonempty("GENDER (Male/Female/Other): ")
    age = input_nonempty("AGE: ")
    contact = input_nonempty("CONTACT NO: ")
    designation = input_nonempty("DESIGNNATION: ")
    date_joined = input_nonempty("DATE JOINED (dd-mm-yyyy): ")
    salary = input_nonempty("salary: ")
    staff_list.append({
        "STAFF ID": sid,
        "STAFF NAME": name,
        "GENDER": gender,
        "AGE": age,
        "CONTACT NO": contact,
        "DESIGNNATION": designation,
        "DATE JOINED": date_joined,
        "salary": salary
    })
    print("Staff added successfully.")

def remove_staff(staff_list):
    sid = input_nonempty("Enter STAFF ID to remove: ")
    idx = find_index_by_id(staff_list, sid)
    if idx == -1:
        print("Staff ID not found.")
        return
    removed = staff_list.pop(idx)
    print(f"Removed staff: {removed.get('STAFF NAME','')} ({sid})")

def modify_all_fields(staff_list):
    sid = input_nonempty("Enter STAFF ID to modify: ")
    idx = find_index_by_id(staff_list, sid)
    if idx == -1:
        print("Staff ID not found.")
        return
    s = staff_list[idx]
    print("Press Enter to keep current value.")
    name = input(f"STAFF NAME [{s.get('STAFF NAME','')}]: ").strip() or s.get("STAFF NAME", "")
    gender = input(f"GENDER [{s.get('GENDER','')}]: ").strip() or s.get("GENDER", "")
    age = input(f"AGE [{s.get('AGE','')}]: ").strip() or s.get("AGE", "")
    contact = input(f"CONTACT NO [{s.get('CONTACT NO','')}]: ").strip() or s.get("CONTACT NO", "")
    designation = input(f"DESIGNNATION [{s.get('DESIGNNATION','')}]: ").strip() or s.get("DESIGNNATION", "")
    date_joined = input(f"DATE JOINED [{s.get('DATE JOINED','')}]: ").strip() or s.get("DATE JOINED", "")
    salary = input(f"salary [{s.get('salary','')}]: ").strip() or s.get("salary", "")
    staff_list[idx] = {
        "STAFF ID": s.get("STAFF ID", sid),
        "STAFF NAME": name,
        "GENDER": gender,
        "AGE": age,
        "CONTACT NO": contact,
        "DESIGNNATION": designation,
        "DATE JOINED": date_joined,
        "salary": salary
    }
    print("Staff record updated successfully.")

def modify_salary_contact_designation(staff_list):
    sid = input_nonempty("Enter STAFF ID to modify salary, CONTACT NO, and DESIGNNATION: ")
    idx = find_index_by_id(staff_list, sid)
    if idx == -1:
        print("Staff ID not found.")
        return
    s = staff_list[idx]
    print("Press Enter to keep current value.")
    salary = input(f"salary [{s.get('salary','')}]: ").strip() or s.get("salary", "")
    contact = input(f"CONTACT NO [{s.get('CONTACT NO','')}]: ").strip() or s.get("CONTACT NO", "")
    designation = input(f"DESIGNNATION [{s.get('DESIGNNATION','')}]: ").strip() or s.get("DESIGNNATION", "")
    s["salary"] = salary
    s["CONTACT NO"] = contact
    s["DESIGNNATION"] = designation
    print("Salary, contact number, and designation updated successfully.")

def main():
    ensure_file_exists(CSV_PATH)
    staff_list, fieldnames = load_staff(CSV_PATH)

    print("Staff Management Menu")
    while True:
        print("\n1. Show all staff")
        print("2. Add a new staff")
        print("3. Remove a staff by ID")
        print("4. Modify all data by ID")
        print("5. Modify salary, CONTACT NO, and DESIGNNATION by ID")
        print("0. Exit")

        choice = input("Enter your choice (1-5) and 0 to exit: ").strip()

        if choice == "1":
            print_all(staff_list, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "2":
            add_staff(staff_list)
            save_staff(CSV_PATH, staff_list, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "3":
            remove_staff(staff_list)
            save_staff(CSV_PATH, staff_list, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "4":
            modify_all_fields(staff_list)
            save_staff(CSV_PATH, staff_list, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "5":
            modify_salary_contact_designation(staff_list)
            save_staff(CSV_PATH, staff_list, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 0-5.")

if __name__ == "__main__":
    main()
