import os
import sys
from datetime import datetime
import math
import pandas as pd
import sqlite3
from sqlite3 import Error 
from account_setup import Path #this script only uses Path.db to connect to database

#Adds parent directory to systempath to import the modul calls.py
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.insert(1, parent_dir)
import calls


#can be deleted, wehn script is tested:
"""
Accounts
Column names:    ['account_number', 'name', 'user', 'remarks', 'active', 'created_timestamp']

Balances
Column names:    ['account_number', 'currency', 'amount', 'initial_amount', 'revenue']

transactions
Column names:    ['account_number', 'timestamp', 'order_type', 'currency', 'amount', 'usdt_rate', 'amount_usdt', 'fee_rate', 'fee_usdt', 'total_usdt']
"""

class Manage():

    def create(name, user, remarks = "-"):
        """creates an entry in the database
        returns the account number"""

        account_number = _DB.account.create_account_number()
        active = 1 #0 = inactive, 1 = active
        timestamp = str(datetime.now())[:23]

        respons = _DB.account.create(account_number, name, user, remarks, active, timestamp)

        if respons == "ok":
            return account_number
        else:
            return respons

    def add_balance(account_number, currency, amount): #change: add new parameters 
        """Creates a database entry for the balance, without making a transaction
        returns a confirmation if the entry was created"""
        
        currency = str(currency).upper()

        if _DB.account.check(account_number) == "nok":
            return f"Account {account_number} does not exist"

        respons = _DB.balance.create(account_number, currency, float(amount))

        if respons == "ok":
            return f"the following balance was created:\nAccount:\t{account_number}\nCurrency:\t{currency}\nAmount:\t\t{amount}"
        else:
            return respons

    def delete(account_number, delet_account = True, delet_balances = True, delet_transactions = True):
        """delets the database entry for the selected values
        returns an confirmation, what was deleted"""

        if _DB.account.check(account_number) == "nok":
            return f"Account {account_number} does not exist"

        respons_account_del = None
        respons_balances_del = None
        respons_transactions_del = None

        if delet_account == True:
            respons_account_del = _DB.account.delete(account_number)

        if delet_balances == True:
            respons_balances_del = _DB.balance.delete(account_number)

        if delet_transactions == True:
            respons_transactions_del = _DB.transaction.delete(account_number)

        respons = f"Account deletion:\t{respons_account_del}\nBalances deletion:\t{respons_balances_del}\nTransactions deletion:\t{respons_transactions_del}"
        return respons

class Get():

    def account_details(account_number):
        """returns a dataframe with the database entry from 'accounts'"""

        respons = _DB.account.check(account_number)
        if respons == "nok":
            return f"Account {account_number} does not exist"

        account_detail = _DB.account.get_detail(account_number)

        return account_detail

    def account_list():
        """returns a list with all account numbers"""
        account_list = _DB.account.get_list()
        return account_list

    def balance(account_number, currency):
        """returns a tupple: (account_number, currency, amount)"""

        currency = currency.upper()
        respons = Get.balance_list(account_number)

        if isinstance(respons, str) == True:
            return respons
        else:
            df = respons
        
        df_currency = df.loc[df["currency"] == currency]
        balance = df_currency[["account_number","currency", "amount"]].values.tolist()

        return tuple(balance[0])

    def balance_list(account_number):
        """returns a dataframe with all balances from an account
        upadtes and/or calculates the revenue"""

        _DB.balance.update_revenue(account_number)
        respons = _DB.balance.get(account_number)
        
        if isinstance(respons, str) == True:
            return f"Something went wrong:\n{respons}"
        else:
            return respons

    def transactions(account_number, currency = "all"):
        """returns a dataframe with all transactions from an account
        If a currency is entered, the dataframe will only contain the respectiv transactions
        default is all transactions and all currencies"""

        df = _DB.transaction.get(account_number)
        if currency == "all":
            return df
        else:
            df_currency = df.loc[df["currency"] == str(currency.upper())]
            return df_currency

    def returns():
        pass

