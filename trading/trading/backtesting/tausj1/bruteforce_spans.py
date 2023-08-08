import pandas as pd
import os
import sys
import sqlite3
from sqlite3 import Error

#Adds parent directory to systempath to import the modul calls.py
parent_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","..")
sys.path.insert(1, parent_dir)

#importing indicators
from indicators import Momentum
from indicators import Volatility

class Data():

    currency = "USDT_ETH"
    path = "data"

    def return_df():
        """read the Data.path folder for .db files and returns a dataframe with the given currency"""

        file_list = os.listdir("data")

        df_list = []

        for db in file_list:
            try:
                connection = sqlite3.connect(os.path.join(Data.path, db))
            except Error as E:
                print(E)
            df = pd.read_sql_query(f"SELECT * FROM {Data.currency}", connection)
            df_list.append(df)
        
        df = df_list[0]

        #return a singl df
        if len(df_list) == 1:
            return df
        else:
            for item in df_list[1:]:
                df = df.append(item)

        df["time"] = df["time"].astype(float)
        df.sort_values(by="time", ascending=True, inplace = True)

        return df

    def write_results(df, name):
        pass

    def test_indicator(ma:bool, macd:bool):

        range_start = 1000
        range_end = 20000
        step = 10000

        df = Data.return_df()

        #dicts for recording data
        results_ma = {
            "span": [],
            "tot_rev": [],
            "net_rev": [],
        }

        "[df, total_rev, net_rev, order_count]"
        if ma:
            for span_ma in range(range_start, range_end, step):
                results = Momentum.ma(df, span=span_ma, price="last", rev=True, drop_order=True, drop_signal=True)
                results_ma["span"].append(span_ma)
                results_ma["tot_rev"].append(results[1])
                results_ma["net_rev"].append(results[2])
                print(f"calculted ma:\t{span_ma}")
            df_ma = pd.DataFrame(results_ma)
            df_ma.to_csv("ma_bf_results")


        #dicts for recording data

        results_macd = {
            "span1": [],
            "span2": [],
            "tot_rev": [],
            "net_rev": [],
        }

        if macd:
            for span1 in range(range_start, range_end,step):
                for span2 in range(span1+step, range_end, step):
                    results = Momentum.macd_ma(df, ma1=span1, ma2=span2, price="last", rev=True, drop_order=True, drop_signal=True)
                    results_macd["span1"].append(span1)
                    results_macd["span2"].append(span2)
                    results_macd["tot_rev"].append(results[1])
                    results_macd["net_rev"].append(results[2])
                    print(f"calculated macd:\t{span1}\t\t\t{span2}")
            df_macd = pd.DataFrame(results_macd)
            df_macd.to_csv("macd_bf_results")


if __name__ == "__main__":
    Data.test_indicator(ma = True, macd = True)