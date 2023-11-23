# ======================================
# Python WACA SDK
# Python SDK with Wasabi Account Control API
# No guaranty from Wasabi Inc.
# ======================================

# WACA API Authentication Python Code Sample
import requests

# WACA Configuration file related
# This is to use the followings as kind of global variable:
# g.GBL_WACA_PROFILE
# g.GBL_WACA_CONF_SUB_PATH
import waca_global as g

# if needed, switch the profile by changing the g.GBL_WACA_PROFILE
# to the entry on the waca.conf
#g.GBL_WACA_PROFILE = 'wasabi'

import logging

# WACA configuration handdler
#import waca_config
from waca_config import parse_conf

# Create logger object
logging.basicConfig()   # This is important
logger = logging.getLogger(__name__)

# Set logging level (default is WARNING)
# DEBUG    - 10
# INFO     - 20
# WARNING  - 30
# ERROR    - 40
# CRITICAL - 50

# logger samples
# logger.info("This is a info log.")
# logger.warning("This is a warning log.")

# Set logging level
logger.setLevel(g.GBL_WACA_LOG_LEVEL)
level = logger.level
logger.debug(f"Current Logging Level is {level}")

## WACA API specific URL
# -----------------------------------------------
# GET a Specific Sub-Account
# https://docs.wasabi.com/docs/get-a-specific-sub-account
# GET /v1/accounts/<AcctNum>
# -----------------------------------------------

############################################################################# 
# Get summary information about the specified  sub-account
# -----------------------------------------
# =========================================
# ******************* 
#  Parameters
# *******************
# Input parameter
# int
# AcctNum   # int (MANDATORY)
# AcctNum is the unique ID assigned per sub-account
# ******************* 
#  Return value
# *******************
# SUCCESS
#  {
#        "AcctNum": 30059,
#        "AcctName": "jk@wasabi.com",
#        "CreateTime": "2020-06-08T12:12:10Z",
#        "IsTrial": false,
#        "Inactive": false,
#        "SendPasswordResetToSubAccountEmail": true
#   }
# FAIL
# {} # NULL (dictionary)
#
# =========================================
# Example:
#   account = get_a_specific_subaccount(acctNum)
#
############################################################################# 
def get_a_specific_subaccount(acctNum):
    # read WACA config file (~/.wasabi/waca.conf)
    api_conf = parse_conf()

    ## URL (Beta site) [/v1/accounts]
    url = api_conf['endpoint']
    ## API Key value
    api_key_value = api_conf['api_key']
    logger.debug(f"API Key is {api_key_value}")

    ## Request Header with API Key Authentication
    api_head = {
        'Authorization':api_key_value
    }

    url = "{}/v1/accounts/{}".format(url, acctNum)

    logger.info(f"Target URL is {url}")

    ## GET request
    ## requests.get(url, params={key: value}, args)
    r = requests.get( url, headers=api_head);

    ## Response status code
    logger.info(f"status: {r.status_code}") ; 

    ## Response JSON
    logger.debug(f"{r.json()}");  
    logger.debug(f"{type(r.json())}");  

    #print(f"{r.json()}");  
    #print(f"{type(r.json())}");  

    ## Sub-Accounts Information
    acct = {}
    if r.status_code == 200:
        acct = r.json()       
        logger.debug("===================================================================================");
        logger.debug(acct);
        logger.debug("-----------------------------------------------------------------------------------");
        logger.info(f"Account Number: {acct['AcctNum']}");
        logger.info(f"Account Name  : {acct['AcctName']}");
        
    return acct

# for the execution of this script only
# for the execution of this script only
def main():
    from waca_get_all_subaccounts import get_all_subaccounts 
    import random

    acctNum = 0 # initial ID in case no subaccount exist   

    all_subaccounts = get_all_subaccounts()     # get all sub-accounts information (list)
    logger.debug(f"all_subaccounts = {all_subaccounts}.")
    logger.debug(f"all_subaccounts type is {type(all_subaccounts)}.")
    
    num_subaccounts = len(all_subaccounts)      # registered sub-account number

    if num_subaccounts == 0:
        logger.info(f"The call for get_a_specific_subaccount() will fail as there is no subaccount created.")        
    else:
        idx =  random.randrange(0, num_subaccounts) # select index of the existing sub-account information
        acctNum = all_subaccounts[idx]["AcctNum"]
    
    logger.debug(f"Calling get_a_specific_subaccount() ...")
    logger.debug(f"Target sub-account AcctNum = {acctNum}")

    a_subaccount = get_a_specific_subaccount(acctNum)

    logger.debug(f"get_a_specific_subaccount() completed.")  

    ## return value 
    logger.debug(f"{a_subaccount}");  
    logger.debug(f"{type(a_subaccount)}");  

if __name__ == "__main__":
    main()