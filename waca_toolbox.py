# ======================================
# Python WACA SDK
# Python SDK with Wasabi Account Control API
# No guaranty from Wasabi Inc.
# ======================================

# WACA API Authentication Python Code Sample
import requests
import json

# WACA Configuration file related
# This is to use the followings as kind of global variable:
# g.GBL_WACA_PROFILE
# g.GBL_WACA_CONF_SUB_PATH
import waca_global as g

# if needed, switch the profile by changing the g.GBL_WACA_PROFILE
# to the entry on the waca.conf
#g.GBL_WACA_PROFILE = 'wasabi'

import logging

# WACA configuration handler
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

import random

# ****************************************************************
# randomname for generate random string for email address creation
# only for development and test purpose 

def randomname(n):
    import random, string

    randlst = [random.choice(string.ascii_letters + string.digits) for i in range(n)]
    return ''.join(randlst).lower()

# for the execution of this script only
# this is only for the test of the updated_subaccount()
def create_dummy_subaccount():
    from waca_put_accounts import create_subaccount
    
    EMAIL_DOMAIN_NAME = "@postwacawasabi.com"    
    
    param = {
#        "AcctName": "",                              # string    (MANDATORY: email address)
#        "IsTrial": True,                            # Boolean   default: True
#        "Password": "@@@@@@@@@@@",                  # string    default: "Wasabisys"
#        "NumTrailDay": 30,                         # int       default: 30
        "QuotaGB": 10,                               # int       default: 1 GB
        "PasswordResetRequired": False,              # Boolean   default: True
#        "EnableFTP": True,                          # Boolean   default: True
#        "Inactive": False,                          # Boolean   default: False
#        "SendPasswordSetToSubAccountEmail": True,   # Boolean   default: True
#        "AllowAccountDelete": True,                 # Boolean   default: True
        }

    param["AcctName"] = randomname(24) + EMAIL_DOMAIN_NAME
    logger.debug(f"Sub-account AcctName = {param['AcctName']}")  
    
    logger.debug(f"Calling create_subaccount() ...")
    
    new_subaccount = create_subaccount(**param)

    logger.debug(f"create_subaccount() completed.")  

    ## return value 
    logger.debug(f"{new_subaccount}");  
    logger.debug(f"{type(new_subaccount)}");  

    #-----------------------------------------------------------
    #-----------------------------------------------------------
    id = new_subaccount['AcctNum']
    return id

# get a random acctNum from the existing sub-accounts
def get_random_subaccount():
    from waca_get_all_subaccounts import get_all_subaccounts 

    acctNum = 0 # initial ID in case no subaccount exist   

    all_subaccounts = get_all_subaccounts()     # get all sub-accounts information (list)
    #logger.debug(f"all_subaccounts = {all_subaccounts}.")
    #logger.debug(f"all_subaccounts type is {type(all_subaccounts)}.")
    
    num_subaccounts = len(all_subaccounts)      # registered sub-account number

    if num_subaccounts == 0:
        logger.info(f"The call for get_a_specific_subaccount() will fail as there is no subaccount created.")        
    else:
        idx =  random.randrange(0, num_subaccounts) # select index of the existing sub-account information
        acctNum = all_subaccounts[idx]["AcctNum"]
    
    logger.debug(f"Calling get_a_specific_subaccount() ...")
    logger.info(f"Target sub-account AcctNum = {acctNum}")

    logger.debug(f"get_random_subaccount() completed.")  
    return acctNum

# for the execution of this script only
# this is only for the test of the updated_subaccount()
# delete the dummy sub-account created for the test
def delete_dummy_subaccount(id):
    from waca_delete_subaccount import delete_subaccount

    logger.debug(f"deleting sub-account AcctNum : {id}");  

    # delete subaccount created
    delete_subaccount(id)
    
    logger.debug(f"deleted");  
