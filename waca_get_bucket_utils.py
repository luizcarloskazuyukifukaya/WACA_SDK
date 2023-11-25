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
# GET Bucket Utilizations
# https://docs.wasabi.com/docs/get-bucket-utilizations
# GET /v1/utilizations/buckets 
# -----------------------------------------------
# INPUT (optional, when provided both should be specified)
# f: Start date of the utilization (ex. f='2023-11-20')
# t: End date of the utilization (ex. t='2023-12-20')
# Example:
# utils = get_util_bucket_utils(f='2023-10-20', t='2023-12-20') 
# -----------------------------------------------
# Return all daily utilizations of both Control and sub-account
# which is broken down into per-bucket components.
# ===============================================
# Response
# SUCCESS
#[
#    {
#        "BucketUtilizationNum": 6947980,
#        "AcctNum": 101430,
#        "AcctPlanNum": 0,
#        "BucketNum": 1011082,
#        "StartTime": "2019-12-26T00:00:00Z",
#        "EndTime": "2019-12-27T00:00:00Z",
#        "CreateTime": "2019-12-27T08:11:13Z",
#        "NumBillableObjects": 1,
#        "NumBillableDeletedObjects": 0,
#        "RawStorageSizeBytes": 1073741824,
#        "PaddedStorageSizeBytes": 1073741824,
#        "MetadataStorageSizeBytes": 48,
#        "DeletedStorageSizeBytes": 0,
#        "OrphanedStorageSizeBytes": 0,
#        "NumAPICalls": 132,
#        "UploadBytes": 1077661331,
#        "DownloadBytes": 106958,
#        "StorageWroteBytes": 1073741824,
#        "StorageReadBytes": 0,
#        "NumGETCalls": 0,
#        "NumPUTCalls": 0,
#        "NumDELETECalls": 0,
#        "NumLISTCalls": 0,
#        "NumHEADCalls": 0,
#        "DeleteBytes": 0, "Bucket": "1.bug2189",
#        "Region": "us-east-1"
#    },
#]
# FAIL
#[] (NULL)
#
from datetime import datetime
def get_bucket_utils(**dateParams):
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
    if paramValidNum == 2:
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

    # GET /v1/utilizations/buckets
    url = "{}/v1/utilizations/buckets".format(url)

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
    #################################################################
    # case 1: no parameter
    logger.debug(f"Calling get_bucket_utils() ...")
    all_utils = get_bucket_utils()
    logger.debug(f"get_bucket_utils() completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 2: with parameter (f and t)
    logger.debug(f"Calling get_bucket_utils(f, t) ...")
    all_utils = get_bucket_utils(f="2023-11-03", t="2023-11-24")
    logger.debug(f"get_bucket_utils(f, t) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  

    #################################################################
    # case 3: with parameter (f only) [Should Fail]
    logger.debug(f"Calling get_bucket_utils(f) ...")
    all_utils = get_bucket_utils(f="2023-11-03")
    logger.debug(f"get_bucket_utils(f) completed.")  

    ## return value 
    logger.info(f"{all_utils}");  
    logger.debug(f"{type(all_utils)}");  


if __name__ == "__main__":
    main()