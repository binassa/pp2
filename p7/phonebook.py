from connect import connect

# ---------------- CREATE TABLE ----------------
def create_table():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50),
            phone VARCHAR(20) UNIQUE
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# ---------------- INSERT FROM USER ----------------
def insert_from_console():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()


# ---------------- INSERT FROM CSV ----------------
def insert_from_csv(file_name="contacts.csv"):
    import csv

    conn = connect()
    cur = conn.cursor()

    with open(file_name, newline="") as file:
        reader = csv.reader(file)
        for row in reader:
            name, phone = row
            cur.execute(
                "INSERT INTO phonebook (first_name, phone) VALUES (%s, %s)",
                (name, phone)
            )

    conn.commit()
    cur.close()
    conn.close()


# ---------------- UPDATE CONTACT ----------------
def update_contact():
    old_phone = input("Enter phone to update: ")
    new_name = input("New name (or press Enter to skip): ")
    new_phone = input("New phone (or press Enter to skip): ")

    conn = connect()
    cur = conn.cursor()

    if new_name:
        cur.execute(
            "UPDATE phonebook SET first_name=%s WHERE phone=%s",
            (new_name, old_phone)
        )

    if new_phone:
        cur.execute(
            "UPDATE phonebook SET phone=%s WHERE phone=%s",
            (new_phone, old_phone)
        )

    conn.commit()
    cur.close()
    conn.close()


# ---------------- SEARCH CONTACTS ----------------
def search_contacts():
    print("1 - by name")
    print("2 - by phone prefix")
    choice = input("Choose: ")

    conn = connect()
    cur = conn.cursor()

    if choice == "1":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE first_name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "2":
        prefix = input("Enter prefix: ")
        cur.execute(
            "SELECT * FROM phonebook WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    results = cur.fetchall()
    for r in results:
        print(r)

    cur.close()
    conn.close()


# ---------------- DELETE CONTACT ----------------
def delete_contact():
    value = input("Enter name or phone to delete: ")

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM phonebook WHERE first_name=%s OR phone=%s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()


# ---------------- MENU ----------------
def menu():
    create_table()

    while True:
        print("\nPHONEBOOK MENU")
        print("1. Add contact (console)")
        print("2. Import from CSV")
        print("3. Update contact")
        print("4. Search contacts")
        print("5. Delete contact")
        print("0. Exit")

        choice = input("Select: ")

        if choice == "1":
            insert_from_console()
        elif choice == "2":
            insert_from_csv()
        elif choice == "3":
            update_contact()
        elif choice == "4":
            search_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break


if __name__ == "__main__":
    menu()