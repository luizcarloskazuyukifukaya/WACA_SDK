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

## WACA API specific URL
# -----------------------------------------------
# PUT Accounts
# https://docs.wasabi.com/docs/post-an-updated-sub-account
# POST /v1/accounts/<AcctNum>
# -----------------------------------------------

############################################################################# 
# Update the sub-account information.
# -----------------------------------------
# <AcctNum> is the target sub-account ID.
# This function will update the sub-account information 
# and return the updated sub-account information as a dictionary
# =========================================
# ******************* 
#  Parameters
# *******************
# Input parameter
# dict 
# {
#   "AcctNum": 0,                               # int (MANDATORY)
#   "AcctName": "",                             # string    
#   "Password": "",                             # string
#   "NumTrailDays": 30,                        # int       
#   "QuotaGB": 1,                               # int
#   "ConvertToPaid", False                      # Boolean
#   "ResetAccessKeys", False                    # Boolean
#   "PasswordResetRequired": True,              # Boolean
#   "EnableFTP": True,                          # Boolean
#   "Inactive": False,                          # Boolean
#   "SendPasswordSetToSubAccountEmail": True,   # Boolean
#   "AllowAccountDelete": True,                 # Boolean
#   "DisableMFA": False,                        # Boolean
# }
# AcctName, if specified, change the root user's email address
# Password, if this will change the root user’s password provided that it passes the password complexity policies.
# NumTrailDays, if specified, this will change the number of days associated with the trial period, up to a limit set on the Control Account.
# QuotaGB, if specified, this will change the trial period storage quota, up to a limit set on the Control Account.
# ConvertToPaid, if is set to “true,” this will transition the sub-account to a full (paid) account.
# ResetAccessKeys, if is set to “true,” all previous access keys on the sub-account are invalidated and a new Access Key to the root user account on the sub-account is generated.
# PasswordResetRequired, if is set to “true,” a newly provisioned sub-account password is temporary.
# EnableFTP, if is set to “true,” FTP/FTPS access to a sub-account will be enabled.
# Inactive, if is set to “true,” the account will be set as inactive. 
# SendPasswordSetToSubAccountEmail, if set to “true,” will send an email of password reset, password changed, password expiring, or password has expired to the sub-account.
# AllowAccountDelete, if is set to “false,” a sub-account is not able to see the Delete Account section in the Wasabi Management Console.
# DisableMFA, if is set to “true,” MFA will be deactivated in a sub-account.
# ******************* 
#  Return value
# ** NOTE **
# Is not necessary all key related to the sub-account, and could be less.
# See the API example https://docs.wasabi.com/docs/post-an-updated-sub-account
# *******************
# SUCCESS
# {
#    "AcctNum": 134,
#    "AcctName": "second-f68241f15bfcf08c1e11877d617a7f93@wasabi.com",
#    "AccessKey": "Z1JI27OQ75B00OLDLYMP",
#    "SecretKey": "z69QahHLjvrSnuHKJOqVufzazv1VcVJpAITvJWjN",
#    "CreateTime": "2018-02-07T19:49:49Z",
#    "IsTrial": true,
#    "TrialExpiry": "2018-03-20T00:00:00Z",
#    "QuotaGB": 512,
#    "FTPEnabled": true,
#    "Inactive": false
# }
# FAIL
# {} # NULL (dictionary)
#
# =========================================
# Example:
#   acctInfo = {
#       "AcctName": "second-f68241f15bfcf08c1e11877d617a7f93@wasabi.com",
#       "NumTrialDays": 45,
#       "Password": "xyzzy123$$$",
#       "QuotaGB": 512,
#       "ResetAccessKeys": true,
#       "EnableFTP": true
#   }
#   account = update_subaccount(**acctInfo)
#   # account will be the information about the updated subaccount
#
############################################################################# 
def update_subaccount(**acctInfo):
    # acctParamInfo is defined with the parameter key name and value type expected
    acctParamInfo = {
        "AcctNum": type(0),                             # int (MANDATORY)
        "AcctName": type("string"),                     # string    
        "Password": type("string"),                     # string                                   
        "NumTrailDays": type(30),                      # int
        "QuotaGB": type(1),                             # int
        "ConvertToPaid": type(False),                   # Boolean
        "ResetAccessKeys": type(False),                 # Boolean
        "PasswordResetRequired": type(True),            # Boolean
        "EnableFTP": type(True),                        # Boolean
        "Inactive": type(False),                        # Boolean
        "SendPasswordSetToSubAccountEmail": type(True), # Boolean
        "AllowAccountDelete": type(True),               # Boolean
        "DisableMFA": type(False),                      # Boolean        
    }
    
    logger.debug(f"Starting update_subaccount ....")
    logger.debug(f"{acctInfo}")

    # return account dict
    account = {}

    # check if the acctInfo include valid key and its value matching the expected type
    isAcctNumValid = False
    isInputParamValid = True
    keyList = list(acctInfo.keys())
    for key in keyList:
        logger.debug(f"{key} is specified as the input parameter")
        if key in acctParamInfo:
            # found matching parameter
            logger.debug(f"Matching parameter : {key} =  value type : {acctParamInfo[key]}")
            logger.debug(f"Input parameter : {key} =  value type : {type(acctInfo[key])}")
                        
            # check the value type
            if type(acctInfo[key]) is acctParamInfo[key]: # True
                # check mandatory key "AcctNum"
                if key == "AcctNum":
                    isAcctNumValid = True
                    logger.debug(f"Mandatory key {key} is found and valid.")
                    
                continue
            else:
                # value not matching expected type
                logger.debug(f"Matching parameter : {key} =  value : {acctParamInfo[key]}")
                isInputParamValid = False
                break
        else:
            logger.debug(f"{key} is not a valid as input parameter")
            # Invalid key found
            isInputParamValid = False
            break
    
    if isAcctNumValid == False:
        logger.error(f"Mandatory AcctNum is either not provided or not valid.")
    
    # Only when the Input parameter is valid
    if isInputParamValid == True:
        logger.debug(f" Input parameter : {acctInfo}")
        # get target AcctNum (id)
        id = acctInfo['AcctNum']

        # format input for post_account()
        acct = acctInfo
        acct.pop('AcctNum')

        # Call put_accounts()    
        account = post_account(id, acct)
        logger.debug(f"post_account() called")

    logger.debug(f"update_subaccount completed.")
    return account            
        
