import doctor
import machinery
import medicine
import patient
import staff

def main():
    while True:
        print("\nMAIN MENU")
        print("1. Doctor management")
        print("2. Machinery management")
        print("3. Medicine management")
        print("4. Patient management")
        print("5. Staff management")
        print("0. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "0":
            print("**********************************Exiting the program**********************************")
            break

        elif choice == "1":
            doctor.main()

        elif choice == "2":
            machinery.main()

        elif choice == "3":
            medicine.main()

        elif choice == "4":
            patient.main()

        elif choice == "5":
            staff.main()

        else:
            print("Invalid choice. Please enter 0–5.")


if __name__ == "__main__":
    main()
