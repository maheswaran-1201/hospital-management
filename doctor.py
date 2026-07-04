import csv
from pathlib import Path


CSV_PATH = Path("doctors.csv")

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

def load_doctors(path: Path):
    doctors = []
    if not path.exists():
        return doctors
    with path.open(mode="r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            doctors.append(row)
    return doctors


def save_doctors(path: Path, doctors):
    with path.open(mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(doctors)


def print_all(doctors):
    if not doctors:
        print("No records found.")
        return
    for d in doctors:
        print("-" * 60)
        for k in FIELDNAMES:
            print(f"{k}: {d.get(k, '')}")
    print("-" * 60)


def find_by_id(doctors, doc_id):
    for d in doctors:
        if d.get("Doctor ID") == doc_id:
            return d
    return None


def add_doctor(doctors):
    print("Enter new doctor details:")
    new_doctor = {}
    for field in FIELDNAMES:
        new_doctor[field] = input(f"{field}: ")

    doctors.append(new_doctor)
    print("New doctor added:")
    for k in FIELDNAMES:
        print(f"{k}: {new_doctor[k]}")


def delete_doctor(doctors):
    doc_id = input("Enter Doctor ID to delete: ")
    doctor = find_by_id(doctors, doc_id)
    if not doctor:
        print("Doctor ID not found.")
        return
    doctors.remove(doctor)
    print("Doctor deleted:")
    for k in FIELDNAMES:
        print(f"{k}: {doctor[k]}")


def modify_all_fields(doctors):
    doc_id = input("Enter Doctor ID to modify: ")
    doctor = find_by_id(doctors, doc_id)
    if not doctor:
        print("Doctor ID not found.")
        return

    print("Current data:")
    for k in FIELDNAMES:
        print(f"{k}: {doctor.get(k, '')}")

    print("\nEnter new data (leave blank to keep old value):")
    for field in FIELDNAMES:
        new_val = input(f"{field} ({doctor.get(field, '')}): ")
        if new_val.strip() != "":
            doctor[field] = new_val

    print("Doctor updated:")
    for k in FIELDNAMES:
        print(f"{k}: {doctor[k]}")


def modify_contact_and_salary(doctors):
    doc_id = input("Enter Doctor ID to modify contact and salary: ")
    doctor = find_by_id(doctors, doc_id)
    if not doctor:
        print("Doctor ID not found.")
        return

    print("Current data:")
    print(f"Contact No: {doctor.get('Contact No', '')}")
    print(f"Salary (₹): {doctor.get('Salary (₹)', '')}")

    new_contact = input(f"New Contact No ({doctor.get('Contact No', '')}): ")
    new_salary = input(f"New Salary (₹) ({doctor.get('Salary (₹)', '')}): ")

    if new_contact.strip() != "":
        doctor["Contact No"] = new_contact
    if new_salary.strip() != "":
        doctor["Salary (₹)"] = new_salary

    print("Doctor updated:")
    print(f"Doctor ID: {doctor.get('Doctor ID')}")
    print(f"Contact No: {doctor.get('Contact No')}")
    print(f"Salary (₹): {doctor.get('Salary (₹)')}")


def main():
    while True:
        print("\nMENU")
        print("1. Read all doctors")
        print("2. Add new doctor")
        print("3. Remove doctor by ID")
        print("4. Modify all data of a doctor")
        print("5. Modify contact no and salary only")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "0":
            print("Exiting program.")
            break

        doctors = load_doctors(CSV_PATH)

        if choice == "1":
            print_all(doctors)

        elif choice == "2":
            add_doctor(doctors)
            save_doctors(CSV_PATH, doctors)

        elif choice == "3":
            delete_doctor(doctors)
            save_doctors(CSV_PATH, doctors)

        elif choice == "4":
            modify_all_fields(doctors)
            save_doctors(CSV_PATH, doctors)

        elif choice == "5":
            modify_contact_and_salary(doctors)
            save_doctors(CSV_PATH, doctors)

        else:
            print("Invalid choice. Please enter 0–5.")


if __name__ == "__main__":
    main()
