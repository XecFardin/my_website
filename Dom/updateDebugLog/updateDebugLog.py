#Important!!!Please do not update the version below. This is to be updated only through proper version control by the owner of the script!!!
script_version = '0.0.2'
#Versions History
#Number     Date                Author          Change
#0.0.1     22-Aug-2021         Abdulla         Initial Version
#0.0.2     26-Aug-2021         Abdulla         Initial Version


import requests
from datetime import date, datetime
import time
import csv
from requests.api import get
import os
import boto3
import sys
sys.path.append(os.getcwd() + os.sep + os.pardir)
import common
#ALL VARIABLES BELOW ARE RUNTIME VARIABLES. THEY CAN BE UPDATED BY WHOEVER IS RUNNING THE SCRIPT.


cognito_password=""
cognito_login=""


DEFAULT_ENV = 'dev'
DEFAULT_ACCESSOR_ID = "8777"
DEFAULT_DEBUG_ENABLE = 'true'
DEFAULT_EXPIRY_DATE = '1617013395'
DEFAULT_EXPIRY_SIZE = '1000'
DEFAULT_UPLOAD_INTERVAL ='10'
DEFAULT_UPLOAD_POLL ='true'
DEFAULT_VERBOSITY_LEVEL  = 'verbose/info/debug/error'


#ALL VARIABLES ABOVE ARE RUNTIME VARIABLES. THEY CAN BE UPDATED BY WHOEVER IS RUNNING THE SCRIPT.
#PLEASE DO NOT TOUCH THE BELOW VARIABLE. CONTACT THE DEVELOPER TO CHANGE THE BELOW VARIABLES.


DEV_DS_BASE_ADDR = 'https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/dev/developerSupport/support/'
TEST_DS_BASE_ADDR = 'https://gpmf48dy80.execute-api.ap-south-1.amazonaws.com/test/developerSupport/support/'
SANDBOX_DS_BASE_ADDR = 'https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/sandbox/developerSupport/support/'
PROD_DS_BASE_ADDR = 'https://nqfdy5tisa.execute-api.ap-south-1.amazonaws.com/prod/developerSupport/support/'        


def updateDebugLog(envName,accessorId,debugEnabled,expiryDate,expirySize,uploadInterval,uploadOnPoll,verbosityLevel,cognitoToken):

    payload={
    "version": 1,
    "msgType":"debug_log",
    "data":{
         "accessorId":accessorId,
         "enabled":debugEnabled,
  	     "expiryDate":expiryDate,
         "expirySize": expirySize,
         "uploadInterval": uploadInterval,
         "uploadOnPoll": uploadOnPoll,
         "verbosityLevel": verbosityLevel
    }
}
    
    url = getCommandUrl(envName)
    headers = {'Accept': '*/*','Content-Type':'application/json','Authorization':cognitoToken}

    response = requests.post(url=url,json=payload,headers=headers)

    jsonResponse = response.json()
    if jsonResponse['type']=='error':

        print("Received error from backend application for \"updateSdkData\" function!")
        print(jsonResponse['message'])

    else:
        
        message = jsonResponse['type']

        if message != []:

            print("message: "+message)
            print("\nDebug Log for accessorId {} is successfully updated!\n".format(accessorId))
        else:
            print("accessorId {}  does not have a Mobile details!\n" .format(accessorId))
            print("For audit purposes a log has been generated in cloud with the inputs of the script and {} cognito user!\n" .format(cognito_login))
        update=input("\nDo you want to Update the Sdkdata? (y/n)\n")
        if update =='y':
            os.chdir("..")
            common.updateSdk(True)
        else:
            common.updateSdk(False)

 
