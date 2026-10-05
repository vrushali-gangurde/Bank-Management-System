# Bank Management System

## Project Overview

A Python-based Bank Management System connected to a PostgreSQL database. It helps manage customers, bank accounts, deposits, withdrawals, and transaction history.

## Technologies Used

* Python
* PostgreSQL
* psycopg2
* python-dotenv

## Features

* Customer Registration
* View Customer Details
* Create Bank Account
* Check Account Balance
* Deposit Money
* Withdraw Money
* View Transaction History

## Setup Instructions

1. Install Python and PostgreSQL.
2. Install dependencies using `pip install -r requirements.txt`.
3. Create a PostgreSQL database named `bank_d`.
4. Configure database credentials in the `.env` file using `.env.example` as a guide.
5. Run the application using `python main.py`.

## Security

Database credentials are stored in `.env`. Do not upload this file to GitHub.
