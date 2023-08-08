import sqlite3
from currencies import Currencies
from setup import DB_name
import pandas as pd
import os

currency_list   = Currencies.currency_list

def load_table_as_df(db_name, table_name):
    """
    Returns any table as df
    """
    
    connection = sqlite3.connect(db_name,)

    table_df = pd.read_sql_query(f"SELECT * FROM {table_name}", connection)

    connection.close()

    return table_df

def load_data_folder(table_name):

    db_files = os.listdir(DB_name.data_directory_path)
    print(db_files)
    df = pd.DataFrame()

    for db_file in db_files:
        print(db_file)

        if df.empty:
            df = load_table_as_df(os.path.join(DB_name.data_directory_path,db_file),table_name)
        else :
            df = pd.concat([df,load_table_as_df(os.path.join(DB_name.data_directory_path,db_file),table_name)],ignore_index=True)
    
    return df

def list_table_names():
    db_files = os.listdir(DB_name.data_directory_path)
    print(db_files)
    df = None

    for db_file in db_files:
        con = sqlite3.connect(os.path.join(DB_name.data_directory_path,db_file))
        cursor = con.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        print(cursor.fetchall())
        con.close()

if __name__ == '__main__':


    df= load_data_folder("USDT_ETH")
    print(df)

    