def validateInput():

    print("\n")

    selected_env = DEFAULT_ENV
    
    selected_accessor_id = DEFAULT_ACCESSOR_ID
    selected_debug_enable = DEFAULT_DEBUG_ENABLE
    selected_expiry_date = DEFAULT_EXPIRY_DATE
    selected_expiry_size = DEFAULT_EXPIRY_DATE
    selected_upload_interval = DEFAULT_UPLOAD_INTERVAL
    selected_upload_poll = DEFAULT_UPLOAD_POLL
    selected_verbosity_level = DEFAULT_VERBOSITY_LEVEL

   
    atleastOneargumentPresent = False
        

    if (len(sys.argv) > 1):

        for i in range(1,len(sys.argv)):

            presentArg = sys.argv[i]
            presentArgLC = sys.argv[i].lower()

            if presentArgLC == '-h' or presentArgLC == '--help':
                print("Usage 1 - Specify accessorId,debugEnabled,expiryDate,expirySize,uploadInterval,uploadOnPoll and verbosityLevel  : python3 updateDebugLog.py -a accessorId -d debugEnable -x expiryDate -s expirySize -i uploadInterval -p uploadOnPoll -l verbosityLevel  -e env_name")
                print("accessorId = 8944(should be a number),debugEnabled = True/False ,expiryDate=1630149301(should be a number),expirySize = 5000(should be a number),uploadInterval=10(should be a number),uploadOnPoll = true/false(boolean),,verbosityLevel= verbose Env name = dev/test/sandbox/prod")
                print("any of the above arguments can be skipped(default values are taken from script) or all can be skipped by using -na for argument")
                print("Usage 1 Example: python3 updateDebugLog.py -a 1100  -d true -x 1630149301 -s 5000 -i 10 -p true -l verbose -e dev")
                print("Usage 1 Example: python3 updateDebugLog.py -a 1100  -d true -x 1630149301 -s 5000 -i 10 -p true -l verbose")
                sys.exit()

            if presentArgLC == '-v' or presentArgLC == '-version':
                print("Script version : {}" .format(script_version))
                sys.exit()

            if presentArgLC == '-a':
                selected_accessor_id = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-d':
                selected_debug_enable = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-x':
                selected_expiry_date = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-s':
                selected_expiry_size = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-i':
                selected_upload_interval = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-p':
                selected_upload_poll = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-l':
                selected_verbosity_level = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True
            if presentArgLC == '-e':
                selected_env = sys.argv[sys.argv.index(presentArg)+1].lower()
                atleastOneargumentPresent = True

            if presentArgLC == '-na':
                atleastOneargumentPresent = True

            if atleastOneargumentPresent == False:
                print("Atleast one argument needs to be provided or use -na for no arguments! Please type 'python3 updateDebugLog.py -h' or 'python3 updateDebugLog.py --help' to get help with required arguments!")
                sys.exit()
                
            if selected_accessor_id.isnumeric()==False:
                print("AccessorId provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()
            if selected_expiry_date.isnumeric()==False:
                print("Expiry date provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()
            if selected_expiry_size.isnumeric()==False:
                print("Expiry Size provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()
            if selected_upload_interval.isnumeric()==False:
                print("Upload Interval provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()
            if selected_debug_enable =='true':
                selected_debug_enable=True
            elif selected_debug_enable=='false':
                selected_debug_enable=False
            elif type(selected_debug_enable)==str:
                print("debug enable provided is not valid! it should be a boolean(True/False)")
                print("Exiting script!")
                sys.exit()
            if selected_upload_poll =='true':
                selected_upload_poll=True
            elif selected_upload_poll=='false':
                selected_upload_poll=False   
            elif type(selected_upload_poll)==str:
                print("upload on poll provided is not valid! it should be a boolean(True/False)")
                print("Exiting script!")
                sys.exit()

            if type(selected_verbosity_level)!=str:
                print("verbosity level  provided is not valid! it should be a boolean(True/False)")
                print("Exiting script!")
                sys.exit()
       
        cognitoToken = common.cognitoLogin(selected_env,cognito_login,cognito_password)

        updateDebugLog(selected_env,selected_accessor_id,selected_debug_enable,selected_expiry_date,selected_expiry_size,selected_upload_interval,selected_upload_poll,selected_verbosity_level,cognitoToken)

    else:
        print("Script requires arguments! Please type 'python3 updateDebugLog.py -h' or 'python3 updateDebugLog.py --help' to get help with required arguments!")
        sys.exit()

def getCommandUrl(envName):

    if envName == 'dev':
        url = DEV_DS_BASE_ADDR + 'commands'
    elif envName == 'test':
        url = TEST_DS_BASE_ADDR + 'commands'        
    elif envName == 'sandbox':
        url = SANDBOX_DS_BASE_ADDR + 'commands'
    elif envName == 'prod':
        url = PROD_DS_BASE_ADDR + 'commands'        
    else:
        print( "Incorrect environment passed to \"getCommandUrl\" function. Passed environment = {}" .format(envName))
        sys.exit()

    return url     
def getLoginCredentials():
    
    login_found = False
    password_found = False
    global cognito_login
    global cognito_password
        
    try:
        oldDir=os.getcwd()
        os.chdir("..")
        fr = open('credentials.txt',"r")
        
        for line in fr:
            line = line.strip()
            line = line.split(':')
            if line[0] == 'login':
                cognito_login = line[1]
                login_found = True
            elif line[0] == 'password':
                cognito_password = line[1]
                password_found = True
            else:
                print("Incorrect key value pair in credentials.txt file. Exiting Script!")
                sys.exit()

        if login_found == False or password_found == False:
            print("Login or password key value pair not found in credentials.txt file. Exiting Script!")
            sys.exit()
        else:
            os.chdir(oldDir)
            validateInput()
        fr.close()
    except Exception as e:
        print("credentails.txt file is missing!")


if __name__=="__main__":
    getLoginCredentials()