class Order():

    fee = 0.00125 #decimal

    def buy(account_number, currency, amount_currency = 0,amount_usdt = 0, custom_rate = None):
        """creates a buy transaction and creates a new balance entry if needed
        only enter one of the two parameter: amount_currency or amount_usdt
        if both are left empyt or at 0, the whole balance will be used
        function always buys with usdt"""

        if _DB.account.check(account_number) == "nok":
            return f"Account {account_number} does not exist"

        currency = str(currency).upper()

        if custom_rate == None:
            price = calls.Public.ticker(f"USDT_{currency}")
            rate = float(price["last"]) #used for further calculations
        
        elif custom_rate != None:
            rate = custom_rate

        #calculate both amounts, perhaps externalise? is this function neccesary
        currency_amount = None
        usdt_amount = None

        if amount_usdt !=0 and amount_currency == 0:
            usdt_amount = amount_usdt
            currency_amount = amount_usdt / rate
        elif amount_usdt ==0 and amount_currency != 0:
            currency_amount = amount_currency
            usdt_amount = amount_currency * rate
        elif amount_usdt ==0 and amount_currency ==0:
            usdt_amount = float(Get.balance(account_number,"USDT")[2])/(1+Order.fee)
            currency_amount = usdt_amount / rate

        if currency_amount == 0 or usdt_amount == 0:
            return "Cant place a buy order without volume"

        #calculate all needed values for database entry: fee_rate, fee_usdt, total_usdt
        usdt_fee = usdt_amount * Order.fee
        usdt_total = round((usdt_fee + usdt_amount),12)

        #check if balance is sufficient
        current_balance_usdt = Get.balance(account_number,"USDT")[2]
        if usdt_total > current_balance_usdt:
            return f"Balance USDT insufficient\nUSDT balance:\t{current_balance_usdt}\nUSDT total:\t{usdt_total}"

        #create the database entry in transaction
        trx_respons = _DB.transaction.create(account_number, "buy", currency, currency_amount, rate, usdt_amount, Order.fee, usdt_fee, usdt_total)
        if trx_respons != "ok":
            return trx_respons
        
        #check if a balance for buy currency is availabel and create new entry if it is missing, call
        new_balance = False
        if _DB.balance.check(account_number, currency) == "nok":
            _DB.balance.create(account_number,currency,currency_amount)
            new_balance = True

        #update balance table with new values, call
        usdt_balance_old = Get.balance(account_number, "USDT")[2]

        if new_balance == False:
            currency_balance_old = Get.balance(account_number, currency)[2]
        elif new_balance == True:
            currency_balance_old = 0
            new_balance = False

        update_balance_usdt = _DB.balance.update(account_number,"USDT", float(usdt_balance_old-usdt_total))
        update_balance_currency = _DB.balance.update(account_number, currency, float(currency_balance_old+currency_amount))

        if update_balance_usdt == "ok" and update_balance_currency == "ok":
            return "transaction ok"
        else:
            return "something went wrong"

    def sell(account_number, currency, amount_currency = 0,amount_usdt = 0, custom_rate = None):
        """creates a sell transaction
        only enter one of the two parameter: amount_currency or amount_usdt
        function always sell against usdt"""

        if _DB.account.check(account_number) == "nok":
            return f"Account {account_number} does not exist"

        currency = str(currency).upper()

        if custom_rate == None:
            price = calls.Public.ticker(f"USDT_{currency}")
            rate = float(price["last"]) #used for further calculations
        
        elif custom_rate != None:
            rate = custom_rate

        #calculate both amounts, perhaps externalise? is this function neccesary
        currency_amount = None
        usdt_amount = None

        if amount_usdt !=0 and amount_currency == 0:
            usdt_amount = amount_usdt
            currency_amount = amount_usdt / rate
        elif amount_usdt ==0 and amount_currency != 0:
            currency_amount = amount_currency
            usdt_amount = amount_currency * rate
        elif amount_usdt ==0 and amount_currency == 0:
            currency_amount = float(Get.balance(account_number,currency)[2])
            usdt_amount = currency_amount * rate

        if currency_amount == 0 or usdt_amount == 0:
            return "Cant place a sell order without volume"

        #calculate all needed values for database entry: fee_rate, fee_usdt, total_usdt
        usdt_fee = usdt_amount * Order.fee
        usdt_total = round((usdt_amount - usdt_fee), 12)

        #check if balance is sufficient
        current_balance_currency = Get.balance(account_number,currency)[2]
        if currency_amount > current_balance_currency:
            return f"Balance {currency} insufficient\n{currency} balance:\t{current_balance_currency}\n{currency} total:\t{usdt_total}"

        #create the database entry in transaction
        trx_respons = _DB.transaction.create(account_number, "sell", currency, currency_amount, rate, usdt_amount, Order.fee, usdt_fee, usdt_total)
        if trx_respons != "ok":
            return trx_respons

        #update balance table with new values, call
        usdt_balance_old = Get.balance(account_number, "USDT")[2]
        currency_balance_old = Get.balance(account_number, currency)[2]

        update_balance_usdt = _DB.balance.update(account_number,"USDT", float(usdt_balance_old+usdt_total))
        update_balance_currency = _DB.balance.update(account_number, currency, float(currency_balance_old-currency_amount))

        if update_balance_usdt == "ok" and update_balance_currency == "ok":
            return "transaction ok"
        else:
            return "something went wrong"

