
from database import connect_db


def add_customer():
    print("\n--- CUSTOMER REGISTRATION ---")

    full_name = input("Enter full name: ").strip()
    email = input("Enter email (optional): ").strip() or None
    phone = input("Enter phone number (optional): ").strip() or None
    address = input("Enter address (optional): ").strip() or None

    if not full_name:
        print("Error: Full name is required.")
        return

    conn = None
    cur = None

    try:
        print("Connecting to database...")

        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            INSERT INTO customers (full_name, email, phone, address)
            VALUES (%s, %s, %s, %s)
            RETURNING customer_id
            """,
            (full_name, email, phone, address)
        )

        result = cur.fetchone()
        conn.commit()

        print("\nCustomer registered successfully!")
        print("Customer ID:", result[0])
        print("Name:", full_name)

    except Exception as error:
        if conn:
            conn.rollback()

        print("\nCustomer registration failed!")
        print("Reason:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def view_customers():
    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT customer_id, full_name, email, phone, address
            FROM customers
            ORDER BY customer_id
            """
        )

        rows = cur.fetchall()

        print("\n--- REGISTERED CUSTOMERS ---")

        if not rows:
            print("No customers found.")
            return

        for row in rows:
            print("-" * 35)
            print("Customer ID:", row[0])
            print("Name:", row[1])
            print("Email:", row[2] or "Not provided")
            print("Phone:", row[3] or "Not provided")
            print("Address:", row[4] or "Not provided")

    except Exception as error:
        print("Could not fetch customers:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()