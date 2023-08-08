import requests
import json
from time import time
from urllib.parse import urlencode as _urlencode
from hmac import new as _new
from hashlib import sha512 as _sha512
from requests import post as _post

nonce = int(time()*100000)

args = {}
args['command'] = 'returnBalances'
args["nonce"] = nonce

# encode arguments for url
postData = _urlencode(args)

# sign postData with our Secret
Secret = "Enter Secret here"
Key = "Enter Key here"

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

# decode json

print(ret.json())