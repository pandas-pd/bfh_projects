#public calls imports
import requests
import datetime as dt
from datetime import datetime

#privat calls imports
import json
from time import time
from urllib.parse import urlencode as _urlencode
from hmac import new as _new
from hashlib import sha512 as _sha512
from requests import post as _post

#API Key encryption
from cryptography.fernet import Fernet
import os

class Public ():
    
    def ticker (currency = "USDT_BTC"):
        """Returns the current Price of a Currency. Currency: CUR1_CUR2"""
        api_answer = requests.get("https://poloniex.com/public?command=returnTicker")
        data = api_answer.json()
        return data[currency]

    def ticker_all ():
        """Returns the current Price of a Currency. Currency: CUR1_CUR2"""
        api_answer = requests.get("https://poloniex.com/public?command=returnTicker")
        data = api_answer.json()
        return data

    def volume_24h (currency = "USDT_BTC"):
        """Returns the total tradet volume, traded in the last 24 houres. Currency: CUR1_CUR2"""
        api_answer = requests.get("https://poloniex.com/public?command=return24hVolume")
        data = api_answer.json()
        return data[currency]

    def orderbook (currency = "USDT_BTC"):
        """Returns the current orderbook. Currency: CUR1_CUR2"""
        api_answer = requests.get(f"https://poloniex.com/public?command=returnOrderBook&currencyPair={currency}")
        data = api_answer.json()
        return data
    
    def chart_data (currency = "USDT_BTC", periode = 300):
        """Returns the chart data for candle sticks. Currency: CUR1_CUR2. Periode (in seconds): 300, 900, 1800, 7200, 14400, 86400"""
        pass
        api_answer = request.get(f"https://poloniex.com/public?command=returnChartData&currencyPair={currency}&start=1546300800&end=1546646400&period={periode}")

class Private():

    path_file = os.path.join(os.path.dirname(os.path.abspath(__file__)),"..") #change this line if needed
    key = None
    secret = None

    def _template(command, args={}):

        args['command'] = command #Example: 'returnBalances'
        args["nonce"] = nonce = int(time()*100000) #needs to be in mil.secs

        # encode arguments for url
        postData = _urlencode(args)

        # sign postData with our Secret
        Key = Private.key
        Secret = Private.secret

        sign = _new(
            Secret.encode('utf-8'),
            postData.encode('utf-8'),
            _sha512)

        # post request
        ret = _post(
            'https://poloniex.com/tradingApi',
            data=args,
            headers={'Sign': sign.hexdigest(), 'Key': Key},
            ) #timeout=self.timeout

        return ret.json()

    def returnBalances():
        """Retruns all balances"""
        return Private._template('returnBalances')

    def returnCompleteBalances(account='all'):
        """Returns all of your balances, including available balance, balance on orders, and the estimated BTC value of your balance"""
        return Private._template('returnCompleteBalances', {'account': str(account)} )

    def returnDepositAddresses():
        """Returns deposit addresses"""
        return Private._template('returnDepositAddresses')

    def generateNewAddress(coin:str):
        """Creates a new deposit address for <coin>"""
        return Private._template('generateNewAddress', {'currency': coin.upper()} )

    def returnDepositsWithdrawals(start = None, end=None):
        """Returns deposit/withdraw history. start and end must be in UNIX timestamp format"""

        one_day = 60*60*24 #one day in seconds
        now = int(datetime.timestamp(datetime.now()))

        if start == None:
            start = int(now-(30*one_day))
        if end == None:
            end = now

        args = {'start': str(start), 'end': str(end)}
        return Private._template('returnDepositsWithdrawals', args)

    def returnOpenOrders(pair:str='all'):
        """Returns your open orders for [pair='all']"""
        return Private._template('returnOpenOrders', {'currencyPair': pair.upper()} )

    def returnTradeHistory(pair:str='all', start=None, end=None):
        """Returns private trade history for <pair>"""

        one_day = 60*60*24 #one day in seconds
        now = int(datetime.timestamp(datetime.now()))

        if start == None:
            start = int(now-(30*one_day))
        if end == None:
            end = now

        args = {
            'currencyPair': pair.upper(),
            'start' : start,
            'end' : end
            }

        return Private._template('returnTradeHistory', args)

    def returnOrderTrades(orderId):
        """Returns any trades made with the given <orderId>"""
        return Private._template('returnOrderTrades', {'orderNumber':str(orderId)})

    def returnOrderStatus(orderId):
        """Returns the status of the given <orderId>"""
        return Private._template('returnOrderStatus', {'orderNumber':str(orderId)})

    def buy(pair:str, rate, amount, type = None):
        """Places a limit buy order
        Required args: <pair>, <rate>, <amount>
        possible type (optional)= fillOrKill, immediateOrCancel, postOnly
        if type is left empty, it will be a normal limit buy order"""

        #Required args
        args = {
            'currencyPair' : pair.upper(),
            'rate' : str(rate),
            'amount' : str(amount)
        }

        #Check optional args
        if type != None:
            if type in ['fillOrKill', 'immediateOrCancel', 'postOnly']:
                args[type] = 1
            else:
                raise ValueError (f"{type} is not a valid order type")

        return Private._template("buy", args)

    def sell(pair:str, rate, amount, type = None):
        """Places a sell order
        Required args: <pair>, <rate>, <amount>
        possible type (optional)= fillOrKill, immediateOrCancel, postOnly
        if type is left empty, it will be a normal sell order"""

        #Required args
        args = {
            'currencyPair' : pair.upper(),
            'rate' : str(rate),
            'amount' : str(amount)
        }

        #Check optional args
        if type != None:
            if type in ['fillOrKill', 'immediateOrCancel', 'postOnly']:
                args[type] = 1
            else:
                raise ValueError (f"{type} is not a valid order type")

        return Private._template("sell", args)

    def cancelOrder(orderId):
        """Cancels an order with the given <orderId>"""
        Private._template('cancelOrder', {'orderNumber':str(orderId)})

    def cancelAllOrders(pair:str=None):
        """Cancels all orders. If a currenyPair is given, only these orders will be canceled
        Optional args = currencyPair"""

        args = {}
        if pair != None:
            args['currencyPair'] = pair.upper()

        return Private._template('cancelAllOrders', args)

    def cancelReplace(orderId, rate, amount = None):
        """Cancels the <orderId> and places a new one of the same type in two separate operations
        Required args: <orderId>, <rate>,
        Optional args: <amount>"""

        args = {
            'orderNumber' : str(orderId),
            'rate' : str(rate)
            }
        
        #add optional arg
        if amount != None:
            args[amount] = str(amount)

        return Private._template('cancelReplace', args)

    def moveOrder():
        """not needed at the moment"""
        pass

    def withdraw(): #must be activated in the poloniex settings
        """not needed at the moment"""
        pass

    def returnFeeInfo():
        """returns your current trading fees and trailing 30-day volume in BTC. This information is updated once every 24 hours."""
        return Private._template("returnFeeInfo")

