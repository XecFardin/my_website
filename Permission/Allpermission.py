import requests
from datetime import date, datetime
import csv
from requests.api import get
import boto3
import sys

username="+919860709109"
password="malcolm123"
ENV_NAME="prod"

accId = sys.argv[1]

    


def getAllPermission(accId,AccessToken):
    
    payload={
               "version": 1,
                "msgType":"get_accessor_permissions",
                "data":{
                            "accessorId":accId
                     }
            }
    headers = {'Accept': '*/*','Content-Type':'application/json','Authorization':AccessToken}
    response = requests.post(url=Url,json=payload,headers=headers) 
    msg=response.json()
    message=msg['message']
    if msg['type']=='error':
        print("\nError!\n")
    else:
        date = datetime.now().strftime("%Y_%m_%d-%I:%M:%S_%p")
        message=msg['message']
        if message == 'Forbidden':
            print('message is '+message)
        else:
            if message['permissions']!=[]:

                with open('Permission_accessorId_'+accId+'_'+ENV_NAME+'_date_'+date+'.csv','w',newline='') as file:
                    fieldnames = ['accessPointId', 'mobile','card','fingerprint','clickToAccess Range','proximityAccess','tapToAccess','remoteAccess']
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                
                    for accecessPonit in message['permissions']:
                        id=accecessPonit['accessPointId']
                        mobile=accecessPonit['mobile']['enabled']
                        click=accecessPonit['mobile']['settings']['clickToAccessRange']
                        proxiy=accecessPonit['mobile']['settings']['proximityAccess']
                        tap=accecessPonit['mobile']['settings']['tapToAccess']
                        remote=accecessPonit['mobile']['settings']['remoteAccess']
                        card=accecessPonit['card']['enabled']
                        fingerprint=accecessPonit['fingerprint']['enabled']
                        writer.writerow({'accessPointId':id, 'mobile':mobile,'card':card,'fingerprint':fingerprint,'clickToAccess Range':click,'proximityAccess':proxiy,'tapToAccess':tap,'remoteAccess':remote})
                    print("\ncsv file is generated with the data\n")
            else:
                print("\nno permissions have been set! \n")                      
            





ENV_NAME = ENV_NAME.lower()

if ENV_NAME == 'dev':
    Url='https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/dev/developerSupport/support/commands'
    
elif ENV_NAME == 'prod':
    Url='https://nqfdy5tisa.execute-api.ap-south-1.amazonaws.com/prod/developerSupport/support/commands'
    
elif ENV_NAME == 'test':
    Url='https://gpmf48dy80.execute-api.ap-south-1.amazonaws.com/test/developerSupport/support/commands'
    
elif ENV_NAME == 'sandbox':
    Url='https://6283buo7y6.execute-api.ap-south-1.amazonaws.com/sandbox/developerSupport/support/commands'
    
else:
     print( "\nplease Enter valid input example : test or dev or sandbox or prod\n")
     sys.exit()
     




def initiate_auth(username, password):
    CLIENT_ID ='64merk1devje3k214e1lqj9fcg'
    region='ap-south-1'
    try:
        client = boto3.client('cognito-idp', region_name=region)
        resp = client.initiate_auth(
            ClientId=CLIENT_ID,
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password,
            },
            ClientMetadata={
                'username': username,
                'password': password, })
        AccessToken =resp['AuthenticationResult']['AccessToken']
        getAllPermission(accId,AccessToken)
    except Exception as e:
        print("\n")
        print(e)
        
initiate_auth(username,password)




    


