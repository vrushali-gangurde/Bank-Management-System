
from decimal import Decimal, InvalidOperation
from database import connect_db


def create_account():
    print("\n--- Create Bank Account ---")

    try:
        customer_id = int(input("Enter registered Customer ID: "))
        opening_balance = Decimal(input("Enter opening balance: "))

        if opening_balance < 0:
            print("Opening balance cannot be negative.")
            return

    except (ValueError, InvalidOperation):
        print("Please enter valid numeric values.")
        return

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            "SELECT customer_id FROM customers WHERE customer_id = %s",
            (customer_id,)
        )

        if cur.fetchone() is None:
            print("Customer not found. Register the customer first.")
            return

        cur.execute(
            """
            INSERT INTO accounts
                (customer_id, name, phone, address, balance)
            SELECT customer_id, full_name, phone, address, %s
            FROM customers
            WHERE customer_id = %s
            RETURNING account_no
            """,
            (opening_balance, customer_id)
        )

        account_no = cur.fetchone()[0]
        conn.commit()

        print("\nAccount created successfully!")
        print("Account Number:", account_no)

    except Exception as error:
        if conn:
            conn.rollback()
        print("Could not create account:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def check_balance():
    print("\n--- Check Account Balance ---")
    account_no = input("Enter account number: ").strip()

    if not account_no.isdigit():
        print("Please enter a valid account number.")
        return

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT name, balance
            FROM accounts
            WHERE account_no = %s
            """,
            (int(account_no),)
        )

        result = cur.fetchone()

        if result:
            print("Account Holder:", result[0])
            print("Available Balance:", result[1])
        else:
            print("Account not found.")

    except Exception as error:
        print("Could not check balance:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()