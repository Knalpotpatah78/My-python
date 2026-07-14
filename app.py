import json
import os
import uuid

DATA_FILE = os.path.join(os.path.dirname(__file__), "data.json")


def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_data(records):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2)


def list_records(records):
    if not records:
        print("No records found.")
        return
    print("\nCurrent records:")
    for record in records:
        print(f"- id: {record['id']}, name: {record['name']}, email: {record['email']}, phone: {record['phone']}")
    print()


def create_record(records):
    name = input("Name: ").strip()
    email = input("Email: ").strip()
    phone = input("Phone: ").strip()
    if not name:
        print("Name is required.")
        return
    record = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "phone": phone,
    }
    records.append(record)
    save_data(records)
    print(f"Created record with id {record['id']}.\n")


def read_record(records):
    record_id = input("Record id: ").strip()
    record = next((r for r in records if r["id"] == record_id), None)
    if record is None:
        print("Record not found.\n")
        return
    print("\nRecord details:")
    print(f"id: {record['id']}")
    print(f"name: {record['name']}")
    print(f"email: {record['email']}")
    print(f"phone: {record['phone']}\n")


def update_record(records):
    record_id = input("Record id: ").strip()
    record = next((r for r in records if r["id"] == record_id), None)
    if record is None:
        print("Record not found.\n")
        return
    print("Press Enter to keep the current value.")
    name = input(f"Name [{record['name']}]: ").strip() or record["name"]
    email = input(f"Email [{record['email']}]: ").strip() or record["email"]
    phone = input(f"Phone [{record['phone']}]: ").strip() or record["phone"]
    record.update({"name": name, "email": email, "phone": phone})
    save_data(records)
    print("Record updated.\n")


def delete_record(records):
    record_id = input("Record id: ").strip()
    index = next((i for i, r in enumerate(records) if r["id"] == record_id), None)
    if index is None:
        print("Record not found.\n")
        return
    records.pop(index)
    save_data(records)
    print("Record deleted.\n")


def main():
    actions = {
        "1": ("List records", list_records),
        "2": ("Create record", create_record),
        "3": ("Read record", read_record),
        "4": ("Update record", update_record),
        "5": ("Delete record", delete_record),
        "0": ("Exit", None),
    }
    while True:
        print("\nPython CRUD Application")
        for key, (label, _) in actions.items():
            print(f"{key}. {label}")
        choice = input("Choose an action: ").strip()
        if choice == "0":
            print("Goodbye!")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid choice. Try again.\n")
            continue
        records = load_data()
        action[1](records)


if __name__ == "__main__":
    main()
