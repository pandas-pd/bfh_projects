"""
required custom moduls:
indicators.py; account_setup.py; account.py; calls-setup.py; calls.py

requirements:
- run account_setup.py
- run calls-setup.py (only needed for live trading)
"""

#import standard moduls
import pandas as pd
import os
import sys
import sqlite3
from sqlite3 import Error
import time

#Adds parent directory to systempath to import the modul calls.py
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
sys.path.insert(1, parent_dir)

parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..")
sys.path.insert(1, parent_dir)

#importing custom moduls (form directory)
from indicators import Momentum
from indicators import Volatility
import account as Account
from calls import Public
from calls import Private as Poloniex

class Strat():

    def __init__(self, currency:str, currency_pair:str, db_folder:str):
        self.currency = currency
        self.currency_pair = currency_pair
        self.df = pd.DataFrame({"last":[]}) #used for current price update and indicator calculation
        self.open_pos = False
        self.db_df = None
        self.db_folder = db_folder
        self.last_buy_price = None
        self.poloniex_time_out = 10 #time out limit for buy and sell oders on poloniex
        self.buy, self.sell = None, None

    def load_db_data(self):
        """loads all the needed data from the data folder for backtesting"""
        file_list = os.listdir(self.db_folder)

        df_list = []

        for db in file_list:
            try:
                connection = sqlite3.connect(os.path.join("data", db))
            except Error as E:
                print(E)
            df = pd.read_sql_query(f"SELECT * FROM {self.currency_pair.upper()}", connection)
            df_list.append(df)
            connection.close()

        df = df_list[0]

        #return a singl df
        if len(df_list) > 1:
            for item in df_list[1:]:
                df = df.append(item)

        df["time"] = df["time"].astype(float)
        df.sort_values(by="time", ascending=True, inplace = True)

        self.db_df = df

    def update_indicator(self, new_price:float): #change the needed code here
        """calculate the new needed indicators and add them to the df"""
        max_span = 3000

        #adds new price to df
        self.df = self.df.append({"last":new_price}, ignore_index = True)

        #change max span, remove unneeded data from df (see the max sapn in indicators)
        if len(self.df["last"].tolist()) >= max_span:
            self.df.drop(self.df.head(1).index, inplace = True)

        #Add needed indicaotrs here (this is an example)
        self.df = Momentum.ma(self.df, span = 2000, price = "last", rev = False, drop_signal=False)

    def update_buy_signal(self): #change the needed code here
        """Change code here to set the bux signal for strat"""

        #code your conditions here

        #Example:
        if self.df["signal_ma"].tolist()[-1] == "+":
            self.buy = True #is this upadte in Run.methods?

    def update_sell_signal(self): #change the needed code here
        """Change code here to set the bux signal for strat"""

        #code your conditions here

        #Example:
        if self.df["signal_ma"].tolist()[-1] == "-":
            self.sell = True #is this upadte in Run.methods?

    def poloniex_buy(self, pair, currency ,rate):
        """places a buy order with the total available USDT balance"""

        #get the avaiable balance
        all_balances = Poloniex.returnBalances()
        amount = (float(all_balances["USDT"])*0.99) / rate #total balance regarding fees

        #place order
        response = Poloniex.buy(pair, rate, amount, type = "fillOrKill") #does that make sense?

        #wait for order to fill and cancle, if timeout is reached (one cyle is 1 second)
        for i in range(self.poloniex_time_out):
            start = time.time()

            #order successfull
            orders = Poloniex.returnOpenOrders(pair)
            if len(orders) == 0: #break loop if order was executed and is not open anymore
                self.open_pos = True
                self.last_buy_price = rate
                break

            #order unsuccessfull, time out is reached, order is cannceled
            if (i+1) == self.poloniex_time_out:
                cancel_res = Poloniex.cancelAllOrders(pair)
                if int(cancel_res["success"]) == 1:
                    break
                else:
                    print("something went wrong when canceling the order during the set time out")
                    break

            #time cycle duraiton
            end = time.time()
            if (1 - (end-start)) > 0:
                time.sleep(1 - (end-start))
            else:
                continue

    def poloniex_sell(self, pair, currency ,rate):
        """places a sell order with the total available USDT balance"""

        #get the avaiable balance
        all_balances = Poloniex.returnBalances()
        amount = (float(all_balances["currency"])*1) #total balance regarding fees

        #place order
        response = Poloniex.sell(pair, rate, amount, type = "fillOrKill") #does that make sense?

        #wait for order to fill and cancle, if timeout is reached (one cyle is 1 second)
        for i in range(self.poloniex_time_out):
            start = time.time()

            #order successfull
            orders = Poloniex.returnOpenOrders(pair)
            if len(orders) == 0: #break loop if order was executed and is not open anymore
                self.open_pos = False
                self.last_buy_price = None
                break

            #order unsuccessfull, time out is reached, order is cannceled
            if (i+1) == self.poloniex_time_out:
                cancel_res = Poloniex.cancelAllOrders(pair)
                if int(cancel_res["success"]) == 1:
                    break
                else:
                    print("something went wrong when canceling the order during the set time out")
                    break

            #time cycle duraiton
            end = time.time()
            if (1 - (end-start)) > 0:
                time.sleep(1 - (end-start))
            else:
                continue

