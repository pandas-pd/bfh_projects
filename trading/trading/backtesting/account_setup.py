import os
import sqlite3
from sqlite3 import Error

#run this scirpt once, to use the account.py correctly
#Creates the database Backtesting.db with the following tables: accounts, balances, transactions
#do not run this script, if Backtesting.db already exists

class Path():
    
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..",) #db not in git, remove ".." if db should be stored in git repo
    db_name = "Backtesting.db" #change, if a diffrent name should be used
    db = os.path.join(db_path, db_name) #this path is also used in account.py

def create_db(db_path):

    try:
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        print("\nDatabase file successfully created")
        return [cursor, connection]

    except Error as E:
        print(E)

def create_tables(cursor, connection):

    try:

        # creates accounts table
        cursor.execute("""CREATE TABLE accounts (
        account_number, name, user, remarks, active, created_timestamp
        )""")
        connection.commit()

        # creates balances table
        cursor.execute("""CREATE TABLE balances (
        account_number, currency, amount, initial_amount, revenue_in_percent
        )""")
        connection.commit()

        # creates transactions table
        cursor.execute("""CREATE TABLE transactions (
        account_number, timestamp, order_type, currency, amount, usdt_rate, amount_usdt, fee_rate, fee_usdt, total_usdt
        )""")
        connection.commit()

    except Error as E:
        print(E)
        return None

    #prints all tables and their columns as confirmation
    for table in ["accounts", "balances", "transactions"]:

        cursor.execute(f"""PRAGMA table_info({table})""")
        table_header = cursor.fetchall()
        column_names = []
        for item in table_header:
            column_names.append(item[1])

        print(f"\nTable {table} successfully created\nColumn names:\t",column_names)
        column_names.clear()

def setup():

    items = create_db(Path.db)
    cursor = items[0]
    connection = items[1]

    create_tables(cursor, connection)

    connection.close()

    print("\nDatabase setup completed\n")


if __name__ == "__main__":
    setup()