class General ():

    privat_calls_coded =[
    'returnBalances',
    'returnCompleteBalances',
    'returnDepositAddresses',
    'generateNewAddress',
    'returnDepositsWithdrawals',
    'returnOpenOrders',
    'returnTradeHistory',
    'returnOrderTrades',
    'returnOrderStatus'
    'buy',
    'sell',
    'cancelOrder',
    'cancelAllOrders',
    'cancelReplace',
    'moveOrder',
    'withdraw',
    'returnFeeInfo'] #coded till here

    private_calls_tbd = [
    'returnAvailableAccountBalances',
    'returnTradableBalances',
    'transferBalance',
    'returnMarginAccountSummary',
    'marginBuy',
    'marginSell',
    'getMarginPosition',
    'closeMarginPosition',
    'createLoanOffer',
    'cancelLoanOffer',
    'returnOpenLoanOffers',
    'returnActiveLoans'
    'returnLendingHistory',
    'toggleAutoRenew',
    'swapCurrencies',
    ]

    def check_privat_call(command):
        """Checks if command is a valid Privat call and if the function is coded in this wrapper"""

        response = {
            "Valid command" : False,
            "Available in wrapper" : False
        }

        if command in General.privat_calls_coded:
            response["Valid command"] = True
            response["Available in wrapper"] = True
        
        if command in General.private_calls_tbd:
            response["Valid command"] = True
            response["Available in wrapper"] = False

        return response

    def _get_api_key():

        # read encrypted pwd and convert into byte
        with open(os.path.join(Private.path_file,"encryptedPWD_key.txt")) as f:
            encpwd = ''.join(f.readlines())
            encpwdbyt = bytes(encpwd, 'utf-8')
        f.close()

        # read key and convert into byte
        with open(os.path.join(Private.path_file,"refKey_key.txt")) as f:
            refKey = ''.join(f.readlines())
            refKeybyt = bytes(refKey, 'utf-8')
        f.close()

        # use the key and encrypt pwd
        keytouse = Fernet(refKeybyt)
        myPass = (keytouse.decrypt(encpwdbyt))
        
        return str(myPass)[2:-1]

    def _get_api_secret():

        # read encrypted pwd and convert into byte
        with open(os.path.join(Private.path_file,"encryptedPWD_secret.txt")) as f:
            encpwd = ''.join(f.readlines())
            encpwdbyt = bytes(encpwd, 'utf-8')
        f.close()

        # read key and convert into byte
        with open(os.path.join(Private.path_file,"refKey_secret.txt")) as f:
            refKey = ''.join(f.readlines())
            refKeybyt = bytes(refKey, 'utf-8')
        f.close()

        # use the key and encrypt pwd
        keytouse = Fernet(refKeybyt)
        myPass = (keytouse.decrypt(encpwdbyt))

        return str(myPass)[2:-1]

if Private.key == None and Private.secret == None:
    try:
        Private.key = General._get_api_key()
        Private.secret = General._get_api_secret()
    except:
        pass