class Run():

    #change the needed code here, needed for live and backtesting
    currency = "ETH"
    currency_pair = "USDT_ETH"
    db_folder = "data"
    cycle_limit = None #if None, whole db will be tested in the backtesting_db
    cycle_time = 5 #defualt, is the same as the bt data

    #parameters only used for backtesting (creating an account)
    strat_name = "test"
    user = "test_script"

    @staticmethod
    def backtesting_db():
        """runs the strat with data from the data folder with db files"""

        strat = Strat(currency = Run.currency, currency_pair = Run.currency_pair, db_folder = Run.db_folder)
        strat.load_db_data() #strat.db_df
        ID = Account.Manage.create(name = Run.strat_name, user=Run.user, remarks = "backtesting with db data")
        Account.Manage.add_balance(ID, "USDT", 100) #used 100 to represent %, eas of use
        print("Account ID:\t",ID)

        price_list = strat.db_df["last"].tolist()
        ticker  = 0 #counts the cycles

        #set the max count of cycles
        if Run.cycle_limit == None:
            Run.cycle_limit = len(price_list)

        #trading loop
        while ticker <= Run.cycle_limit:

            price = price_list[0]
            price_list.pop(0) #delet first entry, to reduce RAM usage
            strat.update_indicator(float(price)) #adds new price to self.df and calculates the new indicators

            #buy condition
            if strat.open_pos == False:
                strat.update_buy_signal()
                if strat.buy == True:
                    Account.Order.buy(ID, currency = Run.currency_pair, custom_rate = price)
                    strat.last_buy_price = price
                    strat.open_pos = True
                    strat.buy = False

            #sell condition
            if strat.open_pos == True:
                strat.update_sell_signal()
                if strat.sell == True:
                    Account.Order.sell(ID, currency = Run.currency_pair, custom_rate = price)
                    strat.last_buy_price = None
                    strat.open_pos = False
                    strat.sell = False

            ticker +=1

    @staticmethod
    def backtesting_live():
        """runs the strat with live data in backtesting"""

        strat = Strat(currency = Run.currency, currency_pair = Run.currency_pair, db_folder = Run.db_folder)
        ID = Account.Manage.create(name = Run.strat_name, user=Run.user, remarks = "backtesting with db data")
        Account.Manage.add_balance(ID, "USDT", 100)
        print("Account ID:\t",ID)

        ticker  = 0 #counts the cycles

        #set the max count of cycles
        if Run.cycle_limit == None:
            raise ValueError ("Cycle_limit must be set")

        #trading loop
        while ticker <= Run.cycle_limit:

            start = time.time()

            try:
                price = Public.ticker(Run.currency_pair)["last"]
                print("Last rate:\t", price)
            except:
                print("Cylce will be skipped, due to error in connection to the poloniex API")
                continue
            strat.update_indicator(float(price)) #adds new price to self.df and calculates the new indicators

            #buy condition
            if strat.open_pos == False:
                strat.update_buy_signal()
                if strat.buy == True:
                    Account.Order.buy(ID, currency = Run.currency_pair, custom_rate = price)
                    strat.last_buy_price = price
                    strat.open_pos = True
                    strat.buy = False
                    print(Account.Get.transactions(ID).tail(1))

            #sell condition
            if strat.open_pos == True:
                strat.update_sell_signal()
                if strat.sell == True:
                    Account.Order.sell(ID, currency = Run.currency_pair, custom_rate = price)
                    strat.last_buy_price = None
                    strat.open_pos = False
                    strat.sell = False
                    print(Account.Get.transactions(ID).tail(1))

            ticker +=1

            #calculate and stop time to keep in sync with cycle
            end = time.time()
            run_time = end-start
            if run_time < Run.cycle_time:
                time.sleep(float(Run.cycle_time - run_time))

    @staticmethod
    def live():
        """runs the strat live on Poloniex"""

        strat = Strat(currency = Run.currency, currency_pair = Run.currency_pair, db_folder = Run.db_folder)
        ticker = 0

        while Run.cycle_limit > ticker or strat.open_pos == True: #trading wil end, when the cylce limit is up and there are no open positions left
            
            start = time.time()

            #setting price and error handling
            try:
                price = Public.ticker(Run.currency_pair)["last"]
            except:
                print("Cylce will be skipped, due to error in connection to the poloniex API")
                continue

            strat.update_indicator(price) #adding new price to df and calculte set indicators

            #buy condition
            if strat.open_pos == False:
                strat.update_buy_signal()
                if strat.buy == True:
                    strat.poloniex_buy(Run.currency_pair, Run.currency, price)
                    strat.buy = False #has to cked with Strat.methods

            #sell condition
            if strat.open_pos == True:
                strat.update_sell_signal()
                if strat.sell == True:
                    strat.poloniex_sell(Run.currency_pair, Run.currency, price)
                    strat.sell = False

            #ticker + time stop

        #contiue here

if __name__ == "__main__":
    Run.backtesting_db()