# post_account
# post_account( id, acct)
# id is the target account AcctNum
# acct is the parameter required for the REST POST call (excluding AcctNum)
# Call WACA REST directly here
def post_account(acctNum, acct):    
    # read WACA config file (~/.wasabi/waca.conf)
    api_conf = parse_conf()

    ## URL (Beta site) [/v1/accounts]
    url = api_conf['endpoint']
    ## API Key value
    api_key_value = api_conf['api_key']
    logger.debug(f"API Key is {api_key_value}")

    ## Request Header with API Key Authentication
    api_head = {
        'Authorization':api_key_value,
        'Content-Type': 'application/json',
        'X-Wasabi-Service': 'partner',
    }
    # "Content-Type: application/json; charset=utf-8" # request( ,json=data )
    # Content-Type: application/json
    # X-Wasabi-Service: partner

    #POST /v1/accounts/<AcctNum>
    url = "{}/v1/accounts/{}".format(url, acctNum)

    logger.debug(f"POST {url}")
    logger.info(f"Target URL is {url}")

    # HTTPS POST
    # data = acct
    # acct is confirmed to have all keys and values required to create the sub-account    
    logger.debug(f"HTTPS POST Request start from here .............. ")
    logger.debug(f"URL =  {url}")
    logger.debug(f"headers =  {api_head}")
    logger.debug(f"data =  {acct}")

    ## PUT request
    ## requests.post(url, params={key: value}, args)

    # This cause Internal Server Error json=acct
    # Response code: 500    
    #r = requests.post( url, headers=api_head, json=json.dumps(acct))

    # ********* requests.post only works with 'data=acct' *************
    # Response code: 403
    # You are not permitted to complete that action
    # Response code: 400
    # Bad Request
    #r = requests.post( url, headers=api_head, data=acct)

    # json in Dictionary (Works)
    #r = requests.post( url, headers=api_head, json=acct)

    # JSON format data (Works)
    logger.debug(f"data JSON =  {json.dumps(acct)}")
    r = requests.post( url, headers=api_head, data=json.dumps(acct))

    ## Response status code
    logger.info(f"status: {r.status_code}") ; 

    ## Response JSON
    logger.debug(f"{r.json()}");  
    logger.debug(f"{type(r.json())}");  

    #print(f"{r.json()}");  
    #print(f"{type(r.json())}");  
    ## Sub-Accounts Information
    newCreatedAcct = {} # default NULL
    if r.status_code == 200:
        newCreatedAcct = r.json()
        logger.debug("===================================================================================");
        logger.debug(" POST an Updated Sub-Account Response.");
        logger.debug(newCreatedAcct);
        logger.debug("-----------------------------------------------------------------------------------");
        logger.info(f"Account Number: {newCreatedAcct['AcctNum']}");
        logger.info(f"Account Name  : {newCreatedAcct['AcctName']}");
        logger.debug("===================================================================================");
    logger.info(f"{r.json()}")
    logger.info(f"{newCreatedAcct}")
    
    return newCreatedAcct


