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
# GET Utilizations for Control and Sub-Accounts
# https://docs.wasabi.com/docs/get-utilizations-for-control-and-sub-accounts
# GET /v1/utilizations
# -----------------------------------------------
# INPUT (optional, when provided both should be specified)
# f: Start date of the utilization (ex. f='2023-11-20')
# t: End date of the utilization (ex. t='2023-12-20')
# Example:
# utils = get_util_control_subaccounts(f='2023-10-20', t='2023-12-20') 
# -----------------------------------------------
# Return the daily storage and data transfer associated 
# with the Control account and the sub-account, 
# across all buckets in both the Control and sub-accounts.
# ===============================================
# Response
# SUCCESS
#[
#    {
#        "UtilizationNum": 39247161,
#        "AcctNum": 693549,
#        "AcctPlanNum": 803221,
#        "StartTime": "2021-12-19T00:00:00Z",
#        "EndTime": "2021-12-20T00:00:00Z",
#        "CreateTime": "2021-12-20T02:22:41Z",
#        "NumBillableObjects": 3,
#        "NumBillableDeletedObjects": 0,
#        "RawStorageSizeBytes": 322122547200,
#        "PaddedStorageSizeBytes": 322122547200,
#        "MetadataStorageSizeBytes": 144,
#        "DeletedStorageSizeBytes": 0,
#        "OrphanedStorageSizeBytes": 0,
#        "MinStorageChargeBytes": 777389080432,
#        "NumAPICalls": 5,
#        "UploadBytes": 322122548200,
#        "DownloadBytes": 0,
#        "StorageWroteBytes": 322122547200,
#        "StorageReadBytes": 0,
#        "NumGETCalls": 0,
#        "NumPUTCalls": 3,
#        "NumDELETECalls": 0,
#        "NumLISTCalls": 0,
#        "NumHEADCalls": 0,
#        "DeleteBytes": 0
#    },
#]
# FAIL
#[] (NULL)
#
from datetime import datetime
def get_util_control_subaccounts(**dateParams):
    # initializing format
    format = "%Y-%m-%d"
    
    # number of valid parameters 
    paramValidNum = 0
    fromDate = ""  # start date 'YY-MM-DD'
    toDate   = ""  # end date 'YY-MM-DD'
    
    ## Sub-Accounts Information
    accts = {}   

    logger.debug(f"Input parameter =  {dateParams}")

    for key, value in dateParams.items():
        logger.debug(f"{key}: {value}")
        
        # check date format
        try:
            res = bool(datetime.strptime(value, format))
            if key == "f":
                logger.debug(f"From date = {value}")
                fromDate = value
                paramValidNum = paramValidNum + 1
            if key == "t":
                logger.debug(f"To date = {value}")
                toDate = value
                paramValidNum = paramValidNum + 1

        except ValueError:
            res = False
            break

        if paramValidNum == 2:
            break
        
    if paramValidNum == 2:
        logger.debug(f"Input parameter is valid")
        logger.info(f"From date = {fromDate}")
        logger.info(f"To date = {toDate}")
    elif paramValidNum == 0:
        logger.debug(f"No input parameter given.")
    else:
        logger.error(f"Input parameter is wrong")
        return accts # {} NULL

    # From here either param is 2 or 0 and is valid
    # fromDate, toDate to be used when paramValidNum == 2
    httpParam = {}
    httpParam['from'] = fromDate
    httpParam['to'] = toDate
    logger.debug(f"HTTP(s) param =  {httpParam}")

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

    url = "{}/v1/utilizations".format(url)

    logger.info(f"Target URL is {url}")

    ## GET request
    ## requests.get(url, params={key: value}, args)
    if paramValidNum == 0:
        r = requests.get( url, headers=api_head);
    elif paramValidNum == 2:
        r = requests.get( url, headers=api_head, params=httpParam);

    ## Response status code
    logger.info(f"status: {r.status_code}") ; 

    ## Response JSON
    logger.info(f"{r.json()}");  
    logger.debug(f"{type(r.json())}");  

    if r.status_code == 200:
        accts = r.json()       
    for util in accts:
        logger.debug("===================================================================================");
        logger.debug(util);
        logger.debug("-----------------------------------------------------------------------------------");
        logger.info(f"Utilization Number : {util['UtilizationNum']}");
        logger.info(f"Account Number     : {util['AcctNum']}");
        logger.info(f"Account Plan Number: {util['AcctPlanNum']}");
        logger.info(f"Start Time         : {util['StartTime']}");
        logger.info(f"End Time           : {util['EndTime']}");
        logger.info(f"Create Time        : {util['CreateTime']}");        

    return accts

# for the execution of this script only
def main():
    #################################################################
    # case 1: no parameter
    logger.debug(f"Calling get_util_control_subaccounts() ...")
    all_utils = get_util_control_subaccounts()
    logger.debug(f"get_util_control_subaccounts() completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 2: with parameter (f and t)
    logger.debug(f"Calling get_util_control_subaccounts(f, t) ...")
    all_utils = get_util_control_subaccounts(f="2023-11-03", t="2023-11-24")
    logger.debug(f"get_util_control_subaccounts(f, t) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 3: with parameter (f only) [Should Fail]
    logger.debug(f"Calling get_util_control_subaccounts(f) ...")
    all_utils = get_util_control_subaccounts(f="2023-11-03")
    logger.debug(f"get_util_control_subaccounts(f) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  


if __name__ == "__main__":
    main()