import requests
from dotenv import load_dotenv
import os
import json
from models import FormModel
from io import BytesIO
from typing import List, Optional
from fastapi import UploadFile
import copy
from datetime import datetime

load_dotenv()
username = os.getenv('strapi_username')
password = os.getenv('strapi_password')

async def getAuthToken():
    data = {
        "identifier": username,
        "password": password
    }
    response = requests.post("https://api.daynitetools.com/api/auth/local", json=data)
    return response.json()

async def ticketSubmission(authToken: str, submittedData: dict):
    # return authToken['jwt']
    headers = {
        'Authorization': f'Bearer {authToken}',
        # 'Content-Type': 'multipart/form-data'
    }
    # data = submittedData.json()
    formData = {}
    
    images: List[UploadFile] = []
    if ('Images' in submittedData and submittedData['Images']):
        for image in submittedData['Images']:
            images.append(image)
        # formData['files.EquipmentImage'] = [(f.filename, f) for f in images]
    # if 'Images' in submittedData:
        del submittedData['Images']

    # formData['data'] = submittedData

    # For testing purposes
    # Use only Test1 Site Name or Test2
    # TODO: pay close attention to ENUM conversion to Bool

    date_str = "2023-08-25"
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    timestamp = int(date_obj.timestamp())

    formattedData = {"data": ""}
    formattedData['RequestDate'] = int(datetime.strptime(submittedData['Preferred_Date'], "%Y-%m-%d").timestamp())
    # formattedData['RequestDate'] = submittedData['Preferred_Date']
    formattedData['AdditionalNotes'] = submittedData['Comments']
    # formattedData['ClientPO'] = submittedData['Purchase_Order_Number']
    formattedData['EquipmentName'] = "TEST 11 18 2022 0234PM" # TODO
    formattedData['EquipmentID'] = "TEST 11 18 2022 0234PM" # TODO
    formattedData['EquipmentRN'] = "279276402"# TODO
    formattedData['SiteID'] = "216742"# TODO
    formattedData['SiteRN'] = "220782573"# TODO
    formattedData['EquipmentServiced'] = True if submittedData['Recently_Serviced'] == "Yes" else False
    formattedData['EquipmentLocation'] = submittedData['Location']
    # formattedData['Make'] = submittedData['Manufacturer']
    # formattedData['Model'] = submittedData['Model']
    # formattedData['EquipmentType'] = submittedData['Type']
    formattedData['POCName'] = submittedData['First_Name'] + " " + submittedData['Last_Name']
    formattedData['POCEmail'] = submittedData['Email_Address']
    formattedData['POCPhoneNumber'] = submittedData['Phone_Number']
    # formattedData['POCPhoneNumberExt'] = submittedData['Phone_Number_Ext']
    # formattedData['POCPhoneTwo'] = submittedData['Alternative_Phone_Number']
    # formattedData['POCPhoneTwoExt'] = submittedData['Alternative_Phone_Number_Ext']
    formattedData['ProblemDescription'] = submittedData['Description']
    formattedData['PORequired'] = True if submittedData['Require_PO_number'] == 'Yes' else False
    formattedData['EquipAccessStart'] = "11:11:00.000" # TODO
    formattedData['EquipAccessEnd'] = "11:11:00.000"# TODO
    formattedData['EquipmentQrCode'] = "n/a"
    # formattedData['UnderWarranty'] = "Yes" if submittedData['Under_Manufacturer_Warranty'] == "Yes" else "No"
    # formattedData['SerialNumber'] = ""# TODO
    # formattedData['StreetOne'] = submittedData['Street_1']
    # formattedData['StreetTwo'] = submittedData['Street_2']
    # formattedData['StreetThree'] = submittedData['Street_3']
    # formattedData['StreetFour'] = submittedData['Street_4']
    # formattedData['City'] = submittedData['City']
    # formattedData['State'] = submittedData['State']
    # formattedData['Zip'] = submittedData['Zip']
    # formattedData['OTApproved'] = "Yes" if submittedData['OT_Approved'] == "Yes" else "No"
    # formattedData['PossibleSites'] = ""# TODO

    formData['data'] = json.dumps(formattedData)
    # formData['data'] = formattedData
    # return formData
    file_contents = [(f.filename, await f.read(), f.content_type) for f in images]
    for f in images:
        await f.close()

    response = requests.post("https://api.daynitetools.com/api/results", 
                             data=formData,
                            #  files={"EquipmentImage" : [(filename, content, "image/jpeg") for filename, content, type in file_contents]},
                            #  files=[("EquipmentImage", f) for f in images], 
                             files=[("files.EquipmentImage", (filename, content, "image/jpeg")) for filename, content, type in file_contents],
                            #  files=[("files.EquipmentImage", content) for content in file_contents],
                             headers=headers)
    return response.json(), formData
    # return formData
# def fetch_image_from_uri(url: URL):
#     response = requests.get(url.url)
#     response.raise_for_status()
#     image_data = BytesIO(response.content)
#     return image_data

async def imageUpload(images: Optional[List[UploadFile]]):
    return {"yes"}