import pandas as pd
import numpy as np
import os


class Momentum():

    def ma(df, span:int, price = "last", rev = False, drop_signal = True, drop_order = True):
        """span = relevant span for rolling mean.
        price = which prices is taken for calculation.
        rev = if True, reutrns list, with the following elements [df, total_rev, net_rev, order_count].
        rev = if False, returns df"""

        #setting signal
        ma_span = f"ma:{span}"
        df[ma_span] = df[price].rolling(span).mean()
        df["signal_ma"] = None
        df.loc[df[price] >= df[ma_span], "signal_ma"] = "+"
        df.loc[df[price] < df[ma_span], "signal_ma"] = "-"

        #signal offset
        offset = df["signal_ma"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["signal_ma_offset"] = offset

        #orders
        df["order_ma"] = None
        df.loc[(df["signal_ma"] == "+") & (df["signal_ma_offset"] == "-"), "order_ma"] = "buy"
        df.loc[(df["signal_ma"] == "-") & (df["signal_ma_offset"] == "+"), "order_ma"] = "sell"

        #calculate rev
        tot_rev, net_rev = None, None
        if rev == True:
            tot_rev = Revenue.total(df, "order_ma", price)
            net_rev = Revenue.net(df, "order_ma", price)

        #delet rows
        df.drop("signal_ma_offset", axis = 1, inplace = True)
        if drop_signal:
            df.drop('signal_ma',axis =1, inplace = True)
        if drop_order:
            df.drop('order_ma',axis = 1, inplace = True)

        #return values
        if rev == True:
            return [df, tot_rev, net_rev]
        if rev == False:
            return df

    def ewm(df, span:int, price = "last", halflife = None, alpha = None, rev = False, drop_signal = True, drop_order = True):
        """span = relevant span for estimated weighted moving average.
        price = which prices is taken for calculation.
        rev = if True, reutrns list, with the following elements [df, total_rev, net_rev, order_count].
        rev = if False, returns df"""
    
        #setting signal
        ewm_span = f"ewm:{span}"
        df[ewm_span] = df[price].ewm(span=span, halflife=halflife, alpha=alpha).mean()
        df["signal_ewm"] = None
        df.loc[df[price] > df[ewm_span], "signal_ewm"] = "+"
        df.loc[df[price] < df[ewm_span], "signal_ewm"] = "-"

        #setting signal offset
        offset = df["signal_ewm"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["signal_ewm_offset"] = offset

        #orders
        df["order_ewm"] = None
        df.loc[(df["signal_ewm"] == "+") & (df["signal_ewm_offset"] == "-"), "order_ewm"] = "buy"
        df.loc[(df["signal_ewm"] == "-") & (df["signal_ewm_offset"] == "+"), "order_ewm"] = "sell"

        #return values
        tot_rev, net_rev = None, None
        if rev:
            tot_rev = Revenue.total(df, "order_ewm", price)
            net_rev = Revenue.net(df, "order_ewm", price)

        #delet rows
        df.drop('signal_ewm_offset', axis =1, inplace = True)
        if drop_signal:
            df.drop(['signal_ewm', ],axis=1, inplace = True)
        if drop_order:
            df.drop('order_ewm',axis=1, inplace = True)

        #return values
        if rev:
            return [df, tot_rev, net_rev]
        if rev == False:
            return df

    def macd_ma (df, ma1:int, ma2:int, price = "last",rev = False, drop_signal = True, drop_order = True):
        """ma1 = span of first moving average.
        ma2 = spand of econd moving average.
        ma1 < ma2.
        price = which prices is taken for calculation.
        rev = True: returns [df, total_revenue, net_revenue]"""

        #setting signal
        macd = f"macd_ma_{ma1}-{ma2}"
        df[macd] = df[price].rolling(ma1).mean() - df[price].rolling(ma2).mean()
        df["signal_macd"] = None
        df.loc[df[macd] >= 0, "signal_macd"] = "+"
        df.loc[df[macd] < 0, "signal_macd"] = "-"

        #setting signal offset
        offset = df["signal_macd"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["signal_macd_offset"] = offset

        #orders
        df["order_macd"] = None
        df.loc[(df["signal_macd"] == "+") & (df["signal_macd_offset"] == "-"), "order_macd"] = "buy"
        df.loc[(df["signal_macd"] == "-") & (df["signal_macd_offset"] == "+"), "order_macd"] = "sell"

        #return values
        tot_rev, net_rev = None, None
        if rev:
            tot_rev = Revenue.total(df, "order_macd", price)
            net_rev = Revenue.net(df, "order_macd", price)

        #delet columns
        df.drop("signal_macd_offset", axis = 1, inplace = True)
        if drop_order:
            df.drop("order_macd", axis =1, inplace = True)
        if drop_signal:
            df.drop("signal_macd", axis = 1, inplace = True)

        if rev:
            return [df, tot_rev, net_rev]
        if rev == False:
            return df

    def macd_ewm (df, ewm1:int, ewm2:int, price = "last",halflife = None, alpha = None, rev = False, drop_signal = True, drop_order = True):
        """ewm1 = span of first moving average.
        ewm2 = spand of econd moving average.
        ewm1 < ewm2.
        price = which prices is taken for calculation.
        rev = True: returns [df, total_revenue, net_revenue]"""

        #setting signal
        macd = f"macd_ewm_{ewm1}-{ewm2}"
        df[macd] = df[price].ewm(ewm1).mean() - df[price].ewm(ewm2).mean()
        df["signal_macd"] = None
        df.loc[df[macd] >= 0, "signal_macd"] = "+"
        df.loc[df[macd] < 0, "signal_macd"] = "-"

        #setting signal offset
        offset = df["signal_macd"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["signal_macd_offset"] = offset

        #orders
        df["order_macd"] = None
        df.loc[(df["signal_macd"] == "+") & (df["signal_macd_offset"] == "-"), "order_macd"] = "buy"
        df.loc[(df["signal_macd"] == "-") & (df["signal_macd_offset"] == "+"), "order_macd"] = "sell"

        #return values
        tot_rev, net_rev = None, None
        if rev:
            tot_rev = Revenue.total(df, "order_macd", price)
            net_rev = Revenue.net(df, "order_macd", price)

        #delet columns
        df.drop("signal_macd_offset", axis = 1, inplace = True)
        if drop_order:
            df.drop("order_macd", axis =1, inplace = True)
        if drop_signal:
            df.drop("signal_macd", axis = 1, inplace = True)

        if rev:
            return [df, tot_rev, net_rev]
        if rev == False:
            return df

    def rsi (df, timeframe, buy_th, sell_th, price = "last",rev = False, orders = False, drop_signal = True, drop_order = True):
        """timeframe = how many periods should be taken for calculation; 14.
        buy_th = buy_threshhold for buying
        sell_th = sell_threshhold for selling
        Explanation: Value of RSI varies between in intervall [-100, 100]"""
        if buy_th >= sell_th:
            print(str("buy_th must be smaller than sell_th"))
            return None

        #price column offset
        price_offset = df[price].tolist()
        price_offset.pop()
        price_offset.insert(0, None)
        df["price_offset"] = price_offset

        #calculate win or loss from offset in %
        df["change"] = ((df[price] / df["price_offset"]) - 1) * 100 #calculated in %

        #win and loss columns
        df["win"] = df["change"]
        df["loss"] = df["change"]
        df.loc[df["win"] <= 0, "win"] = 0
        df.loc[df["loss"] > 0, "loss"] = 0
        df["loss"] = df["loss"] * (-1)

        #average win and loss
        df["avg_win"] = df["win"].rolling(timeframe, min_periods = 0).mean()
        df["avg_loss"] = df["loss"].rolling(timeframe, min_periods = 0).mean()

        #calculte RS
        df["rsi"] = 100 - (100 / (1+(df["avg_win"]/df["avg_loss"])))
       
        #delet columns which are not needed
        df.drop(axis = 1, labels = ["price_offset", "change", "win", "loss", "avg_win", "avg_loss"], inplace = True)

        #orientation
        offset = df["rsi"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["rsi_offset"] = offset
        df["orientation"] = None
        df.loc[(df["rsi"] - df["rsi_offset"] > 0), "orientation"] = "+"
        df.loc[(df["rsi"] - df["rsi_offset"] < 0), "orientation"] = "-"
        df.loc[(df["rsi"] - df["rsi_offset"] == 0), "orientation"] = "0"
        df.drop(axis=1,labels ="rsi_offset", inplace = True)

        if orders == False:
            return df

        #rsi thershhold range (buy if smaller than th buy, hold if between buy_th and sell_th, sell if bigger than sell_th)
        df["th_range"] = None
        df.loc[df["rsi"] < buy_th, "th_range"] = "buy"
        df.loc[(df["rsi"] >= buy_th) & (df["rsi"] <= sell_th), "th_range"] ="hold"
        df.loc[df["rsi"] > sell_th, "th_range"] = "sell"

        #th offset
        offset = df["th_range"].tolist()
        offset.pop()
        offset.insert(0, None)
        df["th_range_offset"] = offset

        #make orders
        df["order_rsi"] = None
        df.loc[ (df["th_range"] == "hold") & (df["th_range_offset"] == "buy"),"order_rsi"] = "buy"
        df.loc[ (df["th_range"] == "sell") & (df["th_range_offset"] == "hold"),"order_rsi"] = "sell"

        #order correction
        order_list = df["order_rsi"].tolist()

        last_order = None
        for pos in range(len(order_list)):
            if order_list[pos] != None:
                if order_list[pos] != last_order:
                    last_order = order_list[pos]
                elif order_list[pos] == last_order:
                    order_list[pos] = None
        df["order_rsi"] = order_list

        #return values
        tot_rev, net_rev = None, None
        if rev:
            tot_rev = Revenue.total(df, "order_rsi", price)
            net_rev = Revenue.net(df, "order_rsi", price)

        #delet columns
        #df.drop("signal_macd_offset", axis = 1, inplace = True)
        if drop_order:
            df.drop("order_rsi", axis =1, inplace = True)
        if drop_signal:
            df.drop(['orientation', 'th_range', 'th_range_offset'], axis = 1, inplace = True)

        if rev:
            return [df, tot_rev, net_rev]
        if rev == False:
            return df

    def adx(timeframe):
            pass

class Volatility():

    def relativ(df, price = "last", range1 = 50, range2 = 1000):
        "(delat max min) range 1 / (delta max min) range 2"
        df["vol_relative"] = (df[price].rolling(range1).max() - df[price].rolling(range1).min()) / (df[price].rolling(range2).max() - df[price].rolling(range2).min())
        return df

    def price_ratio(df, price = "last", range = 50):
        "(delat max min) range / current price"
        df["vol_price_ratio"] = (df[price].rolling(range).max() - df[price].rolling(range).min()) / df[price]
        return df

    def range_ratio(df, price = "last", range_delta = 50, range_ma = 300):
        "(delta max min) raange_delta / ma(range_ma) price"
        df["vol_price_ratio"] = (df[price].rolling(range_delta).max() - df[price].rolling(range_delta).min()) / df[price].rolling(range_ma).mean()
        return df

class Revenue():
    """returns the revenue in %"""

    fee = 0.125 #in %
    fee_d = 0.00125 #in decimal

    def total(df,signal_name, price):

        df = df[df[signal_name].notna()][[price, signal_name]]

        #drop first order if not buy; drop last order if not sell
        if df[signal_name].iloc[0] != "buy":
            df = df.iloc[1:]
        if df[signal_name].iloc[-1] != "sell":
            df = df.iloc[:-1]

        #total_orders = len(df["orders"].tolist())

        #calculate ongoing revenue
        orders = {
            "buy" : (df[df[signal_name]=="buy"][price]*(1)).tolist(), #factor = price + fees
            "sell" : (df[df[signal_name]=="sell"][price]*(1)).tolist(), #factro = price -fees
        }

        df_o = pd.DataFrame(orders) #df_o = df_orders
        df_o["rev_d"] = df_o["sell"] / df_o["buy"]
        #df_o["ongoing_rev_d"] = None

        balance = 1 #calculate with decimal
        balance_list = []

        for rev_d in df_o["rev_d"].tolist():
            balance = balance * rev_d
            balance_list.append(balance)

        #df_o["ongoing_rev_d"] = balance_list
        rev = (balance_list[-1] - 1) * 100
        return rev
    
    def net(df, signal_name, price):

        df = df[df[signal_name].notna()][[price, signal_name]]

        #drop first order if not buy; drop last order if not sell
        if df[signal_name].iloc[0] != "buy":
            df = df.iloc[1:]
        if df[signal_name].iloc[-1] != "sell":
            df = df.iloc[:-1]

        #total_orders = len(df["orders"].tolist())

        #calculate ongoing revenue
        orders = {
            "buy" : (df[df[signal_name]=="buy"][price]*(1 + Revenue.fee_d)).tolist(), #factor = price + fees
            "sell" : (df[df[signal_name]=="sell"][price]*(1 - Revenue.fee_d)).tolist(), #factro = price -fees
        }

        df_o = pd.DataFrame(orders) #df_o = df_orders
        df_o["rev_d"] = df_o["sell"] / df_o["buy"]
        #df_o["ongoing_rev_d"] = None

        balance = 1 #calculate with decimal
        balance_list = []

        for rev_d in df_o["rev_d"].tolist():
            balance = balance * rev_d
            balance_list.append(balance)

        #df_o["ongoing_rev_d"] = balance_list
        rev = (balance_list[-1] - 1) * 100
        return rev