# ======================================
# Python WACA SDK
# Python SDK with Wasabi Account Control API
# No guaranty from Wasabi Inc.
# ======================================

# WACA API Authentication Python Code Sample
import requests
#from get_waca_config import pursue_conf
#import get_waca_config
from waca_config import pursue_conf

# WACA Configuration file related
# This is to use the followings as kind of global variable:
# g.GBL_WACA_PROFILE
# g.GBL_WACA_CONF_SUB_PATH
import waca_global as g

# if needed, switch the profile by changing the g.GBL_WACA_PROFILE
# to the entry on the waca.conf
g.GBL_WACA_PROFILE = 'wasabi'

api_conf = pursue_conf()
print(api_conf)

## URL (Beta site) [/v1/accounts]
url = api_conf['endpoint']
## API Key value
api_key_value = api_conf['api_key']

## Request Header with API Key Authentication
api_head = {
    'Authorization':api_key_value
}

## WACA API specific URL
# -----------------------------------------------
# https://docs.wasabi.com/docs/get-all-sub-accounts
# GET /v1/accounts
# -----------------------------------------------
url = url + '/v1/accounts'

## GET request
r = requests.get( url, headers=api_head);

## Response status code
print(f"status: {r.status_code}") ; 

## Response JSON
print(f"{r.json()}");  

## Sub-Accounts Information
for acct in r.json():
    print("===================================================================================");
    print(acct);
    print("-----------------------------------------------------------------------------------");
    print(f"Account Number: {acct['AcctNum']}");
    print(f"Account Name  : {acct['AcctName']}");
