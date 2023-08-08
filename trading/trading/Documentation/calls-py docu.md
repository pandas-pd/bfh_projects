# calls.py documentation

## Setup
There is no setup required for the public calls<br/>
The private calls need to be set-up

## calss Public

### Public.ticker (currency = "USDT_BTC")
Returns a dictonary with multiple prices form the given currency pair. The current price to use for transactions in "last"<br/><br/>
Respons:{
    'id': 121, 
    'last': '52570.00000000', 
    'lowestAsk': '52570.99987988', 
    'highestBid': '52562.74384000', 
    'percentChange': '0.01604517', 
    'baseVolume': '34468272.33651587', 
    'quoteVolume': '662.78280465', 
    'isFrozen': '0', 
    'postOnly': '0', 
    'high24hr': '52920.95690601', 
    'low24hr': '50953.73415013'
    }<br/><br/>
Parameters:
 - currency = str, currency pair

### Public.ticker_all ()
Returns a dictonary with all the available currencies from poloniex. They are callable with the key "CUR1_CUR2"<br/><br/>
Respons: dict<br/><br/>
Parameters: None

### Public.volume_24h (currency = "USDT_BTC")
Returns the trading volume of a currency pair as a dictonary<br/><br/>
Respons:{
    'USDT': '34454285.30201973', 
    'BTC': '662.49040196'
    }<br/><br/>
Parameters:
 - currency = str, currency pair

### Public.orderbook (currency = "USDT_BTC")
Returns a dictonary with all the current orderbook information<br/><br/>
Respons:{
    'asks': [['52500.00000001', 0.93184629], ... ['52868.28057385', 0.03035]], 
    'bids': [['52500.00000000', 1.33936308], ..., ['52261.53869581', 0.02503153]], 
    'isFrozen': '0', 
    'postOnly': '0', 
    'seq': 1530317119
    }

### Public.chart_data (currency = "USDT_BTC", periode = 300)
currently not used

## calss Privat

### Setup
1. https://support.poloniex.com/hc/en-us/articles/360060622793-How-to-Create-an-API-Secret-Key-Set
2. pip install rsa
3. Enter the needed inpus

### Documentation
The script is coded as a wrapper. Poloniex API docu<br\>
https://docs.poloniex.com/#private-http-api-methods<br\>
The functions within the script (class Private) should be selfexplanatory
