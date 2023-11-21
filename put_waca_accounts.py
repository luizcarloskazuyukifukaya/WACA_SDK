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

# WACA Global variables
import waca_global as g

# Set loggin(g level
logger.setLevel(g.GBL_WACA_LOG_LEVEL)
level = logger.level
logger.debug(f"Current Logging Level is {level}")

## WACA API specific URL
# -----------------------------------------------
# PUT Accounts
# https://docs.wasabi.com/docs/put-accounts
# PUT /v1/accounts
# -----------------------------------------------

############################################################################# 
# Create a subaccount
# -----------------------------------------
# Create a new sub-account that is linked to the Control Account (as authenticated via the API Key).
# Additionally, a new root user for the account will be created.
# =========================================
# Input paramater
# dict 
# {
#   "AcctName": "",                             # string    (MANDATORY: email address)
#   "IsTrial": True,                            # Boolean   default: True
#   "Password": "",                             # string    default: "Wasabi"
#   "NumTrial": 30,                             # int       default: 30
#   "QuotaGB": 1,                               # int       default: 1 GB
#   "PasswordResetRequired": True,              # Boolean   default: True
#   "EnableFTP": True,                          # Boolean   default: True
#   "Inactive": False,                          # Boolean   default: False
#   "SendPasswordSetToSubAccountEmail": True,   # Boolean   default: True
#   "AllowAccountDelete": True,                 # Boolean   default: True
# }
# ******************* 
#  Parameters
# *******************
# AcctName is email address for the subaccount to be created
# IsTrial, if set to "True," will indicate the sub-account should be created as a trial account.
# Password specifies the password for the new root user for the account and must pass the password complexity rules.
# NumTrial Day specifies the number of days for which the trial should be valid before automatically being converted to a paying account. If NumTrialDays is omitted, the default that is established for the Control Account will be used.
# QuotaGB will specify the quota (in GB) to which the new sub-account will be limited during the trial phase and, if omitted, will be the default associated with the Control Account.
# PasswordResetRequired will mark a newly provisioned sub-account password as temporary. The user will be prompted to change the password during the first login.
# EnableFTP will enable FTP/FTPS access to a sub-account.
# Inactive will set the sub-account as inactive. If Inactive is set to “False,” the sub-account will be updated as active.
# SendPasswordResetToSubAccountEmail, if set to “True,” will send an email of password reset, password changed, password expiring, or password has expired to the sub-account. Otherwise, the Control Account receives the email.
# If AllowAccountDelete is set to “False,” a sub-account is not able to see the Delete Account section in the Wasabi Management Console. If it is “true,” the Delete Account section is visible.
# ******************* 
#  Return value
# *******************
# SUCCESS
# {
#    "AcctName": "9d0a2872855afca3c11fe46e9a4018e2@wasabi.com",
#    "AcctNum": 124,
#    "AccessKey": "Z1JI27OQ75B00OLDLYMP",
#    "SecretKey": "z69QahHLjvrSnuHKJOqVufzazv1VcVJpAITvJWjN",
#    "IsTrial": true,
#    "TrialExpiry": "2018-03-09T00:00:00Z",
#    "QuotaGB": 1024
#    "FTPEnabled": true
#    "Inactive": False
# }
# FAIL
# {} # NULL (dictionary)
#
# =========================================
# Example:
#   acctInfo = {
#       "AcctName": "subaccount1@x.poweredbywasabi.com",
#       "IsTrial": True,
#       "Password": "1234567890abcdefg",
#       "QuotaGB": 10,
#   }
#   account = create_subaccount(**acctInfo)
#   # account will be the information about the new created subaccount
#
############################################################################# 
def create_subaccount(**acctInfo):
    # acct is defined with all required keys and default value
    acct = {
        "AcctName": "",                             # string    (MANDATORY: email address)
        "IsTrial": True,                            # Boolean   default: True
        "Password": "Wasabi",                       # string    default: "Wasabi"
        "NumTrial": 30,                             # int       default: 30
        "QuotaGB": 1,                               # int       default: 1 GB
        "PasswordResetRequired": True,              # Boolean   default: True
        "EnableFTP": True,                          # Boolean   default: True
        "Inactive": False,                          # Boolean   default: False
        "SendPasswordSetToSubAccountEmail": True,   # Boolean   default: True
        "AllowAccountDelete": True,                 # Boolean   default: True
        }

    account = {}
    # check mandatory information required    
    # acctInfo (dictionary)
    # acctInfo['AcctName'] (Mandatory)
    if "AcctName" in acctInfo:
        acct["AcctName"] = acctInfo["AcctName"]
    else:
        # Missing mandatory parameters
        return account
            
    # check if all given parameters are correct or not
    hasUnknownParameter = False
    keyList = list(acctInfo.keys())
    for key in keyList:
        logger.debug(f"{key} is passed as a parameter")
        if key in acctInfo:
            # found matching parameter
            logger.debug(f"Matching parameter : {key} = {acctInfo[key]}")
            # acct corresponding key's value is overwritten by the given parameter key's value
            acct[key] = acctInfo[key]
        else:
            # Unknown parameter found
            logger.error(f"Wrong parameter is given.: {key} = {acctInfo[key]}")
            hasUnknownParameter = True
            break                        
    
    if hasUnknownParameter != True:
        logger.debug(f" Input parameter : {acct}")
        # Call put_accounts()    
        account = put_accounts(acct)
        logger.debug(f"put_accounts(acct) called")
        #############
        # dummy success return
        #account = acct 
        #############
    return account


