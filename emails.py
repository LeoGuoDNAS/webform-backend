import asyncio
import json
import requests
from auth import acquire_access_token_without_user

email_address1 = 'lguo@wearetheone.com'
email_address2 = 'achowdhury@wearetheone.com'
user_id = '36d8ede0-773f-46b2-835d-c3988e9a39fe' # it

async def sendMessage(data: dict):
    access_token = await acquire_access_token_without_user()
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type' : 'application/json'}
    
    msg = {
        "message": {
            "subject": "[Action Required] New Service Request from non-contract customer webform",
            "body": {
                "contentType": "Text",
                "content": "Hello\n\nThere's a new service request from the non-contract customer webform whose site address does not match our records.\n\n" +
                    "Here are the details:\n\n" +
                    "Contact Info:\n\n" +
                    f"POC Name: {data['POCName']}\n" +
                    f"POC Email: {data['POCEmail']}\n" +
                    f"POC Phone Number: {data['POCPhoneNumber']}\n" +
                    f"POC Phone Number Ext: {data['POCPhoneNumberExt']}\n" +
                    f"POC Phone Two: {data['POCPhoneTwo']}\n" +
                    f"POC Phone Two Ext: {data['POCPhoneTwoExt']}\n\n" +

                    "Site Info:\n\n" +
                    f"Street One: {data['StreetOne']}\n" +
                    f"Street Two: {data['StreetTwo']}\n" +
                    f"Street Three: {data['StreetThree']}\n" +
                    f"Street Four: {data['StreetFour']}\n" +
                    f"City: {data['City']}\n" +
                    f"State: {data['State']}\n" +
                    f"Zip: {data['Zip']}\n" +
                    f"Possible Sites: {data['PossibleSites']}\n\n"

                    "Equipment Info:\n\n" +
                    f"Make: {data['Make']}\n" +
                    f"Model: {data['Model']}\n" +
                    f"Equipment Qr Code: {data['EquipmentQrCode']}\n" +
                    f"Under Warranty: {data['UnderWarranty']}\n" +
                    f"Serial Number: {data['SerialNumber']}\n" +
                    f"Equipment Type: {data['EquipmentType']}\n" +
                    f"Equipment Serviced in last 30 days: {data['EquipmentServiced']}\n" +
                    f"Equipment Location: {data['EquipmentLocation']}\n\n" +

                    "Service Request Info:\n\n" +
                    f"Request Date: {data['RequestDate']}\n" + 
                    f"Access Date: {data['AccessDate']}\n" +
                    f"Equip Access Start: {data['EquipAccessStart']}\n" +
                    f"Equip Access End: {data['EquipAccessEnd']}\n" +
                    f"OT Approved: {data['OTApproved']}\n"
                    f"Problem Description: {data['ProblemDescription']}\n" +
                    f"Additional Notes: {data['AdditionalNotes']}\n" +
                    f"PO Required: {data['PORequired']}\n" +
                    f"ClientPO: {data['ClientPO']}\n"
            }
            ,
            "toRecipients": [
                {
                    "emailAddress": {
                        "address": email_address1
                    }
                },
                {
                    "emailAddress": {
                        "address": email_address2
                    }
                }
            ],
            "ccRecipients": []
        },
        "saveToSentItems": "false"
    }
    # import requests
    status = requests.post(f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail', 
                           headers=headers, json=json.loads(json.dumps(msg)))
    # response = requests.get(f'https://graph.microsoft.com/v1.0/users/admin@wearetheone.com', 
    #                        headers=headers)
    
    # return json.dumps(msg), status
    # return response.content
    return status.content

# print(asyncio.run(sendMessage({"hello": "world"})))

