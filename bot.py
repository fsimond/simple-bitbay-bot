import hashlib
import hmac
from datetime import datetime
import json
import math
import pickle
import slack
import requests
import time

BITBAY_PUBLIC_KEY = <bitbay_public_key>
BITBAY_PRIVATE_KEY = <bitbay_public_key>

SLACK_TOKEN = <slack_token>

BITBAY_CHANNEL = "test"


def slack_message(message, channel):
    sc = slack.WebClient(SLACK_TOKEN)

    sc.chat_postMessage(channel=channel, text=message, icon_emoji=':robot_face:', username="BitBay Bot")


def bitbay_trading_api(method, privatek, publick):
    post = "method=" + method + "&moment=" + str(math.floor(time.time())) + "&currency=BTC"

    sign = hmac.new(bytes(privatek, 'utf-8'), post.encode('utf-8'), hashlib.sha512).hexdigest()

    headers = {"API-Key": publick, "API-Hash": sign, 'Content-Type': 'application/x-www-form-urlencoded'}

    api_url = "https://bitbay.net/API/Trading/tradingApi.php"

    return requests.post(api_url, data=post, headers=headers)


def transaction2string(tr):
    trstr = tr['date'] + ": "

    if tr['type'] == 'ASK':
        trstr += "SOLD "
    elif tr['type'] == 'BID':
        trstr += "BOUGHT "
    else:
        assert False

    trstr += tr['amount'] + " " + tr['market'].split("-")[0] + " at " + tr['rate'] + " for a total amount of " \
             + tr['price'] + " " + tr['market'].split("-")[1]

    return trstr


last_transaction_date = None
try:
    with open('last_transaction_date.pkl', 'rb') as f:
        last_transaction_date = pickle.load(f)
except FileNotFoundError as fnfe:
    last_transaction_date = None

orders = json.loads(bitbay_trading_api("transactions", BITBAY_PRIVATE_KEY, BITBAY_PUBLIC_KEY).text)

ltd = None

for o in orders:
    tr_date = datetime.strptime(o['date'], "%Y-%m-%d %H:%M:%S")
    if last_transaction_date is None or tr_date > last_transaction_date:
        slack_message(transaction2string(o), BITBAY_CHANNEL)
        if ltd is None or tr_date > ltd:
            ltd = tr_date

if ltd:
    with open('last_transaction_date.pkl', 'wb') as f:  # Python 3: open(..., 'wb')
        pickle.dump(ltd, f)
