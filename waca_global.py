# ======================================
# WACA API SDK (Python)
# No guaranty from Wasabi Inc.
# ======================================
# WACA global variables

#global GBL_WACA_CONF_SUB_PATH
#global GBL_WACA_PROFILE

# WACA configuration file
GBL_WACA_CONF_SUB_PATH = "/.wasabi/waca.conf"
# WACA Profile default
GBL_WACA_PROFILE = "default"

# Example config file
# [default]
# endpoint_url = https://partner.wasabibeta.com
# api_key_value = xxxxxxxxxxxxxxxxxxxxxxxx
# [wasabi]
# endpoint_url = https://partner.wasabisys.com
# api_key_value = xxxxxxxxxxxxxxxxxxxxxxxx
# EOF
# -------------------------------------------------------------------------------------------------------------
# GBL_WACA_PROFILE is a global variable that can be reference from any module
# If the WACA Profile need to be modified, for case of debugging or/and to switch between multiple API KEYS/URLS
# this variable can be modified at the initiation stage before calling the functions to interact with WACA
# EXAMPLE
# (implement the followin code in your source code at the initiation stage)
# GBL_WACA_PROFILE = 'wasabi'
# ( ~/.wasabi/waca.conf to have the [<GBL_WACA_PROFILE>] section)