# for the execution of this script only
def create_update_delete():
    import time

    from waca_toolbox import create_dummy_subaccount
    from waca_toolbox import randomname
    from waca_get_specific_subaccount import get_a_specific_subaccount
    from waca_delete_subaccount import delete_subaccount

    NEW_EMAIL_DOMAIN_NAME = "@poweredbywasabi.ai"    

    # create dummy subaccount
    id = create_dummy_subaccount()
    logger.debug(f"Waiting for WACM to complete account creation : {id}");
    time.sleep(5)      
    # It cause Server Internal Error if the update_subaccount is called in short time after creation
    logger.debug(f"Resuming test ...");
    # Use static AcctNum 1058395, 1058394, 1059642
    #id =  1058394

    # Instead of creating new subaccount, let's get from existing one
    #id = get_random_subaccount()
    #logger.info(f"Target AcctNum for update is {id}");

    updateParam = generate_dummy_update_param()

    # specify the target id (the new created subaccount)
    updateParam['AcctNum'] = id
    logger.info(f"Target sub-account to be updated AcctNum is {id}.")
    
    logger.debug(f"Calling update_subaccount() ...")
    
    updated_subaccount = update_subaccount(**updateParam)

    logger.debug(f"update_subaccount() called.")  

    ## Updated sub-account 
    logger.info(f"[Response value] {updated_subaccount}");  
    logger.debug(f"[Response value] {type(updated_subaccount)}");
    
    logger.debug(f"Waiting for WACM to complete account UPDATE : {id}");
    time.sleep(5)      
    logger.debug(f"Resuming test ...");

    # Get Updated sub-account information
    new_updated_subaccount = get_a_specific_subaccount(id)  
    ## Updated sub-account 
    logger.info(f"{new_updated_subaccount}");  
    logger.debug(f"{type(new_updated_subaccount)}");

    delete_subaccount(id)
    
    logger.info(f"updated_subaccount test completed.");  