def put_accounts(acct):    
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

    #PUT /v1/accounts
    url = url + '/v1/accounts'
    logger.debug(f"PUT {url}")
    logger.info(f"Target URL is {url}")

    newAcct = {
        "AcctName": "9d0a2872855afca3c11fe46e9a4018e2@wasabi.com",
        "AcctNum": 124,
        "AccessKey": "Z1JI27OQ75B00OLDLYMP",
        "SecretKey": "z69QahHLjvrSnuHKJOqVufzazv1VcVJpAITvJWjN",
        "IsTrial": True,
        "TrialExpiry": "2018-03-09T00:00:00Z",
        "QuotaGB": 1024,
        "FTPEnabled": True,
        "Inactive": False,
    }

    keyList = list(newAcct.keys())
    for key in keyList:
        logger.debug(f"{key} is being updated")
        if key in acct:
            # found matching parameter
            logger.debug(f"Matching parameter : {key} = {acct[key]}")
            # acct corresponding key's value is overwritten by the given parameter key's value
            newAcct[key] = acct[key]   

    # HTTPS PUT
    #
    #
    #
    return newAcct
"""     
    ## PUT request
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
 """



# for the execution of this script only
if __name__ == "__main__":

    param = {
        "AcctName": "dummyaccount@dummydomain.ai",   # string    (MANDATORY: email address)
#        "IsTrial": True,                            # Boolean   default: True
        "Password": "@@@@@@@@@@@",                   # string    default: "Wasabi"
#        "NumTrial": 30,                             # int       default: 30
        "QuotaGB": 100,                              # int       default: 1 GB
#        "PasswordResetRequired": True,              # Boolean   default: True
#        "EnableFTP": True,                          # Boolean   default: True
#        "Inactive": False,                          # Boolean   default: False
#        "SendPasswordSetToSubAccountEmail": True,   # Boolean   default: True
#        "AllowAccountDelete": True,                 # Boolean   default: True
        }

    logger.debug(f"Calling create_subaccount() ...")
      
    new_subaccount = create_subaccount(**param)

    logger.debug(f"create_subaccount() completed.")  

    ## return value 
    logger.debug(f"{new_subaccount}");  
    logger.debug(f"{type(new_subaccount)}");  
