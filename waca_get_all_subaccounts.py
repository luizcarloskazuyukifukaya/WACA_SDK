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

# Set loggin(g level
logger.setLevel(g.GBL_WACA_LOG_LEVEL)
level = logger.level
logger.debug(f"Current Logging Level is {level}")

## WACA API specific URL
# -----------------------------------------------
# GET All Sub-Accounts
# https://docs.wasabi.com/docs/get-all-sub-accounts
# GET /v1/acco(unts
# -----------------------------------------------
# List all sub-acco(unts
# (with summary profile information)
# that are associated with the Control Account (as authenticated via the API K(ey).
def get_all_subaccounts():
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

    url = url + '/v1/accounts'
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
    for acct in r.json():
        logger.debug("===================================================================================");
        logger.debug(acct);
        logger.debug("-----------------------------------------------------------------------------------");
        logger.debug(f"Account Number: {acct['AcctNum']}");
        logger.debug(f"Account Name  : {acct['AcctName']}");
        
    return r.json

# for the execution of this script only
if __name__ == "__main__":
    logger.debug(f"Calling all_subaccounts() ...")
      
    all_subaccounts = get_all_subaccounts()

    logger.debug(f"all_subaccounts() completed.")  

    ## return value 
    logger.debug(f"{all_subaccounts}");  
    logger.debug(f"{type(all_subaccounts)}");  
