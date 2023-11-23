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
#   "NumTrial Days": 30,                        # int       
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
# NumTrial Days, if specified, this will change the number of days associated with the trial period, up to a limit set on the Control Account.
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
        "NumTrial Days": type(30),                      # int
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
#        'Content-Type': 'application/json',
        'X-Wasabi-Service': 'partner',
    }
    # "Content-Type: application/json; charset=utf-8" # request( ,json=data )
    # Content-Type: application/json
    # X-Wasabi-Service: partner

    #POST /v1/accounts/134
    url = url + '/v1/accounts' + '/' + str(acctNum)
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
    r = requests.post( url, headers=api_head, json=acct);
     
    # ********* requests.post only works with 'data=acct' *************
    # Response code: 403
    # You are not permitted to complete that action
    #r = requests.post( url, headers=api_head, data=acct);

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
        logger.debug(newCreatedAcct);
        logger.debug("-----------------------------------------------------------------------------------");
        logger.info(f"Account Number: {newCreatedAcct['AcctNum']}");
        logger.info(f"Account Name  : {newCreatedAcct['AcctName']}");
    return newCreatedAcct

# for the execution of this script only
# this is only for the test of the updated_subaccount()
def create_dummy_subaccount():
    from waca_put_accounts import create_subaccount
    from waca_put_accounts import randomname
    
    EMAIL_DOMAIN_NAME = "@postwacawasabi.com"    
    
    param = {
        "AcctName": "",                              # string    (MANDATORY: email address)
#        "IsTrial": True,                            # Boolean   default: True
#        "Password": "@@@@@@@@@@@",                  # string    default: "Wasabisys"
#        "NumTrial Day": 30,                         # int       default: 30
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


# for the execution of this script only
# this is only for the test of the updated_subaccount()
# delete the dummy sub-account created for the test
def delete_dummy_subaccount(id):
    logger.debug(f"deleting sub-account AcctNum : {id}");  

    # to be added when the delete_subaccount is created

    logger.debug(f"deleted");  



# for the execution of this script only
def main():
    import time

    from waca_put_accounts import randomname

    NEW_EMAIL_DOMAIN_NAME = "@poweredbywasabi.ai"    

    # create dummy subaccount
    #id = create_dummy_subaccount()
    #logger.debug(f"Waiting for WACM to complete account creation : {id}");
    #time.sleep(10)
    #logger.debug(f"Resuming test ...");
    # Use static AcctNum 1058395, 1058394, 1059642
    id =  1058394

    param = {}

    # specify the target id (the new created subaccount)
    param['AcctNum'] = id
    logger.info(f"Target sub-account to be updated AcctNum is {id}.")

    # Specify the account information to be updated here 
    #    {
    #        "AcctName": type("string"),                     # string (Mandatory)   
    #        "Password": type("string"),                     # string                                   
    #        "NumTrial Days": type(30),                      # int
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

    # New updated AcctName 
    param["AcctName"] = randomname(24) + NEW_EMAIL_DOMAIN_NAME
    logger.debug(f"New Updated Sub-account AcctName = {param['AcctName']}")  
    
    logger.debug(f"Calling update_subaccount() ...")
    
    updated_subaccount = update_subaccount(**param)

    logger.debug(f"create_subaccount() completed.")  

    ## Updated sub-account 
    logger.info(f"{updated_subaccount}");  
    logger.debug(f"{type(updated_subaccount)}");  

    delete_dummy_subaccount(id)
    
    logger.info(f"updated_subaccount test completed.");  



if __name__ == "__main__":
    main()