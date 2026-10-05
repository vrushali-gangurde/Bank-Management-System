
from customer import add_customer, view_customers
from account import create_account, check_balance
from transaction import (
    deposit_money,
    withdraw_money,
    transaction_history,
)


def main():
    while True:
        print("\n" + "=" * 45)
        print("          BANK MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Register Customer")
        print("2. View Customers")
        print("3. Create Bank Account")
        print("4. Check Account Balance")
        print("5. Deposit Money")
        print("6. Withdraw Money")
        print("7. Transaction History")
        print("8. Exit")
        print("=" * 45)

        choice = input("Enter your choice (1-8): ").strip()

        if choice == "1":
            print("TEST: OPTION")
            add_customer()

        elif choice == "2":
            view_customers()

        elif choice == "3":
            create_account()

        elif choice == "4":
            check_balance()

        elif choice == "5":
            deposit_money()

        elif choice == "6":
            withdraw_money()

        elif choice == "7":
            transaction_history()

        elif choice == "8":
            print("\nThank you for using Bank Management System!")
            print("Shri Swami Samartha 🙏")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 8.")


if __name__ == "__main__":
    main()