class _DB(): #class is only used from within this script (private)

    connection = None
    cursor = None

    def create_connection():
        if _DB.connection == None and _DB.cursor == None:
            try:
                _DB.connection = sqlite3.connect(Path.db)
                _DB.cursor = _DB.connection.cursor()
            except Error as E:
                message = f"Could not connect to database. Make sure account_setup.py was run.\n Error: {E}"
                print(message)
    
    def close_connection():
        #currently not used
        if _DB.connection != None and _DB.cursor != None:
            try:
                _DB.connection.close()
            except Error as E:
                message = f"Could not close connection.\nError: {E}"

            _DB.connection = None
            _DB.cursor = None

    class account():

        def create(account_number, name, user, remarks, active, timestamp):

            try:
                _DB.cursor.execute(f"""INSERT INTO accounts VALUES ({account_number}, '{name}', '{user}', '{remarks}', {active}, '{timestamp}')""")
                _DB.connection.commit()
                return "ok"

            except Error as E:
                return E

        def get_detail(account_number):
            try:
                df = pd.read_sql_query(f"""SELECT * FROM accounts WHERE account_number = {account_number}""", _DB.connection)
                return df
            except Error as E:
                return E

        def get_list():

            _DB.cursor.execute("""SELECT * FROM accounts""")
            content = _DB.cursor.fetchall()

            accounts = []
            for row in content:
                accounts.append(row[0])

            return accounts

        def check(account_number):
            accounts = _DB.account.get_list()
            if account_number in accounts:
                return "ok"
            return "nok"

        def update():
            pass

        def delete(account_number):

            try:
                _DB.cursor.execute(f"""DELETE FROM accounts WHERE account_number = {account_number}""")
                _DB.connection.commit()
                return "ok"

            except Error as E:
                return E

        def create_account_number():

            _DB.cursor.execute("""SELECT * FROM accounts""")

            accounts = _DB.account.get_list()

            if len(accounts) == 0:
                return 1001
            else:
                new_number = accounts[-1] + 1
                return new_number

    class transaction():

        def create(account_number, order_type, currency, amount, usdt_rate, amount_usdt, fee_rate, fee_usdt, total_usdt):
            timestamp = str(datetime.now())[:23]

            try:
                _DB.cursor.execute(f"""INSERT INTO transactions VALUES ({account_number},'{timestamp}', '{order_type}', '{currency}', {amount}, {usdt_rate}, {amount_usdt}, {fee_rate}, {fee_usdt}, {total_usdt})""")
                _DB.connection.commit()
                return "ok"
            except Error as E:
                return E

        def get(account_number):
            try:
                df = pd.read_sql_query(f"""SELECT * FROM transactions WHERE account_number = {account_number}""", _DB.connection)
                return df
            except Error as E:
                return E

        def delete(account_number):

            try:
                _DB.cursor.execute(f"""DELETE FROM transactions WHERE account_number = {account_number}""")
                _DB.connection.commit()
                return "ok"

            except Error as E:
                return E

    class balance():

        def create(account_number, currency, amount):
            try:
                _DB.cursor.execute(f""" INSERT INTO balances VALUES ({account_number}, '{currency}', {amount}, {amount}, {0})""")
                _DB.connection.commit()
                return "ok"
            except Error as Er:
                return Er

        def get(account_number):
            """returns all balances as a dataframe"""

            try:
                df = pd.read_sql_query(f"""SELECT * FROM balances WHERE account_number = {account_number}""",_DB.connection)
            except Error as Er:
                return str(Er)
            
            return df

        def check(account_number, currency):

            df = _DB.balance.get(account_number)
            currency_list = df["currency"].tolist()

            if currency in currency_list:
                return "ok"
            else:
                return "nok"

        def update(account_number, currency,new_amount):

            try:
                _DB.cursor.execute(f"""UPDATE balances SET amount = {new_amount} WHERE account_number = {account_number} AND currency = '{currency}'""")
                _DB.connection.commit()
                return "ok"
            except Error as E:
                return E

        def update_revenue(account_number):

            df = _DB.balance.get(account_number)
            df["revenue_updated"] = ((df["amount"]/df["initial_amount"])-1) * 100

            for currency_item in df["currency"].to_list():
                try:
                    new_rev = float(df.loc[df["currency"] == currency_item]["revenue_updated"])
                    _DB.cursor.execute(f"""UPDATE balances SET revenue_in_percent = {new_rev} WHERE account_number = {account_number} AND currency = '{currency_item}'""")
                    _DB.connection.commit()
                except Error as E:
                    print(E)


        def delete(account_number):

            try:
                _DB.cursor.execute(f"""DELETE FROM balances WHERE account_number = {account_number}""")
                _DB.connection.commit()
                return "ok"
            except Error as E:
                return E

_DB.create_connection()