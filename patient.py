import csv
import os
from pathlib import Path

CSV_PATH = Path("patient.csv")

EXPECTED_FIELDS = ["PATIENT ID", "PATIENT NAME", "GENDER", "AGE", "CONTACT NO", "DATE OF ADMISSION", "DISEASE"]

def load_patients(path):
    patients = []
    with open(path, mode="r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [h.strip() for h in reader.fieldnames]
        for row in reader:
            norm_row = {k.strip(): (v.strip() if isinstance(v, str) else v) for k, v in row.items()}
            patients.append(norm_row)
    return patients, fieldnames

def save_patients(path, patients, fieldnames):
    out_fields = EXPECTED_FIELDS if all(h in fieldnames for h in EXPECTED_FIELDS) else fieldnames
    with open(path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=out_fields)
        writer.writeheader()
        for p in patients:
            row = {h: p.get(h, "") for h in out_fields}
            writer.writerow(row)

def print_all(patients, fieldnames):
    if not patients:
        print("No patients found.")
        return
    print("\nAll patients:")
    print(" | ".join(fieldnames))
    for p in patients:
        print(" | ".join(str(p.get(h, "")) for h in fieldnames))
    print()

def find_index_by_id(patients, pid):
    for i, p in enumerate(patients):
        if p.get("PATIENT ID", "").strip().upper() == pid.strip().upper():
            return i
    return -1

def input_nonempty(prompt):
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty. Try again.")

def add_patient(patients):
    print("\nEnter new patient details:")
    pid = input_nonempty("PATIENT ID (e.g., PAT051): ")
    if find_index_by_id(patients, pid) != -1:
        print("A patient with this ID already exists.")
        return
    name = input_nonempty("PATIENT NAME: ")
    gender = input_nonempty("GENDER (Male/Female/Other): ")
    age = input_nonempty("AGE: ")
    contact = input_nonempty("CONTACT NO: ")
    doa = input_nonempty("DATE OF ADMISSION (dd-mm-yyyy): ")
    disease = input_nonempty("DISEASE: ")
    patients.append({
        "PATIENT ID": pid,
        "PATIENT NAME": name,
        "GENDER": gender,
        "AGE": age,
        "CONTACT NO": contact,
        "DATE OF ADMISSION": doa,
        "DISEASE": disease
    })
    print("Patient added successfully.")

def remove_patient(patients):
    pid = input_nonempty("Enter PATIENT ID to remove: ")
    idx = find_index_by_id(patients, pid)
    if idx == -1:
        print("Patient ID not found.")
        return
    removed = patients.pop(idx)
    print(f"Removed patient: {removed.get('PATIENT NAME','')} ({pid})")

def modify_all_fields(patients):
    pid = input_nonempty("Enter PATIENT ID to modify: ")
    idx = find_index_by_id(patients, pid)
    if idx == -1:
        print("Patient ID not found.")
        return
    p = patients[idx]
    print("Press Enter to keep current value.")
    name = input(f"PATIENT NAME [{p.get('PATIENT NAME','')}]: ").strip() or p.get("PATIENT NAME","")
    gender = input(f"GENDER [{p.get('GENDER','')}]: ").strip() or p.get("GENDER","")
    age = input(f"AGE [{p.get('AGE','')}]: ").strip() or p.get("AGE","")
    contact = input(f"CONTACT NO [{p.get('CONTACT NO','')}]: ").strip() or p.get("CONTACT NO","")
    doa = input(f"DATE OF ADMISSION [{p.get('DATE OF ADMISSION','')}]: ").strip() or p.get("DATE OF ADMISSION","")
    disease = input(f"DISEASE [{p.get('DISEASE','')}]: ").strip() or p.get("DISEASE","")
    patients[idx] = {
        "PATIENT ID": p.get("PATIENT ID", pid),  # keep same ID
        "PATIENT NAME": name,
        "GENDER": gender,
        "AGE": age,
        "CONTACT NO": contact,
        "DATE OF ADMISSION": doa,
        "DISEASE": disease
    }
    print("Patient updated successfully.")

def modify_disease_contact(patients):
    pid = input_nonempty("Enter PATIENT ID to modify disease and contact: ")
    idx = find_index_by_id(patients, pid)
    if idx == -1:
        print("Patient ID not found.")
        return
    p = patients[idx]
    print("Press Enter to keep current value.")
    disease = input(f"DISEASE [{p.get('DISEASE','')}]: ").strip() or p.get("DISEASE","")
    contact = input(f"CONTACT NO [{p.get('CONTACT NO','')}]: ").strip() or p.get("CONTACT NO","")
    p["DISEASE"] = disease
    p["CONTACT NO"] = contact
    print("Disease and contact updated successfully.")

def ensure_file_exists(path):
    if not os.path.exists(path):
        with open(path, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=EXPECTED_FIELDS)
            writer.writeheader()

def main():
    ensure_file_exists(CSV_PATH)
    patients, fieldnames = load_patients(CSV_PATH)

    print("Patient Management Menu")
    while True:
        print("\n1. Show all patients")
        print("2. Add a new patient")
        print("3. Remove a patient by ID")
        print("4. Modify all data by ID")
        print("5. Modify disease and contact by ID")
        print("0. Exit")
        choice = input("Enter your choice (1-5) and 0 to exit: ").strip()

        if choice == "1":
            print_all(patients, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "2":
            add_patient(patients)
            save_patients(CSV_PATH, patients, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "3":
            remove_patient(patients)
            save_patients(CSV_PATH, patients, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "4":
            modify_all_fields(patients)
            save_patients(CSV_PATH, patients, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "5":
            modify_disease_contact(patients)
            save_patients(CSV_PATH, patients, fieldnames if fieldnames else EXPECTED_FIELDS)
        elif choice == "0":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a number from 0-5.")

if __name__ == "__main__":
    main()
