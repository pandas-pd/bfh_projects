import account
import sys
import os


#print(account.Manage.create("test", "tausj1", "testing all functions"))
#print(account.Manage.add_balance(1001, "usdt", 350))
#print(account.Get.balance_list(1001))
#print(account.Order.buy(1001,"btc"))
#print(account.Order.sell(1001,"btc"))
#print(account.Get.balance_list(1001))
#print(account.Get.account_details(1001))
#print(account.Manage.delete(1001))
#print(account.Get.account_list())
#print(account.Get.transactions(1001,"eth"))


#testing loop for transactions

ID = (account.Manage.create("test2", "tausj1", "testing all functions"))
print(account.Manage.add_balance(ID, "usdt", 350))

trx_ok = True
ticker = 0

while trx_ok == True and ticker < 20:

    if ticker % 2 == 0:
        currency ="btc"
    else:
        currency ="eth"

    buy_response = (account.Order.buy(ID,currency))
    sell_respons = (account.Order.sell(ID,currency))
    if buy_response != "transaction ok" or sell_respons != "transaction ok":
        trx_ok = False
    ticker += 1
    print(f"{ticker}:\t{buy_response}\t{sell_respons}")

account.Order.buy(ID,"btc",amount_usdt=100)
account.Order.buy(ID,"eth",amount_usdt=100)


print(f"number of transaction:\t{ticker}")
print(account.Get.balance_list(ID))
