import asyncio
import json
import requests
from auth import acquire_access_token_without_user

email_address1 = 'it@wearetheone.com'
email_address2 = 'allservice@wearetheone.com'
user_id = '36d8ede0-773f-46b2-835d-c3988e9a39fe' # it

async def sendMessage(data: dict):
    access_token = await acquire_access_token_without_user()
    headers = {'Authorization': 'Bearer ' + access_token,
               'Content-Type' : 'application/json'}
    
    msg = {
        "message": {
            "subject": "[New Service Request] from non-contract customer webform",
            "body": {
                "contentType": "Text",
                "content": "Hello Day & Nite Team,\n\n" + 
                    "There's a new service request from the non-contract customer webform.\n" +
                    "Here are the details:\n\n" +
                    
                    "Site Info:\n" +
                    f"- Business Name: {data['BusinessName']}\n" +
                    f"- Site ID: {data['SiteID']}\n" +
                    f"- Street 1: {data['StreetOne']}\n" +
                    f"- Street 2: {data['StreetTwo']}\n" +
                    f"- Street 3: {data['StreetThree']}\n" +
                    f"- Street 4: {data['StreetFour']}\n" +
                    f"- City: {data['City']}\n" +
                    f"- State: {data['State']}\n" +
                    f"- Zip: {data['Zip']}\n\n"

                    "Contact Info:\n" +
                    f"- POC Name: {data['POCName']}\n" +
                    f"- POC Email: {data['POCEmail']}\n" +
                    f"- POC Phone Number: {data['POCPhoneNumber']}\n" +
                    f"- POC Phone Number Ext: {data['POCPhoneNumberExt']}\n" +
                    f"- POC Phone Two: {data['POCPhoneTwo']}\n" +
                    f"- POC Phone Two Ext: {data['POCPhoneTwoExt']}\n\n" +

                    "Service Request Info:\n" +
                    f"- Problem Description: {data['ProblemDescription']}\n" +
                    f"- Additional Notes: {data['AdditionalNotes']}\n" +
                    f"- PO Required: {data['PORequired']}\n" +
                    f"- ClientPO: {data['ClientPO']}\n" +
                    f"- Request Date: {data['RequestDate']}\n" + 
                    f"- Access Date: {data['AccessDate']}\n" +
                    f"- Equipment Access Start Time: {data['EquipAccessStart']}\n" +
                    f"- Equipment Access End Time: {data['EquipAccessEnd']}\n" +
                    f"- OT Approved: {data['OTApproved']}\n\n"
                    
                    # f"Zip: {data['Zip']}\n" +
                    # f"Possible Sites: {data['PossibleSites']}\n\n"

                    "Equipment Info:\n" +
                    f"- Make: {data['Make']}\n" +
                    f"- Model: {data['Model']}\n" +
                    # f"- Equipment Qr Code: {data['EquipmentQrCode']}\n" +
                    f"- Under Warranty: {data['UnderWarranty']}\n" +
                    f"- Serial Number: {data['SerialNumber']}\n" +
                    f"- Equipment Name: {data['EquipmentName']}\n" +
                    f"- Equipment ID: {data['EquipmentID']}\n" +
                    # f"Equipment Type: {data['EquipmentType']}\n" +
                    f"- Equipment Serviced in last 30 days: {data['EquipmentServiced']}\n" +
                    f"- Equipment Location (in their property): {data['EquipmentLocation']}\n\n" +

                    "Best Regards,\n" + 
                    "Day & Nite Information Technology\n\n" +
                    "**NO REPLIES: This is an automated message sent by the non-contract customer webform, reach out to lguo@wearetheone.com or achowdhury@wearetheone.com to learn more.**"
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
                },
                # {
                #     "emailAddress": {
                #         "address": email_address3
                #     }
                # }
            ],
            "ccRecipients": []
        }, 
        "saveToSentItems": "false"
    }
    # import requests
    res = requests.post(f'https://graph.microsoft.com/v1.0/users/{user_id}/sendMail', 
                           headers=headers, json=json.loads(json.dumps(msg)))
    # response = requests.get(f'https://graph.microsoft.com/v1.0/users/admin@wearetheone.com', 
    #                        headers=headers)
    
    # return json.dumps(msg), status
    # return response.content
    return res

# print(asyncio.run(sendMessage({"hello": "world"})))

