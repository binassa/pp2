from connectt import get_connection


def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            first_name VARCHAR(50) NOT NULL,
            last_name  VARCHAR(50) NOT NULL,
            phone      VARCHAR(20) NOT NULL,
            UNIQUE(first_name, last_name)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def load_sql_file(filename):
    conn = get_connection()
    cur = conn.cursor()

    with open(filename, "r", encoding="utf-8") as f:
        sql = f.read()
        cur.execute(sql)

    conn.commit()
    cur.close()
    conn.close()


def upsert_contact(first_name, last_name, phone):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL upsert_contact(%s, %s, %s);", (first_name, last_name, phone))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact inserted or updated successfully.")


def search_by_pattern(pattern):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
    rows = cur.fetchall()

    print("\nSearch results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def get_paginated(limit, offset):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s);", (limit, offset))
    rows = cur.fetchall()

    print("\nPaginated results:")
    for row in rows:
        print(row)

    cur.close()
    conn.close()


def insert_many_contacts():
    conn = get_connection()
    cur = conn.cursor()

    first_names = ["Aida", "John", "Sara"]
    last_names = ["Nurm", "Smith", "Lee"]
    phones = ["+77771234567", "123", "+77005554433"]

    cur.execute(
        "CALL insert_many_contacts(%s, %s, %s, %s);",
        (first_names, last_names, phones, "invalid_cursor")
    )

    cur.execute("FETCH ALL FROM invalid_cursor;")
    invalid_rows = cur.fetchall()

    conn.commit()

    print("\nInvalid rows:")
    for row in invalid_rows:
        print(row)

    cur.close()
    conn.close()


def delete_contact(value):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("CALL delete_contact(%s);", (value,))

    conn.commit()
    cur.close()
    conn.close()
    print("Contact deleted if matched.")


def menu():
    while True:
        print("\n===== PHONEBOOK MENU =====")
        print("1. Create table")
        print("2. Load functions.sql")
        print("3. Load procedures.sql")
        print("4. Insert or update one contact")
        print("5. Search by pattern")
        print("6. Insert many contacts")
        print("7. Show paginated contacts")
        print("8. Delete by username or phone")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_table()

        elif choice == "2":
            load_sql_file("functions.sql")
            print("Functions loaded successfully.")

        elif choice == "3":
            load_sql_file("procedures.sql")
            print("Procedures loaded successfully.")

        elif choice == "4":
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            phone = input("Enter phone: ")
            upsert_contact(first_name, last_name, phone)

        elif choice == "5":
            pattern = input("Enter search pattern: ")
            search_by_pattern(pattern)

        elif choice == "6":
            insert_many_contacts()

        elif choice == "7":
            limit = int(input("Enter LIMIT: "))
            offset = int(input("Enter OFFSET: "))
            get_paginated(limit, offset)

        elif choice == "8":
            value = input("Enter first name, last name, or phone to delete: ")
            delete_contact(value)

        elif choice == "9":
            print("Goodbye.")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    menu()