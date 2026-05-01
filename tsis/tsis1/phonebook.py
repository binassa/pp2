from connect import get_connection
import json
import csv


def load_sql_file(filename):
    conn = get_connection()
    if conn is None:
        print("Database connection failed.")
        return
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as file:
        sql = file.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()


def create_schema():
    load_sql_file("schema.sql")
    print("Schema created successfully.")


def load_procedures():
    load_sql_file("procedures.sql")
    print("Procedures and functions loaded successfully.")


def get_group_id(cur, group_name):
    cur.execute(
        "INSERT INTO groups(name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (group_name,)
    )

    cur.execute("SELECT id FROM groups WHERE name = %s;", (group_name,))
    return cur.fetchone()[0]


def add_contact():
    conn = get_connection()
    cur = conn.cursor()

    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    birthday = input("Enter birthday YYYY-MM-DD: ")
    group_name = input("Enter group Family/Work/Friend/Other: ")

    group_id = get_group_id(cur, group_name)

    cur.execute("""
        INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (first_name, last_name)
        DO UPDATE SET
            email = EXCLUDED.email,
            birthday = EXCLUDED.birthday,
            group_id = EXCLUDED.group_id;
    """, (first_name, last_name, email, birthday, group_id))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact inserted or updated successfully.")


def add_phone():
    conn = get_connection()
    cur = conn.cursor()

    contact_name = input("Enter full contact name: ")
    phone = input("Enter phone number: ")
    phone_type = input("Enter phone type home/work/mobile: ")

    cur.execute("CALL add_phone(%s, %s, %s);", (contact_name, phone, phone_type))

    conn.commit()
    cur.close()
    conn.close()

    print("Phone added successfully.")


def move_to_group():
    conn = get_connection()
    cur = conn.cursor()

    contact_name = input("Enter full contact name: ")
    group_name = input("Enter new group name: ")

    cur.execute("CALL move_to_group(%s, %s);", (contact_name, group_name))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact moved to group successfully.")


