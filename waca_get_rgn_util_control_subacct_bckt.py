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

## WACA API specific URL
# -----------------------------------------------
# GET Regional Utilizations for Control and Sub-Accounts Across All Buckets
# https://docs.wasabi.com/docs/get-regional-utilizations-for-control-and-sub-accounts-across-all-buckets
# GET /v1/utilizations?includeRegionalUtilizations=true
# -----------------------------------------------
# INPUT (optional)
# rgn='true'
# IncludeRegionalUtilizations: True if regional utilizations should be included
# Example1:
# utils = get_util_rgn_util_control_subaccnt_bkt(rgn=True)
# Example2:
# utils = get_util_rgn_util_control_subaccnt_bkt()
# Equal to rgn=False is given, no regional utilizations included 
# -----------------------------------------------
# Return the daily storage and data transfer associated with the Control and sub-account, 
# across all buckets in the Control and sub-account along with regional utilizations.
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
#        "NumAPICalls": 0,
#        "UploadBytes": 0,
#        "DownloadBytes": 0,
#        "StorageWroteBytes": 0,
#        "StorageReadBytes": 0,
#        "NumGETCalls": 0,
#        "NumPUTCalls": 0,
#        "NumDELETECalls": 0,
#        "NumLISTCalls": 0,
#        "NumHEADCalls": 0,
#        "DeleteBytes": 0,
#        "RegionalUtilizations": {
#            "us-east-1": {
#                "NumBillableObjects": 3,
#                "NumBillableDeletedObjects": 0,
#                "RawStorageSizeBytes": 322122547200,
#                "PaddedStorageSizeBytes": 322122547200,
#                "MetadataStorageSizeBytes": 144,
#                "DeletedStorageSizeBytes": 0,
#                "OrphanedStorageSizeBytes": 0,
#                "NumAPICalls": 0,
#                "UploadBytes": 0,
#                "DownloadBytes": 0,
#                "StorageWroteBytes": 0,
#                "StorageReadBytes": 0,
#                "NumGETCalls": 0,
#                "NumPUTCalls": 0,
#                "NumDELETECalls": 0,
#                "NumLISTCalls": 0,
#                "NumHEADCalls": 0,
#                "DeleteBytes": 0
#            }
#        }
#    }
#]
# FAIL
#[] (NULL)
#
def get_rgn_util_control_subacct_bkt(**param):
    
    # number of valid parameters 
    paramValidNum = 0
    rgnValue = False
    
    ## Sub-Accounts Information
    accts = {}   

    logger.debug(f"Input parameter =  {param}")

    for key, value in param.items():
        logger.debug(f"{key}: {value}")
        
        if key == "rgn":
            logger.debug(f"rgn param specified = {value} , type = {type(value)}")
            if type(value) == type(True):
                rgnValue = value
                paramValidNum = paramValidNum + 1
            else:
                logger.error(f"rgn param specified, but the value type is wrong. type = {type(value)}")
                paramValidNum = -1
        else:
            # Other parameter specified
            logger.error(f"Other invalid param specified = {value} , type = {type(value)}")
            paramValidNum = -1
            break

    if paramValidNum == 1:
        logger.debug(f"Input parameter is valid")
        logger.info(f"includeRegionalUtilizations = {rgnValue}")
    elif paramValidNum == 0:
        logger.debug(f"No input parameter given.")
    else:
        logger.error(f"Input parameter is wrong")
        return accts # {} NULL

    # From here either param is 1 or 0 and is valid
    # if rgn = True, then includeRegionalUtilizations=true is added in the request parameter
    httpParam = {}
    if rgnValue:    # only specify the param when it is true
        httpParam['includeRegionalUtilizations'] = rgnValue
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
    r = requests.get( url, headers=api_head, params=httpParam)
 
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
    logger.debug(f"Calling get_rgn_util_control_subacct_bckt() ...")
    all_utils = get_rgn_util_control_subacct_bkt()
    logger.debug(f"get_util_control_subaccounts() completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  
    #################################################################
    # case 2: with parameter (rgn=True)
    logger.debug(f"Calling get_rgn_util_control_subacct_bkt(rgn) ...")
    all_utils = get_rgn_util_control_subacct_bkt(rgn=True)
    logger.debug(f"get_rgn_util_control_subacct_bkt(rgn) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  
    #################################################################
    # case 3: with parameter (rgn=False)
    logger.debug(f"Calling get_rgn_util_control_subacct_bkt(rgn) ...")
    all_utils = get_rgn_util_control_subacct_bkt(rgn=False)
    logger.debug(f"get_rgn_util_control_subacct_bkt(rgn) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  
    #################################################################
    # case 4: with parameter (rgn='true') Fail (string value)
    logger.debug(f"Calling get_rgn_util_control_subacct_bkt(rgn) ...")
    all_utils = get_rgn_util_control_subacct_bkt(rgn='true')
    logger.debug(f"get_rgn_util_control_subacct_bkt(rgn) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 5: with parameter (regional=True) Fail (key name should be rgn)
    logger.debug(f"Calling get_rgn_util_control_subacct_bkt(none rgn key ) ...")
    all_utils = get_rgn_util_control_subacct_bkt(reginal='true')
    logger.debug(f"get_rgn_util_control_subacct_bkt(none rgn key) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 6: with parameter (regional=True, rgn=True) Fail (key name should be rgn + valid key and value)
    logger.debug(f"Calling get_rgn_util_control_subacct_bkt(none rgn key and valid one ) ...")
    all_utils = get_rgn_util_control_subacct_bkt(rgn=True, other='true')
    logger.debug(f"get_rgn_util_control_subacct_bkt(none rgn key and valid one) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

if __name__ == "__main__":
    main()