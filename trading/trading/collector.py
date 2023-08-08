import time
import sqlite3
import subprocess
import os
from emailer import New_mail
from currencies import Currencies
from datetime import datetime as dt
from setup import DB_name
import setup
from calls import Public

db_name         = DB_name.db_path
currency_list   = Currencies.currency_list
folder_path     = os.path.dirname(os.path.abspath(__file__))
backuper_path   = os.path.join(folder_path,"backuper.py")

def write_currency_row(
    con,
    cursor,
    table_name, 
    time, 
    last, 
    lowestAsk, 
    highestBid, 
    percentChange, 
    baseVolume, 
    quoteVolume, 
    high24hr, 
    low24hr):

    # Insert a row of data into table
    cursor.execute(f"INSERT INTO {table_name} VALUES ({time},{last},{lowestAsk},{highestBid},{percentChange}, {baseVolume}, {quoteVolume}, {high24hr}, {low24hr})")

    # Save (commit) the changes!! Never forget to commit after a change!
    con.commit()

def new_db_name():

    return db_name+"_"+str(dt.today()).split(".")[0].replace(" ","_").replace(":","_")+".db"

def new_connection(name):

    connection      = sqlite3.connect(name)
    cursor          = connection.cursor()

    return (connection, cursor)

def run():

    """
    Main loop to collect and save data.
    """
    new_name = new_db_name()
    setup.setup(new_name)

    connection,cursor = new_connection(new_name)
    backup_count      = 0

    while True:

        timestamp    = dt.timestamp(dt.now())
        backup_count += 1                      

        try:
            data_all = Public.ticker_all()

        except Exception as e:
                print(e)
                New_mail(e)

        for table_name in currency_list:
            try:

                data = data_all[table_name]
                write_currency_row(
                    connection,
                    cursor,
                    table_name, 
                    timestamp, 
                    data['last'], 
                    data['lowestAsk'], 
                    data['highestBid'], 
                    data['percentChange'], 
                    data['baseVolume'], 
                    data['quoteVolume'], 
                    data['high24hr'], 
                    data['low24hr'])

            except Exception as e:
                print(e)
                New_mail(e)

        if backup_count == 17280: # backup daily, and seetup new db
            
            try:
                connection.close()
                new_name = new_db_name()
                setup.setup(new_name)
                connection,cursor = new_connection(new_name)
                New_mail("Started new DB")

            except  Exception as e:
                print(e)
                New_mail(e)
            
            backup_count= 0

        time_difference = dt.timestamp(dt.now())-timestamp
        print("Tasks time:", time_difference, "seconds")

        try:
            time.sleep(5-time_difference)
        except:
            print("Loop runs too slow")
            New_mail("Loop runs too slow")

        loop_time = dt.timestamp(dt.now())-timestamp
        
        print("Loop time:", loop_time, "seconds")


if __name__ == '__main__':
    run()
    
    