def search_contacts_console():
    conn = get_connection()
    cur = conn.cursor()

    query = input("Enter search text: ")

    cur.execute("SELECT * FROM search_contacts(%s);", (query,))
    rows = cur.fetchall()

    print("\nSearch results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def filter_by_group():
    conn = get_connection()
    cur = conn.cursor()

    group_name = input("Enter group name: ")

    cur.execute("""
        SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE LOWER(g.name) = LOWER(%s);
    """, (group_name,))

    rows = cur.fetchall()

    print("\nContacts in group:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def search_by_email():
    conn = get_connection()
    cur = conn.cursor()

    email_part = input("Enter email search text: ")

    cur.execute("""
        SELECT first_name, last_name, email, birthday
        FROM contacts
        WHERE email ILIKE %s;
    """, (f"%{email_part}%",))

    rows = cur.fetchall()

    print("\nEmail search results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def sort_contacts():
    conn = get_connection()
    cur = conn.cursor()

    print("Sort by:")
    print("1. Name")
    print("2. Birthday")
    print("3. Date added")

    choice = input("Choose: ")

    if choice == "1":
        order_by = "first_name, last_name"
    elif choice == "2":
        order_by = "birthday"
    elif choice == "3":
        order_by = "date_added"
    else:
        print("Invalid choice.")
        return

    cur.execute(f"""
        SELECT first_name, last_name, email, birthday, date_added
        FROM contacts
        ORDER BY {order_by};
    """)

    rows = cur.fetchall()

    print("\nSorted contacts:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def paginated_navigation():
    conn = get_connection()
    cur = conn.cursor()

    limit = int(input("Enter page size: "))
    offset = 0

    while True:
        cur.execute("""
            SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id = g.id
            ORDER BY c.id
            LIMIT %s OFFSET %s;
        """, (limit, offset))

        rows = cur.fetchall()

        print("\nPage results:")
        if not rows:
            print("No contacts on this page.")
        else:
            for row in rows:
                print(row)

        command = input("\nnext / prev / quit: ").lower()

        if command == "next":
            offset += limit
        elif command == "prev":
            offset = max(0, offset - limit)
        elif command == "quit":
            break
        else:
            print("Invalid command.")

    cur.close()
    conn.close()


def export_to_json():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.first_name,
            c.last_name,
            c.email,
            c.birthday,
            g.name
        FROM contacts c
        LEFT JOIN groups g ON c.group_id = g.id
        ORDER BY c.id;
    """)

    contacts = []

    for contact in cur.fetchall():
        contact_id = contact[0]

        cur.execute("""
            SELECT phone, type
            FROM phones
            WHERE contact_id = %s;
        """, (contact_id,))

        phones = [
            {"phone": phone, "type": phone_type}
            for phone, phone_type in cur.fetchall()
        ]

        contacts.append({
            "first_name": contact[1],
            "last_name": contact[2],
            "email": contact[3],
            "birthday": str(contact[4]) if contact[4] else None,
            "group": contact[5],
            "phones": phones
        })

    filename = input("Enter JSON filename to save: ")

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(contacts, file, indent=4)

    cur.close()
    conn.close()

    print("Contacts exported successfully.")


def import_from_json():
    conn = get_connection()
    cur = conn.cursor()

    filename = input("Enter JSON filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        contacts = json.load(file)

    for contact in contacts:
        first_name = contact["first_name"]
        last_name = contact["last_name"]

        cur.execute("""
            SELECT id FROM contacts
            WHERE first_name = %s AND last_name = %s;
        """, (first_name, last_name))

        existing = cur.fetchone()

        if existing:
            action = input(f"{first_name} {last_name} exists. skip/overwrite: ").lower()

            if action == "skip":
                continue

        group_id = get_group_id(cur, contact.get("group") or "Other")

        cur.execute("""
            INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (first_name, last_name)
            DO UPDATE SET
                email = EXCLUDED.email,
                birthday = EXCLUDED.birthday,
                group_id = EXCLUDED.group_id
            RETURNING id;
        """, (
            first_name,
            last_name,
            contact.get("email"),
            contact.get("birthday"),
            group_id
        ))

        contact_id = cur.fetchone()[0]

        if existing:
            cur.execute("DELETE FROM phones WHERE contact_id = %s;", (contact_id,))

        for phone_data in contact.get("phones", []):
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (
                contact_id,
                phone_data["phone"],
                phone_data["type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("JSON imported successfully.")


def import_from_csv():
    conn = get_connection()
    cur = conn.cursor()

    filename = input("Enter CSV filename: ")

    with open(filename, "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            group_id = get_group_id(cur, row["group"])

            cur.execute("""
                INSERT INTO contacts(first_name, last_name, email, birthday, group_id)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (first_name, last_name)
                DO UPDATE SET
                    email = EXCLUDED.email,
                    birthday = EXCLUDED.birthday,
                    group_id = EXCLUDED.group_id
                RETURNING id;
            """, (
                row["first_name"],
                row["last_name"],
                row["email"],
                row["birthday"],
                group_id
            ))

            contact_id = cur.fetchone()[0]

            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s);
            """, (
                contact_id,
                row["phone"],
                row["phone_type"]
            ))

    conn.commit()
    cur.close()
    conn.close()

    print("CSV imported successfully.")


def delete_contact():
    conn = get_connection()
    cur = conn.cursor()

    value = input("Enter first name, last name, email, or phone: ")

    cur.execute("""
        DELETE FROM contacts
        WHERE id IN (
            SELECT c.id
            FROM contacts c
            LEFT JOIN phones p ON c.id = p.contact_id
            WHERE c.first_name ILIKE %s
               OR c.last_name ILIKE %s
               OR c.email ILIKE %s
               OR p.phone ILIKE %s
        );
    """, (value, value, value, value))

    conn.commit()
    cur.close()
    conn.close()

    print("Contact deleted if matched.")


def menu():
    while True:
        print("\n===== EXTENDED PHONEBOOK MENU =====")
        print("1. Create schema")
        print("2. Load procedures.sql")
        print("3. Add or update contact")
        print("4. Add phone to contact")
        print("5. Move contact to group")
        print("6. Search contacts")
        print("7. Filter by group")
        print("8. Search by email")
        print("9. Sort contacts")
        print("10. Paginated navigation")
        print("11. Export to JSON")
        print("12. Import from JSON")
        print("13. Import from CSV")
        print("14. Delete contact")
        print("15. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_schema()
        elif choice == "2":
            load_procedures()
        elif choice == "3":
            add_contact()
        elif choice == "4":
            add_phone()
        elif choice == "5":
            move_to_group()
        elif choice == "6":
            search_contacts_console()
        elif choice == "7":
            filter_by_group()
        elif choice == "8":
            search_by_email()
        elif choice == "9":
            sort_contacts()
        elif choice == "10":
            paginated_navigation()
        elif choice == "11":
            export_to_json()
        elif choice == "12":
            import_from_json()
        elif choice == "13":
            import_from_csv()
        elif choice == "14":
            delete_contact()
        elif choice == "15":
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()