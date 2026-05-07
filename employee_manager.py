import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "employees.json"


def load_employees():
    if not DATA_FILE.exists():
        return []
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_employees(employees):
    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(employees, file, indent=2)


def add_employee(name, phone_number):
    employees = load_employees()
    employees.append({"name": name, "phone_number": phone_number})
    save_employees(employees)
    print(f"Added employee: {name} ({phone_number})")


def list_employees():
    employees = load_employees()
    if not employees:
        print("No employees stored yet.")
        return
    print("Stored employees:")
    for index, employee in enumerate(employees, start=1):
        print(f"{index}. {employee['name']} - {employee['phone_number']}")


def main():
    print("Employee Manager")
    print("1. Add employee")
    print("2. List employees")
    choice = input("Choose an option (1 or 2): ").strip()

    if choice == "1":
        name = input("Enter employee name: ").strip()
        phone_number = input("Enter phone number: ").strip()
        add_employee(name, phone_number)
    elif choice == "2":
        list_employees()
    else:
        print("Invalid choice. Please run the script again and choose 1 or 2.")


if __name__ == "__main__":
    main()
