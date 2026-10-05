
from decimal import Decimal, InvalidOperation
from database import connect_db


def deposit_money():
    process_transaction("DEPOSIT")


def withdraw_money():
    process_transaction("WITHDRAW")


def process_transaction(transaction_type):
    print(f"\n--- {transaction_type} MONEY ---")

    try:
        account_no = int(input("Enter account number: "))
        amount = Decimal(input("Enter amount: "))

        if account_no <= 0 or amount <= 0:
            print("Account number and amount must be positive.")
            return

    except (ValueError, InvalidOperation):
        print("Please enter valid numbers.")
        return

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        # Lock the account row while updating its balance.
        cur.execute(
            """
            SELECT balance
            FROM accounts
            WHERE account_no = %s
            FOR UPDATE
            """,
            (account_no,)
        )

        result = cur.fetchone()

        if result is None:
            print("Account not found.")
            conn.rollback()
            return

        current_balance = Decimal(str(result[0]))

        if transaction_type == "WITHDRAW" and current_balance < amount:
            print("Insufficient balance.")
            conn.rollback()
            return

        if transaction_type == "DEPOSIT":
            new_balance = current_balance + amount
            description = "Money deposited"
        else:
            new_balance = current_balance - amount
            description = "Money withdrawn"

        cur.execute(
            """
            UPDATE accounts
            SET balance = %s
            WHERE account_no = %s
            """,
            (new_balance, account_no)
        )

        cur.execute(
            """
            INSERT INTO transactions
                (account_no, transaction_type, amount, description)
            VALUES (%s, %s, %s, %s)
            RETURNING transaction_id
            """,
            (account_no, transaction_type, amount, description)
        )

        transaction_id = cur.fetchone()[0]
        conn.commit()

        print("\nTransaction successful!")
        print("Transaction ID:", transaction_id)
        print("Updated balance:", new_balance)

    except Exception as error:
        if conn:
            conn.rollback()
        print("Transaction failed:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def transaction_history():
    print("\n--- Transaction History ---")

    try:
        account_no = int(input("Enter account number: "))
        if account_no <= 0:
            print("Invalid account number.")
            return
    except ValueError:
        print("Please enter a valid account number.")
        return

    conn = None
    cur = None

    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute(
            """
            SELECT transaction_id, transaction_type, amount,
                   transaction_date, description
            FROM transactions
            WHERE account_no = %s
            ORDER BY transaction_date DESC, transaction_id DESC
            """,
            (account_no,)
        )

        rows = cur.fetchall()

        if not rows:
            print("No transactions found.")
            return

        for row in rows:
            print("-" * 35)
            print("Transaction ID:", row[0])
            print("Type:", row[1])
            print("Amount:", row[2])
            print("Date:", row[3])
            print("Description:", row[4] or "-")

    except Exception as error:
        print("Could not fetch history:", error)

    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()