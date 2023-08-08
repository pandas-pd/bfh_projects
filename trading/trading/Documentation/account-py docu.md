# accounts.py documentation

 ## Set up
1. Change path in setup.py from database if needed (only needs to be changed there). See class Path
2. Run py account_setup.py in console
3. Database should be set up corretly
4. Change and run testing.py to make sure everythin works

## class Manage:

### Manage.create(name, user, remarks = "-")
Creates a new entry in the database accounts table and returns the account number<br/><br/>
Respons: int, account number<br/><br/>
Parameters:
 - name = str
 - user = str
 - remarks = str

### Manage.add_balance(account_number, currency, amount)
Creates a database entry for the balance, without making a transaction.<br/>
Also sets the initial_ammount value in the table balances. This value is used for calculation the revenues.<br/>
Note that dublicates of a currency can be created. Will perhaps be fixed later on.<br/><br/>
Response: str, "the following balance was created:\nAccount:\t{account_number}\nCurrency:\t{currency}\nAmount:\t\t{amount}"<br/><br/>
Parameters:
 - account_number = int, 4 charaters
 - currency = str, can be upper or lower case
 - amount = float/int

### Manage.delete(account_number, delet_account = True, delet_balances = True, delet_transactions = True)
Delets the selected database entries in the tabels accounts, balances, transactions<br/><br/>
Response: str, "Account deletion:\t{respons_account_del}\nBalances deletion:\t{respons_balances_del}\nTransactions deletion:\t{respons_transactions_del}"<br/><br/>
Parameters:
 - account_number = int, 4 characters
 - delet_account = bool, default is True
 - delet_balances = bool, default is True
 - delet_transactions = bool, default is True

## class Get:

### Get.account_details(account_number)
Returns a dataframe with the database entry from table accounts<br/><br/>
Respons: pd.dataframe, columns =  account_number, name, user, remarks, active, created_timestamp<br/><br/>
Parameters:
 - account_number = int, 4 characters

### Get.account_list():
Returns a list with all account numbers<br/><br/>
Respons: list, int values<br/><br/>
Parameters: None

### Get.balance(account_number, currency)
Returns a tupple with the infos below<br/><br/>
Respons: tuple, (account_number, currency, amount)<br/><br/>
Parameters:
 - account_number = int, 4 characters
 - currency = str, 3 to 4 charaters, can be upper or lower case

### Get.balance_list(account_number)
Returns a dataframe with all balances entry from table balances.<br/>
Also updates the column revenue when method is called<br/><br/>
Respons: pd.dataframe, columns = account_number, currency, amount, initial_amount, revenue_in_percent<br/><br/>
Parameters:
 - account_number = int, 4 characters

### Get.transactions(account_number, currency = "all")
Returns a dataframe with all transactions from an account<br/>
If a currency is entered, the dataframe will only contain the respectiv transactions.<br/><br/>
Respons: pd.dataframe, columns = account_number, timestamp, order_type, currency, amount, usdt_rate, amount_usdt, fee_rate, fee_usdt, total_usdt<br/><br/>
Parameters:
 - account_number = int, 4 characters
 - currency = str, default is "all"

## class Order:

### Order.buy(account_number, currency, amount_currency = 0,amount_usdt = 0)
Creates a buy transaction and creates a new balance entry if needed and a new entry in transactions.<br/>
Only enter one of the two parameter: amount_currency or amount_usdt. If both are left empyt or at 0, the whole USDT balance will be used for the buy transaction.<br/>
Method always buys with usdt. If the balance is not big enough, the Respons will be f"Balance USDT insufficient\nUSDT balance:\t{current_balance_usdt}\nUSDT total:\t{usdt_total}"<br/><br/>
Respons: str, "transaction ok" or "something went wrong"<br/><br/>
Parameters:
 - account_number = int, 4 characters
 - currency = str, the currency which will be bought
 - amount_currency = float/int, the ammount of currency which will be bought
 - amount_usdt = float/int, the ammoutn of usdt which will be used for buying the selected currency

### Order.sell(account_number, currency, amount_currency = 0,amount_usdt = 0)
Creates a sell transaction and creates a new entry in transactions.<br/>
Only enter one of the two parameter: amount_currency or amount_usdt. If both are left empyt or at 0, the whole currency balance will be sold.<br/>
Method always sells against usdt. If the balance is not big enough, the Respons will be f"Balance USDT insufficient\nUSDT balance:\t{current_balance_usdt}\nUSDT total:\t{usdt_total}"<br/><br/>
Respons: str, "transaction ok" or "something went wrong"<br/><br/>
Parameters:
 - account_number = int, 4 characters
 - currency = str, the currency which will be bought
 - amount_currency = float/int, the ammount of currency which will be bought
 - amount_usdt = float/int, the ammoutn of usdt which will be used for buying the selected currency