# Update exiting subaccount
def update_existing():
    import time

    from waca_get_specific_subaccount import get_a_specific_subaccount
    from waca_toolbox import get_random_subaccount

    # Instead of creating new subaccount, let's get from existing one
    id = get_random_subaccount()
    #
    # id = 1058180 # fixed account
    #id = 1060004 
    logger.info(f"Target AcctNum for update is {id}");

    updateParam = generate_dummy_update_param()

    # specify the target id (the new created subaccount)
    updateParam['AcctNum'] = id
    logger.info(f"Target sub-account to be updated AcctNum is {id}.")

    logger.debug(f"Calling update_subaccount() ...")
    
    updated_subaccount = update_subaccount(**updateParam)

    logger.debug(f"update_subaccount() called.")  

    ## Updated sub-account 
    logger.info(f"[Response value] {updated_subaccount}");  
    logger.debug(f"[Response value] {type(updated_subaccount)}");
    
    logger.debug(f"Waiting for WACM to complete account UPDATE : {id}");
    time.sleep(5)      
    logger.debug(f"Resuming test ...");

    # Get Updated sub-account information
    new_updated_subaccount = get_a_specific_subaccount(id)  
    ## Updated sub-account 
    logger.info(f"[Updated Value] {new_updated_subaccount}");  
    logger.debug(f"[Updated Value] {type(new_updated_subaccount)}");
    
    logger.info(f"updated_subaccount test completed.");  

# generate dummy update param
# for test the update_subaccount()
def generate_dummy_update_param():

    from waca_toolbox import randomname

    NEW_EMAIL_DOMAIN_NAME = "@poweredbywasabi.ai"    

    param = {}
    # Specify the account information to be updated here 
    #    {
    #        "AcctName": type("string"),                     # string (Mandatory)   
    #        "Password": type("string"),                     # string                                   
    #        "NumTrailDays": type(30),                      # int
    #        "QuotaGB": type(1),                             # int
    #        "ConvertToPaid": type(False),                   # Boolean
    #        "ResetAccessKeys": type(False),                 # Boolean
    #        "PasswordResetRequired": type(True),            # Boolean
    #        "EnableFTP": type(True),                        # Boolean
    #        "Inactive": type(False),                        # Boolean
    #        "SendPasswordSetToSubAccountEmail": type(True), # Boolean
    #        "AllowAccountDelete": type(True),               # Boolean
    #        "DisableMFA": type(False),                      # Boolean        
    #    }

    # placeholder (to be in the first order)
    param['AcctNum'] = 0
    
    # From here you can specify which key to update with the random value
    # New updated AcctName 
    key = "AcctName"
    param[key] = randomname(24) + NEW_EMAIL_DOMAIN_NAME
    logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated Password
    #key = "Password"
    #param[key] = randomname(12)
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated NumTrailDays
    #key = "NumTrailDays"
    #param[key] = random.randrange(1, 30, 5) # from 10 to 90, 5 days step
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated QuotaGB
    key = "QuotaGB"
    param[key] = random.randrange(20, 1000, 50) # from 10 to 1000, 50 GB step
    logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated ConvertToPaid
    #key = "ConvertToPaid"
    #param[key] = random.choice([True, False])
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated ResetAccessKeys
    key = "ResetAccessKeys"
    param[key] = random.choice([True, False])
    logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated PasswordResetRequired
    #key = "PasswordResetRequired"
    #param[key] = random.choice([True, False])
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated EnableFTP
    key = "EnableFTP"
    param[key] = random.choice([True, False])
    logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated Inactive
    #key = "Inactive"
    #param[key] = random.choice([True, False])
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated SendPasswordSetToSubAccountEmail
    #key = "SendPasswordSetToSubAccountEmail"
    #param[key] = random.choice([True, False])
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated AllowAccountDelete
    #key = "AllowAccountDelete"
    #param[key] = random.choice([True, False])
    #logger.info(f"New Updated Sub-account {key} = {param[key]}")
    # New updated DisableMFA
    key = "DisableMFA"
    param[key] = random.choice([True, False])
    logger.info(f"New Updated Sub-account {key} = {param[key]}")

    return param


def main():
    #create_update_delete()
    update_existing()

if __name__ == "__main__":
    main()