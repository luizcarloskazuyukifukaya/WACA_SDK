# Python WACA SDK
Python SDK with Wasabi Account Control API

The details of the Wasabi Account Control API (WACA) is published on the following URL:
https://docs.wasabi.com/docs/account-control-api

As explained in this document, WACA is a set of RESTful JSON methods to interact with Wasabi Account Control Manager (WACM), which is the web-based UI tool provided by Wasabi.

This SDK is the high level programming module written in Python, and its purpose is to provide easy and quick method to develop an application to interact/integrate with WACM. The methods exposed with this SDK simply is a rapping high level function written in Python that utilize WACA itself.

If you are familiar with Python, and intend to develop an application/system it might be easier achieving your objectives utilizing this SDK.

## Profile and WACA configurations
Just like the AWS CLI credentials file, WACA config file is introduced in the Python WACA SDK.
This is to provide a way to switch target WACA endpoint URLs and the associated WACA API Key without changing the source codes.

You can define a "Profile" that holds the endpoint URL and the associated WACA API Key, and it is possible to define multiple profiles. These information are managed by the WACA configuration file named waca.conf, which is to be installed on the following path:
~/.wasabi/waca.conf

*(Important)* Please create the .wasabi folder, under your home directory, and the waca.conf manually as at this moment, there is no SDK installer created to automate the setup.

(note) Please refer to the following AWS document explaining details of the configuration files:
https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html

### ~/.wasabi/waca.conf
The following is a sample of the WACA Configuration file for the use with the sample code provided here:
```
[default]
endpoint_url = https://partner.wasabibeta.com
api_key_value = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[wasabibeta]
endpoint_url = https://partner.wasabibeta.com
api_key_value = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[wasabisys]
endpoint_url = https://partner.wasabisys.com
api_key_value = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```