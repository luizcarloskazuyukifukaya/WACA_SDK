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
# GET Utilizations for Control and Sub-Accounts
# https://docs.wasabi.com/docs/get-regional-utilizations-for-a-sub-account-across-all-buckets
# GET /v1/accounts/<AcctNum>/utilizations?includeRegionalUtilizations=true
# -----------------------------------------------
# INPUT Mandatory
# AcctNum: sub-account id (int)
# INPUT (optional)
# rgn: True, with regional utilizations
# Example1:
# utils = get_util_rgn_util_subaccnt_bkt(id, rgn=True)
# Example2:
# utils = get_util_rgn_util_subaccnt_bkt(id)
# Equal to rgn=False is given, no regional utilizations included 
# -----------------------------------------------
# Return the daily storage and data transfer associated 
# with the  sub-account specified with the AcctNum (id), 
# across all buckets in the specified sub-account.
# ===============================================
# Response
# SUCCESS
#[
#    {
#        "UtilizationNum": 1063777,
#        "AcctNum": 101430,
#        "AcctPlanNum": 20499,
#        "StartTime": "2019-12-26T00:00:00Z",
#        "EndTime": "2019-12-27T00:00:00Z",
#        "CreateTime": "2019-12-27T08:11:14Z",
#        "NumBillableObjects": 2,
#        "NumBillableDeletedObjects": 0,
#        "RawStorageSizeBytes": 2147483648,
#        "PaddedStorageSizeBytes": 2147483648,
#        "MetadataStorageSizeBytes": 96,
#        "DeletedStorageSizeBytes": 0,
#        "OrphanedStorageSizeBytes": 0,
#        "MinStorageChargeBytes": 1097364144032,
#        "NumAPICalls": 223,
#        "UploadBytes": 1794628020,
#        "DownloadBytes": 191771,
#        "StorageWroteBytes": 1788095943,
#        "StorageReadBytes": 0,
#        "NumGETCalls": 0,
#        "NumPUTCalls": 213,
#        "NumDELETECalls": 0,
#        "NumLISTCalls": 4,
#        "NumHEADCalls": 0,
#        "DeleteBytes": 0,
#        "RegionalUtilizations": {
#            "us-east-1": {
#                "NumBillableObjects": 1,
#                "NumBillableDeletedObjects": 0,
#                "RawStorageSizeBytes": 1073741824,
#                "PaddedStorageSizeBytes": 1073741824,
#                "MetadataStorageSizeBytes": 48,
#                "DeletedStorageSizeBytes": 0,
#                "OrphanedStorageSizeBytes": 0,
#                "NumAPICalls": 132,
#                "UploadBytes": 1077661331,
#                "DownloadBytes": 106958,
#                "StorageWroteBytes": 1073741824,
#                "StorageReadBytes": 0,
#                "NumGETCalls": 0,
#                "NumPUTCalls": 128,
#                "NumDELETECalls": 0,
#                "NumLISTCalls": 2,
#                "NumHEADCalls": 0,
#                "DeleteBytes": 0
#            },
#            "us-west-1": {
#                "NumBillableObjects": 1,
#                "NumBillableDeletedObjects": 0,
#                "RawStorageSizeBytes": 1073741824,
#                "PaddedStorageSizeBytes": 1073741824,
#                "MetadataStorageSizeBytes": 48,
#                "DeletedStorageSizeBytes": 0,
#                "OrphanedStorageSizeBytes": 0,
#                "NumAPICalls": 88,
#                "UploadBytes": 716963101,
#                "DownloadBytes": 76027,
#                "StorageWroteBytes": 714354119,
#                "StorageReadBytes": 0,
#                "NumGETCalls": 0,
#                "NumPUTCalls": 85,
#                "NumDELETECalls": 0,
#                "NumLISTCalls": 1,
#                "NumHEADCalls": 0,
#                "DeleteBytes": 0
#            }
#        }    
#    }
#]
# FAIL
#[] (NULL)
#
def get_rgn_util_subacct_bckt(id, **param):
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


#        if paramValidNum == 1:
#            # disregard other parameters
#            break
        
    if paramValidNum == 1:
        logger.debug(f"Input parameter is valid")
        logger.info(f"includeRegionalUtilizations = {rgnValue}")
    elif paramValidNum == 0:
        logger.debug(f"No input parameter given.")
    else:
        logger.error(f"Input parameter is wrong")
        return accts # {} NULL
        
    # The sub-account AcctNum is specified with 'id'
    # if rgn = True, then includeRegionalUtilizations=true is added in the request parameter
    httpParam = {}
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

    #/v1/accounts/<AcctNum>/utilizations?includeRegionalUtilizations=true
    url = "{}/v1/accounts/{}/utilizations".format(url, id)

    logger.info(f"Target URL is {url}")

    ## GET request
    ## requests.get(url, params={key: value}, args)
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

    from waca_toolbox import get_random_subaccount

    # AcctNum
    id = 0
    
    # Instead of creating new subaccount, let's get from existing one
    id = get_random_subaccount()
    #
    # id = 1058180 # fixed account
    #id = 1060004 
    logger.info(f"Target AcctNum for update is {id}");

    #################################################################
    # case 1: no parameter
    logger.debug(f"Calling get_rgn_util_subacct_bckt(id) ...")
    all_utils = get_rgn_util_subacct_bckt(id)
    logger.debug(f"get_rgn_util_subacct_bckt(id).")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 2: with parameter (id, rng=True)
    logger.debug(f"Calling get_rgn_util_subacct_bckt(id, rng=True) ...")
    all_utils = get_rgn_util_subacct_bckt(id, rng=True)
    logger.debug(f"get_rgn_util_subacct_bckt(id, rng=True) Done...")

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 3: with parameter (id, rng='false')
    logger.debug(f"Calling get_rgn_util_subacct_bckt(id, rng=True) ...")
    all_utils = get_rgn_util_subacct_bckt(id, rng=True)
    logger.debug(f"get_rgn_util_subacct_bckt(id, rng=True) Done...")

    ## return value 
    logger.info(f"{all_utils}");
    logger.debug(f"{type(all_utils)}");  
    #################################################################


if __name__ == "__main__":
    main()