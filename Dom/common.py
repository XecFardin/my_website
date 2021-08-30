
import csv
import os
from re import L
import boto3
import sys
import updateSdkData





DEV_COGNITO_CLIENT_ID ='64merk1devje3k214e1lqj9fcg'
DEV_COGNITO_REGION = 'ap-south-1'
TEST_COGNITO_CLIENT_ID ='64merk1devje3k214e1lqj9fcg'
TEST_COGNITO_REGION = 'ap-south-1'
SANDBOX_COGNITO_CLIENT_ID ='64merk1devje3k214e1lqj9fcg'
SANDBOX_COGNITO_REGION = 'ap-south-1'
PROD_COGNITO_CLIENT_ID ='64merk1devje3k214e1lqj9fcg'
PROD_COGNITO_REGION = 'ap-south-1'

 

def saveListToCsvFile(fileName,listData):

    fo = open(fileName,"w")
    csvWriter = csv.writer(fo)

    for i in range(0,len(listData)):
        csvWriter.writerow(listData[i])
    
    fo.close()


     


def cognitoLogin(envName,cognito_login,cognito_password):

    if envName == 'dev':
        cognito_client_id = DEV_COGNITO_CLIENT_ID
        cognito_region = DEV_COGNITO_REGION
    elif envName == 'test':
        cognito_client_id = TEST_COGNITO_CLIENT_ID
        cognito_region = TEST_COGNITO_REGION        
    elif envName == 'sandbox':
        cognito_client_id = SANDBOX_COGNITO_CLIENT_ID
        cognito_region = SANDBOX_COGNITO_REGION
    elif envName == 'prod':
        cognito_client_id = PROD_COGNITO_CLIENT_ID
        cognito_region = PROD_COGNITO_REGION        
    else:
        print( "Incorrect environment passed to \"cognitoLogin\" function. Passed environment = {}" .format(envName))
        sys.exit()
        
    
    try:
        client = boto3.client('cognito-idp',region_name=cognito_region)
        resp = client.initiate_auth(
            ClientId=cognito_client_id,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': cognito_login,
                'PASSWORD': cognito_password,
            },
            ClientMetadata={
                'username': cognito_login,
                'password': cognito_password, })
        accessToken =resp['AuthenticationResult']['AccessToken']
        return accessToken

    except Exception as e:
        print( "Login failed for \"cognitoLogin\" function!")
        print(e)
def updateSdk(update):
    if update:
        updateSdkData.getLoginCredentials()
    else:
        print("No changes will be made in sdk data!")
        sys.exit()
    
