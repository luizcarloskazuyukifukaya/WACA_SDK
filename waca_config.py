# ======================================
# Python WACA SDK
# Python SDK with Wasabi Account Control API
# No guaranty from Wasabi Inc.
# ======================================

# Define function to purse configuration file (waca.conf)
# INPUT: config file
# OUTPUT: dictionary {'endpoint_url':'<URL>', 'api_key_value':'<API_KEY_VALUE>', 'profile':'<PROFILE_NAME>'}
# -------------------------------------------------------------------------------------------------------------
# Example config file
# [default]
# endpoint_url = https://partner.wasabibeta.com
# api_key_value = xxxxxxxxxxxxxxxxxxxxxxxx
# [wasabi]
# endpoint_url = https://partner.wasabisys.com
# api_key_value = xxxxxxxxxxxxxxxxxxxxxxxx
# EOF
# -------------------------------------------------------------------------------------------------------------
# g.GBL_WACA_PROFILE is a global variable that can be reference from any module
# If the WACA Profile need to be modified, for case of debugging or/and to switch between multiple API KEYS/URLS
# this variable can be modified at the initiation stage before calling the functions to interact with WACA
# EXAMPLE
# (implement the following code in your source code at the initiation stage)
# import waca_global as g
# g.GBL_WACA_PROFILE = 'wasabi'

import waca_global as g

from logging import getLogger
logger = getLogger(__name__)

from os.path import expanduser
home = expanduser("~")

# return value when the input is not valid
INVALID_KEY = 'no_key'
INVALID_VALUE = ''

def parse_conf():
    # global variable
    # g.GBL_WACA_PROFILE
    # g.GBL_WACA_CONF_SUB_PATH
    
    target_profile = ''
    waca_api_inf = {'api_key':'', 'endpoint':''}

    if len(g.GBL_WACA_PROFILE) == 0:
        g.GBL_WACA_PROFILE = 'default'
        
    profile = g.GBL_WACA_PROFILE
    print('Target profile is ' + profile)
         
    # profile is set either default or specific value    
    target_profile = '[' + profile + ']';
    
    # open configuration file
    conf_file_path = home + g.GBL_WACA_CONF_SUB_PATH;
    file = open(conf_file_path, 'r')
    lines = file.readlines()
    
    target_profile_found = False
    target_counts = 0 # when both key found, the configuration file read to end
    for line in lines:
        l = line.strip()
        if len(l) == 0:
            continue

        # line is not spaced only
        k , v = extract_key(l)
            
        if k == INVALID_KEY:
            continue

        if k == target_profile:
            target_profile_found = True
            continue

        if target_profile_found == False:
            continue
        
        # only when the target profile is found
        if k == 'api_key_value':
            waca_api_inf['api_key'] = v
            target_counts = target_counts + 1

        if k == 'endpoint_url':
            waca_api_inf['endpoint'] = v
            target_counts = target_counts + 1
        
        if target_counts == 2:
            break                
    # read line and identify the start of profile information   
    # return WACA API configuration information as dictionary
    return waca_api_inf


def extract_key(l):
    # space only line
    l = l.strip()
    if len(l) == 0:
        return INVALID_KEY, INVALID_VALUE;
    
    # l should have content, but skip comments (line starting with #)
    if l[0] == '#':
        return INVALID_KEY, INVALID_VALUE;
    
    # l should have content, but skip comments (line starting with #)
    if l[0] == '[':
        return l, None;

    # find start of comment and remove the remaining characters
    l = l.split('#', 1)[0];
    
    # split the line by ':'
    keys = l.split('=')
    
    #print(keys)
    if len(keys) == 2:
        return f"{keys[0].strip()}",f"{keys[1].strip()}";
    else:
        print("The configuration file syntax is not correct. Please check the format of the file.");
        return INVALID_KEY, INVALID_VALUE;

# Main function defined here
import sys

def main():
    #g.GBL_WACA_PROFILE
    
    if len(sys.argv) == 1:
        g.GBL_WACA_PROFILE = 'default'
        api_conf = parse_conf()
    else:
        print(sys.argv[1])
        g.GBL_WACA_PROFILE = sys.argv[1]
        print(g.GBL_WACA_PROFILE)
        api_conf = parse_conf()
        
    print(api_conf)

# for the execution of this script only
if __name__ == "__main__":
    main()