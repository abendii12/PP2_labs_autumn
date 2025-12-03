import psycopg2
import csv
import os


def connect():
    return psycopg2.connect(
        host="localhost",
        database="phonebook_db",  
        user="postgres",
        password="28AMI!11.2k5"   
    )

def create_table():
    conn = connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS phonebook (
            id SERIAL PRIMARY KEY,
            name VARCHAR(50),
            surname VARCHAR(50),
            phone VARCHAR(20)
        );
    """)
    conn.commit()
    conn.close()
    print("Table created successfully.")

def insert_from_csv(filename):
    conn = connect()
    cur = conn.cursor()

    
    script_dir = os.path.dirname(__file__)
    csv_path = os.path.join(script_dir, filename)

    if not os.path.exists(csv_path):
        print(f"CSV file not found: {csv_path}")
        return

    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader, None)  
        for row in reader:
            if len(row) >= 3:  
                name, surname, phone = row
                cur.execute(
                    "INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)",
                    (name, surname, phone)
                )

    conn.commit()
    conn.close()
    print("CSV data inserted successfully.")


def query_data():
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM phonebook ORDER BY id")
    rows = cur.fetchall()
    print("\n--- PHONEBOOK DATA ---")
    for r in rows:
        print(f"ID: {r[0]} | Name: {r[1]} | Surname: {r[2]} | Phone: {r[3]}")
    print("----------------------\n") #форматированный вывод записи
    conn.close()

def insert_from_console():
    name = input("Enter name: ")
    surname = input("Enter surname: ")
    phone = input("Enter phone: ")
    conn = connect()
    cur = conn.cursor()
    cur.execute("INSERT INTO phonebook (name, surname, phone) VALUES (%s, %s, %s)", (name, surname, phone))
    conn.commit()
    conn.close()
    print("Data inserted.")


def update_data():
    conn = connect()
    cur = conn.cursor()
    field = input("Update name, surname or phone? (name/surname/phone): ")
    old_val = input("Enter old value: ")
    new_val = input("Enter new value: ")

    if field == "name":
        cur.execute("UPDATE phonebook SET name=%s WHERE name=%s", (new_val, old_val))
    elif field == "surname":
        cur.execute("UPDATE phonebook SET surname=%s WHERE surname=%s", (new_val, old_val))
    elif field == "phone":
        cur.execute("UPDATE phonebook SET phone=%s WHERE phone=%s", (new_val, old_val))
    else:
        print("Invalid option")
        return

    conn.commit()
    conn.close()
    print("Updated successfully.")


def delete_data():
    conn = connect()
    cur = conn.cursor()
    print("Delete by: 1 - name, 2 - surname, 3 - phone")
    option = input("Choose: ")

    if option == "1":
        name = input("Enter name: ")
        cur.execute("DELETE FROM phonebook WHERE name=%s", (name,))
    elif option == "2":
        surname = input("Enter surname: ")
        cur.execute("DELETE FROM phonebook WHERE surname=%s", (surname,))
    elif option == "3":
        phone = input("Enter phone: ")
        cur.execute("DELETE FROM phonebook WHERE phone=%s", (phone,))
    else:
        print("Invalid option")
        return

    conn.commit()
    conn.close()
    print("Deleted successfully.")


def main():
    create_table()

    # Автоматическая вставка CSV и вывод таблицы
    insert_from_csv("phonebook.csv")  #положи CSV рядом с phonebook.py
    query_data()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1 - Insert from CSV")
        print("2 - Insert from console")
        print("3 - Update data")
        print("4 - Query data")
        print("5 - Delete data")
        print("0 - Exit")

        choice = input("Choose option: ")

        if choice == "1":
            insert_from_csv("phonebook.csv")
            query_data()
        elif choice == "2":
            insert_from_console()
            query_data()
        elif choice == "3":
            update_data()
            query_data()
        elif choice == "4":
            query_data()
        elif choice == "5":
            delete_data()
            query_data()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Wrong option")

if __name__ == "__main__":
    main()
