import os
from currencies import Currencies
import sqlite3

currency_list = Currencies.currency_list

class DB_name:
    """
    Sets the name for a new database. 
    """    
    db_name         = "crypto" #change here, .db ending is added later
    backup_name     = "backup" #change here, .db ending is added later

    data_directory_path     = os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")
    db_path                 = os.path.join(data_directory_path, db_name)
    backup_path             = os.path.join(data_directory_path, backup_name)

def check_data_directory():
    """
    Creates data directory if none.
    """
    if not os.path.isdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data")):
        os.mkdir(os.path.join(os.path.dirname(os.path.abspath(__file__)),"data"))

def create_currency_table(connection, cursor, table_name):
    """
    Needs to be executed in the setup. Creates table.
    """
   
    cursor.execute(f'''CREATE TABLE {table_name}
                (time text, last real, lowestAsk real, highestBid real, percentChange real, baseVolume real, quoteVolume real, high24hr real, low24hr real)''')


def setup(new_db_path):
    """
    Execute to setup database. 
    """
    check_data_directory()
    
    connection  = sqlite3.connect(new_db_path)
    cursor      = connection.cursor()
    for table_name in currency_list:
        create_currency_table(connection, cursor, table_name) #using currency pair as table name

    connection.commit()
    connection.close()
    print("Database is set")

if __name__ == '__main__':
    pass