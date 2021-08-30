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
DEFAULT_MOBILE_ID = "8777"
DEFAULT_ACCESSOR_ID = "1100"

#ALL VARIABLES ABOVE ARE RUNTIME VARIABLES. THEY CAN BE UPDATED BY WHOEVER IS RUNNING THE SCRIPT.
#PLEASE DO NOT TOUCH THE BELOW VARIABLE. CONTACT THE DEVELOPER TO CHANGE THE BELOW VARIABLES.


DEV_DS_BASE_ADDR = 'https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/dev/developerSupport/support/'
TEST_DS_BASE_ADDR = 'https://gpmf48dy80.execute-api.ap-south-1.amazonaws.com/test/developerSupport/support/'
SANDBOX_DS_BASE_ADDR = 'https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/sandbox/developerSupport/support/'
PROD_DS_BASE_ADDR = 'https://nqfdy5tisa.execute-api.ap-south-1.amazonaws.com/prod/developerSupport/support/'        


def updateSdkData(envName,mobileId,accessorId,cognitoToken):

    payload={
    "version": 1,
    "msgType":"update_sdk_data",
    "data":{
    	"accessorId":accessorId,
        "mobileId":mobileId
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
            print("\nSdkdata for mobileId {} is successfully updated!\n".format(mobileId))

            

        else:
            print("MobileId {}  does not have a Mobile details!\n" .format(mobileId))
            print("For audit purposes a log has been generated in cloud with the inputs of the script and {} cognito user!\n" .format(cognito_login))


 
def validateInput():

    print("\n")

    selected_env = DEFAULT_ENV
    
    selected_mobile_id = DEFAULT_MOBILE_ID

    selected_accessor_id = DEFAULT_ACCESSOR_ID
    
    atleastOneargumentPresent = False
        

    if (len(sys.argv) > 1):

        for i in range(1,len(sys.argv)):

            presentArg = sys.argv[i]
            presentArgLC = sys.argv[i].lower()

            if presentArgLC == '-h' or presentArgLC == '--help':
                print("Usage 1 - Specify MobileId and AccessorId : python3 updateSdkData.py -a accessorId -m mobileId  -e env_name")
                print("accessorId 1100(should be a number),mobileId = 8944(should be a number) and  Env name = dev/test/sandbox/prod")
                print("any of the above arguments can be skipped(default values are taken from script) or all can be skipped by using -na for argument")
                print("Usage 1 Example: python3 updateSdkData.py -a 8944 -m 8777 -e dev")
                print("Usage 1 Example: python3 updateSdkData.py -a 8944 -m 8777")
                sys.exit()

            if presentArgLC == '-v' or presentArgLC == '-version':
                print("Script version : {}" .format(script_version))
                sys.exit()

            if presentArgLC == '-a':
                selected_accessor_id = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True

            if presentArgLC == '-m':
                selected_mobile_id = sys.argv[sys.argv.index(presentArg)+1].lower()                   
                atleastOneargumentPresent = True

            if presentArgLC == '-e':
                selected_env = sys.argv[sys.argv.index(presentArg)+1].lower()
                atleastOneargumentPresent = True

            if presentArgLC == '-na':
                atleastOneargumentPresent = True

            if atleastOneargumentPresent == False:
                print("Atleast one argument needs to be provided or use -na for no arguments! Please type 'python3 updateSdkData.py -h' or 'python3 updateSdkData.py --help' to get help with required arguments!")
                sys.exit()
                
            if selected_mobile_id.isnumeric()==False:
                print("MobileId provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()
            if selected_accessor_id.isnumeric()==False:
                print("Offset Value provided is not valid! it should be a number")
                print("Exiting script!")
                sys.exit()

       
        
        cognitoToken = common.cognitoLogin(selected_env,cognito_login,cognito_password)

        updateSdkData(selected_env,selected_mobile_id,selected_accessor_id,cognitoToken)

    else:
        print("Script requires arguments! Please type 'python3 updateSdkData.py -h' or 'python3 updateSdkData.py --help' to get help with required arguments!")
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
            
            validateInput()
        fr.close()
    except Exception as e:
        print("credentails.txt file is missing!")  
  


if __name__=="__main__":
    getLoginCredentials()

