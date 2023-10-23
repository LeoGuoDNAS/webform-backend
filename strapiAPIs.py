import requests
import re
from dotenv import load_dotenv
import os
import json
from models import FormModel, SiteInfo
from samproAPIs import clientAddressByZip, clientAddressByZipUnique
from io import BytesIO
from typing import List, Optional
from fastapi import UploadFile
import copy
from datetime import datetime
from geocoding import get_lat_lng, address_validation, haversine_distance, matchSiteToClientAddress, siteMatchingViaLatLng, haversine_distance
from auth import acquire_access_token_without_user
from emails import sendMessage
from difflib import SequenceMatcher
from Levenshtein import distance

similarity_threshold = 0.8

load_dotenv()
username = os.getenv('strapi_username')
password = os.getenv('strapi_password')

def getIntFromStr(input: str):
    return int(re.sub("[^0-9]", "", input))

def getDomainFromEmail(input: str):
    domain_part = input.split('@')
    if len(domain_part) == 2:
        return domain_part[1].split('.')[0]
    else:
        return ""

async def getAuthToken():
    data = {
        "identifier": username,
        "password": password
    }
    response = requests.post("https://api.daynitetools.com/api/auth/local", json=data)
    return response.json()

async def getSiteInfo(info: SiteInfo):
    # Gets site address info from Sampro DB using name, address, phone and email
    # Scoring system
    sitesByZip = await clientAddressByZipUnique(info.zip)
    sitesByZipNameEmailPhone = []
    sitesByZipNameEmailPhoneDist = []
    possibleSites = []
    possibleSitesDist = []
    formLat, formLng = get_lat_lng(
        addressLine=[info.street1], 
        city=info.city, 
        state=info.state,
        zip=info.zip
    )

    highestScore = 0

    # print(type(sitesByZip))

    for site in sitesByZip:
        score = 0
        #  filter by phone
        # if getIntFromStr(site['clntste_cntct1_cntct_phne']) == getIntFromStr(info.phone) or getIntFromStr(site['clntste_cntct2_cntct_phne']) == getIntFromStr(info.phone) or getIntFromStr(site['clntste_phne_vce']) == getIntFromStr(info.phone):
        if getIntFromStr(site['clntste_cntct1_cntct_phne']) in [getIntFromStr(phone) for phone in info.phoneNumbers] or getIntFromStr(site['clntste_cntct2_cntct_phne']) in [getIntFromStr(phone) for phone in info.phoneNumbers] or getIntFromStr(site['clntste_phne_vce']) in [getIntFromStr(phone) for phone in info.phoneNumbers]:
        
            score += 20
        
        # filter by email
        # if getDomainFromEmail(site['clntste_cntct1_cntct_eml']).strip().lower() == getDomainFromEmail(info.email.strip().lower()) or getDomainFromEmail(site['clntste_cntct2_cntct_eml']).strip().lower() == getDomainFromEmail(info.email.strip().lower()):
        if getDomainFromEmail(site['clntste_cntct1_cntct_eml']).strip().lower() in [getDomainFromEmail(email) for email in info.emails] or getDomainFromEmail(site['clntste_cntct2_cntct_eml']).strip().lower() in [getDomainFromEmail(email) for email in info.emails]:
            score += 20
        else:
            email_list = site['clntste_eml'].split(';')
            for email in email_list:
                # if getDomainFromEmail(email).strip().lower() == getDomainFromEmail(info.email.strip().lower()):
                if getDomainFromEmail(email).strip().lower() in [getDomainFromEmail(email) for email in info.emails]:
                    score += 20
        
        # filter by name
        if info.businessName.strip().lower() in site['clntste_nme'].strip().lower() or site['clntste_nme'].strip().lower() in info.businessName.strip().lower():
            score += 20

        levenshteinDistance = distance(site['clntste_nme'].strip().lower(), info.businessName.strip().lower())

        # ratio = SequenceMatcher(None, info.businessName.strip().lower(), site['clntste_name'].strip().lower()).ratio()
        # if ratio >= similarity_threshold:
        #     score += ratio * 20

        if score > highestScore:
            highestScore = score
        
        if score >= 20:
            sitesByZipNameEmailPhone.append(site)
        else:
            if levenshteinDistance <= 5:
                possibleSites.append(site)

    for site in possibleSites:
        siteLat, siteLng = get_lat_lng(
            addressLine=[site['clntste_addrss_shp_addrss_strt']], 
            city=site['clntste_addrss_shp_addrss_cty'], 
            state=site['clntste_addrss_shp_addrss_stte'],
            zip=site['clntste_addrss_shp_addrss_zp']
        )
        if siteLat != None and siteLng != None:
            dist = haversine_distance([formLat, formLng], [siteLat, siteLng])
            if dist < 0.1:
                # possibleSitesDist.append(site)
                sitesByZipNameEmailPhoneDist.append(site)

    # Filter by address (distance)
    for site in sitesByZipNameEmailPhone:
        siteLat, siteLng = get_lat_lng(
            addressLine=[site['clntste_addrss_shp_addrss_strt']], 
            city=site['clntste_addrss_shp_addrss_cty'], 
            state=site['clntste_addrss_shp_addrss_stte'],
            zip=site['clntste_addrss_shp_addrss_zp']
        )
        if siteLat != None and siteLng != None:
            dist = haversine_distance([formLat, formLng], [siteLat, siteLng])

            # if dist < 0.5:
                # distance is less than 500meters
                # sitesByZipNameEmailPhoneDist.append(site)
            if dist < 0.1:
                # distance is less than 100meters
                # return [site, site]
                # return []
                sitesByZipNameEmailPhoneDist.append(site)
            # if dist <= 0.1:
            #     sitesByZipNameEmailPhoneDist.append(site)

    # return sitesByZipNameEmailPhoneDist, possibleSitesDist
    return sitesByZipNameEmailPhoneDist

# async def getPossibleSites(info: SiteInfo):
#     sitesByZip = await clientAddressByZipUnique(info.zip)
#     sitesByZipNameEmailPhone = []
#     sitesByZipNameEmailPhoneDist = []
#     formLat, formLng = get_lat_lng(
#         addressLine=[info.street1], 
#         city=info.city, 
#         state=info.state,
#         zip=info.zip
#     )

#     highestScore = 0

#     for site in sitesByZip:
#         score = 0
#         if getIntFromStr(site['clntste_cntct1_cntct_phne']) in [getIntFromStr(phone) for phone in info.phoneNumbers] or getIntFromStr(site['clntste_cntct2_cntct_phne']) in [getIntFromStr(phone) for phone in info.phoneNumbers] or getIntFromStr(site['clntste_phne_vce']) in [getIntFromStr(phone) for phone in info.phoneNumbers]:
#             score += 20
#         if getDomainFromEmail(site['clntste_cntct1_cntct_eml']).strip().lower() in [getDomainFromEmail(email) for email in info.emails] or getDomainFromEmail(site['clntste_cntct2_cntct_eml']).strip().lower() in [getDomainFromEmail(email) for email in info.emails]:
#             score += 20
#         else:
#             email_list = site['clntste_eml'].split(';')
#             for email in email_list:
#                 if getDomainFromEmail(email).strip().lower() in [getDomainFromEmail(email) for email in info.emails]:
#                     score += 20

#         levenshteinDistance = distance(site['clntste_nme'].strip().lower(), info.businessName.strip().lower())
#         # if info.businessName.strip().lower() in site['clntste_nme'].strip().lower() or site['clntste_nme'].strip().lower() in info.businessName.strip().lower():
#         #     score += 20
#         score += 0 if levenshteinDistance >= 5 else 20 - levenshteinDistance
#         if score > highestScore:
#             highestScore = score
#         if score >= 20:
#             sitesByZipNameEmailPhone.append(site)

#     for site in sitesByZipNameEmailPhone:
#         siteLat, siteLng = get_lat_lng(
#             addressLine=[site['clntste_addrss_shp_addrss_strt']], 
#             city=site['clntste_addrss_shp_addrss_cty'], 
#             state=site['clntste_addrss_shp_addrss_stte'],
#             zip=site['clntste_addrss_shp_addrss_zp']
#         )
#         if siteLat != None and siteLng != None:
#             dist = haversine_distance([formLat, formLng], [siteLat, siteLng])
#             if dist < 0.1:
#                 sitesByZipNameEmailPhoneDist.append(site)
#     return sitesByZipNameEmailPhoneDist

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

    # date_str = "2023-08-25"
    # date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    # timestamp = int(date_obj.timestamp())

    # equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites = await matchSiteToClientAddress(submittedData)
    
    
    formattedData = {}
    
    ## TODO: THIS IS what I used for Strapi
    # formattedData['RequestDate'] = submittedData['Preferred_Date']
    # formattedData['AccessDate'] = submittedData['Preferred_Date']
    # formattedData['AdditionalNotes'] = submittedData['Comments']
    # formattedData['ClientPO'] = submittedData['Purchase_Order_Number']
    # # formattedData['EquipmentName'] = "TEST 11 18 2022 0234PM" # TODO
    # # formattedData['EquipmentID'] = "TEST 11 18 2022 0234PM" # TODO
    # # formattedData['EquipmentRN'] = "279276402"# TODO
    # # formattedData['SiteID'] = "216742"# TODO
    # # formattedData['SiteRN'] = "220782573"# TODO
    # formattedData['EquipmentName'] = str(equipmentName)
    # formattedData['EquipmentID'] = str(equipmentId)
    # formattedData['EquipmentRN'] = str(equipmentRn)
    # formattedData['SiteID'] = str(siteId)
    # formattedData['SiteRN'] = str(siteRn)
    # formattedData['EquipmentServiced'] = True if submittedData['Recently_Serviced'] == "Yes" else False
    # formattedData['EquipmentLocation'] = submittedData['Location']
    # formattedData['Make'] = submittedData['Manufacturer']
    # formattedData['Model'] = submittedData['Model']
    # formattedData['EquipmentType'] = submittedData['Type']
    # formattedData['POCName'] = submittedData['First_Name'] + " " + submittedData['Last_Name']
    # formattedData['POCEmail'] = submittedData['Email_Address']
    # formattedData['POCPhoneNumber'] = submittedData['Phone_Number']
    # formattedData['POCPhoneNumberExt'] = submittedData['Phone_Number_Ext']
    # formattedData['POCPhoneTwo'] = submittedData['Alternative_Phone_Number']
    # formattedData['POCPhoneTwoExt'] = submittedData['Alternative_Phone_Number_Ext']
    # formattedData['ProblemDescription'] = submittedData['Description']
    # formattedData['PORequired'] = True if submittedData['Require_PO_number'] == 'Yes' else False
    # formattedData['EquipAccessStart'] = submittedData['Preferred_Start_Time'] + ":00.000" # TODO
    # formattedData['EquipAccessEnd'] = submittedData['Preferred_End_Time'] + ":00.000" # TODO
    # formattedData['EquipmentQrCode'] = "n/a"
    # formattedData['UnderWarranty'] = True if submittedData['Under_Manufacturer_Warranty'] == "Yes" else False
    # formattedData['SerialNumber'] = ""# TODO: add input
    # formattedData['StreetOne'] = submittedData['Street_1']
    # formattedData['StreetTwo'] = submittedData['Street_2']
    # formattedData['StreetThree'] = submittedData['Street_3']
    # formattedData['StreetFour'] = submittedData['Street_4']
    # formattedData['City'] = submittedData['City']
    # formattedData['State'] = submittedData['State']
    # formattedData['Zip'] = submittedData['Zip']
    # formattedData['OTApproved'] = True if submittedData['OT_Approved'] == "Yes" else False
    # formattedData['PossibleSites'] = possibleSites# TODO



    formattedData['RequestDate'] = submittedData['Preferred_Date']
    formattedData['AccessDate'] = submittedData['Preferred_Date']
    formattedData['AdditionalNotes'] = submittedData['Comments']
    formattedData['ClientPO'] = submittedData['Purchase_Order_Number']
    # formattedData['EquipmentName'] = equipmentName
    # formattedData['EquipmentID'] = equipmentId
    # formattedData['EquipmentRN'] = equipmentRn
    # formattedData['SiteID'] = siteId
    # formattedData['SiteRN'] = siteRn
    formattedData['EquipmentName'] = submittedData['Equipment_Name']
    formattedData['EquipmentID'] = submittedData['Equipment_ID']
    formattedData['EquipmentRN'] = submittedData['Equipment_RN']
    formattedData['SiteID'] = submittedData['Site_ID']
    formattedData['SiteRN'] = submittedData['Site_RN']
    # formattedData['PossibleSites'] = submittedData['Possible_Sites']

    formattedData['EquipmentServiced'] = submittedData['Recently_Serviced']
    formattedData['EquipmentLocation'] = submittedData['Location']
    formattedData['Make'] = submittedData['Manufacturer']
    formattedData['Model'] = submittedData['Model']
    # formattedData['EquipmentType'] = submittedData['Type']
    # formattedData['EquipmentRN'] = submittedData['Equipment_RN']
    formattedData['POCName'] = submittedData['First_Name'] + " " + submittedData['Last_Name']
    formattedData['POCEmail'] = submittedData['Email_Address']
    formattedData['POCPhoneNumber'] = submittedData['Phone_Number']
    formattedData['POCPhoneNumberExt'] = submittedData['Phone_Number_Ext']
    formattedData['POCPhoneTwo'] = submittedData['Alternative_Phone_Number']
    formattedData['POCPhoneTwoExt'] = submittedData['Alternative_Phone_Number_Ext']
    formattedData['ProblemDescription'] = submittedData['Description']
    formattedData['PORequired'] = submittedData['Require_PO_number']
    formattedData['EquipAccessStart'] = submittedData['Preferred_Start_Time'] + ":00.000" # TODO
    formattedData['EquipAccessEnd'] = submittedData['Preferred_End_Time'] + ":00.000" # TODO
    formattedData['EquipmentQrCode'] = "n/a"
    formattedData['UnderWarranty'] = submittedData['Under_Manufacturer_Warranty']
    formattedData['SerialNumber'] = ""# TODO: add input
    formattedData['StreetOne'] = submittedData['Street_1']
    formattedData['StreetTwo'] = submittedData['Street_2']
    formattedData['StreetThree'] = submittedData['Street_3']
    formattedData['StreetFour'] = submittedData['Street_4']
    formattedData['City'] = submittedData['City']
    formattedData['State'] = submittedData['State']
    formattedData['Zip'] = submittedData['Zip']
    formattedData['OTApproved'] = submittedData['OT_Approved']
    # formattedData['PossibleSites'] = possibleSites# TODO

    responseContent = await sendMessage(formattedData)

    # formData['data'] = json.dumps(formattedData)

    # check if there is match
    # if equipmentName != "" and equipmentId != "" and equipmentRn != "" and siteId != "" and siteRn != "":
    #     # TODO: for images, not in use for now
    #     # file_contents = [(f.filename, await f.read(), f.content_type) for f in images]
    #     # for f in images:
    #     #     await f.close()
    #     # TODO: use strapi API
    #     # if len(file_contents) != 0:
    #     #     response = requests.post("https://api.daynitetools.com/api/results", 
    #     #                             data={"data": json.dumps(formattedData)},
    #     #                             files=[("files.EquipmentImage", file) for file in file_contents],
    #     #                             headers=headers)
    #     # else:
    #     #     response = requests.post("https://api.daynitetools.com/api/results", 
    #     #                             json={"data": formattedData},
    #     #                             headers=headers
    #     #     )
        
    response = requests.post("https://sampro.wearetheone.com/FMMSService/WeblogAPI", 
                            json={
                                "caller": f"{submittedData['First_Name'] + ' ' + submittedData['Last_Name']} (Web Form)",
                                "phoneNumder": submittedData['Phone_Number'],
                                "siteId": submittedData['Site_ID'],
                                "street1": submittedData['Street_1'],
                                "street2": submittedData['Street_2'],
                                "city": submittedData['City'],
                                "state": submittedData['State'],
                                "zip": submittedData['Zip'],
                                "problemDescription": submittedData['Description'],
                                "notToExceed": "999999",
                                "siteRN": int(submittedData['Site_RN']),
                                "equipmentRN": int(submittedData['Equipment_RN']),
                                "workRequested": formattedData['ProblemDescription'] + ":Work requested (From Webform: Equipment Qr Code Number:"
                                                + " -- Equip Serviced in Last 30 Days:" + formattedData['EquipmentServiced']
                                                + " -- PO Required:" + formattedData['PORequired']
                                                + " -- Client PO:" + formattedData['ClientPO']
                                                + " -- Equip Access Start Time:" + formattedData['EquipAccessStart']
                                                + " -- Equip Access End Time:" + formattedData['EquipAccessEnd']
                                                + " -- Equip Access Date:" + formattedData['AccessDate']
                                                + " -- Point of Contact Name:" + formattedData['POCName'] 
                                                + " -- POC Email:" + formattedData['POCEmail'] 
                                                + " -- Diagnosis Images:"
                                                + " -- Poc Phone:" + formattedData['POCPhoneNumber']
                                                + " -- Poc Phone Ext:" + formattedData['POCPhoneNumberExt']
                                                + " -- Poc Phone Two:" + formattedData['POCPhoneTwo']
                                                + " -- Poc Phone Two Ext:" + formattedData['POCPhoneTwoExt']
                                                + " -- Street 1:" + formattedData['StreetOne']
                                                + " -- Street 2:" + formattedData['StreetTwo']
                                                + " -- Street 3:" + formattedData['StreetThree']
                                                + " -- Street 4:" + formattedData['StreetFour']
                                                + " -- City:" + formattedData['City']
                                                + " -- State:" + formattedData['State']
                                                + " -- Zip:" + formattedData['Zip']
                                                + " -- Additional Notes:" + formattedData['AdditionalNotes']
                                                + " -- ClientSite ID:" + formattedData['SiteID']
                                                + " -- EquipmentID:" + formattedData['EquipmentID']
                                                + " -- Under Warranty?:" + formattedData['UnderWarranty']
                                                + " -- Equipment Serial Number:" + formattedData['SerialNumber']
                                                + " -- Equipment Make:" + formattedData['Make']
                                                + " -- Equipment Model:" + formattedData['Model']
                                                + " -- EquipmentFloor#/location:" + formattedData['EquipmentLocation']
                                                + " -- Equipment Name:" + formattedData['EquipmentName']
                                                + " -- UserID:webform",
                                "requestDate": submittedData['Preferred_Date'],
                                "poNumber": submittedData['Purchase_Order_Number'],
                                "submittedBy": "Web form"
                            }
    )

    return {
        "WeblogAPI response": response.status_code,
        "SendEmail response": responseContent.status_code
    }, formattedData
    # else: # no match
    #     # send email to ...
    #     responseContent = await sendMessage(formattedData)

    #     # send to weblog with Unknown siteID and siteRn
    #     # TODO: Unknown siteID and siteRn
        
    #     # response = requests.post("https://sampro.wearetheone.com/FMMSService/WeblogAPI", 
    #     #                         json={
    #     #                             "caller": f"{submittedData['First_Name'] + ' ' + submittedData['Last_Name']} (Web Form)",
    #     #                             "phoneNumder": submittedData['Phone_Number'],
    #     #                             "siteId": str(siteId),
    #     #                             "street1": submittedData['Street_1'],
    #     #                             "street2": submittedData['Street_2'],
    #     #                             "city": submittedData['City'],
    #     #                             "state": submittedData['State'],
    #     #                             "zip": submittedData['Zip'],
    #     #                             "problemDescription": submittedData['Description'],
    #     #                             "notToExceed": "999999",
    #     #                             "siteRN": int(siteRn),
    #     #                             "equipmentRN": int(equipmentRn),
    #     #                             "workRequested": formattedData['ProblemDescription'] + ":Work requested (From Webform: Equipment Qr Code Number:"
    #     #                                             + " -- Equip Serviced in Last 30 Days:" + formattedData['EquipmentServiced']
    #     #                                             + " -- PO Required:" + formattedData['PORequired']
    #     #                                             + " -- Client PO:" + formattedData['ClientPO']
    #     #                                             + " -- Equip Access Start Time:" + formattedData['EquipAccessStart']
    #     #                                             + " -- Equip Access End Time:" + formattedData['EquipAccessEnd']
    #     #                                             + " -- Equip Access Date:" + formattedData['AccessDate']
    #     #                                             + " -- Point of Contact Name:" + formattedData['POCName'] 
    #     #                                             + " -- POC Email:" + formattedData['POCEmail'] 
    #     #                                             + " -- Diagnosis Images:"
    #     #                                             + " -- Poc Phone:" + formattedData['POCPhoneNumber']
    #     #                                             + " -- Poc Phone Ext:" + formattedData['POCPhoneNumberExt']
    #     #                                             + " -- Poc Phone Two:" + formattedData['POCPhoneTwo']
    #     #                                             + " -- Poc Phone Two Ext:" + formattedData['POCPhoneTwoExt']
    #     #                                             + " -- Street 1:" + formattedData['StreetOne']
    #     #                                             + " -- Street 2:" + formattedData['StreetTwo']
    #     #                                             + " -- Street 3:" + formattedData['StreetThree']
    #     #                                             + " -- Street 4:" + formattedData['StreetFour']
    #     #                                             + " -- City:" + formattedData['City']
    #     #                                             + " -- State:" + formattedData['State']
    #     #                                             + " -- Zip:" + formattedData['Zip']
    #     #                                             + " -- Possible Sites:" + formattedData['PossibleSites']
    #     #                                             + " -- Additional Notes:" + formattedData['AdditionalNotes']
    #     #                                             + " -- ClientSite ID:" + formattedData['SiteID']
    #     #                                             + " -- EquipmentID:" + formattedData['EquipmentID']
    #     #                                             + " -- Under Warranty?:" + formattedData['UnderWarranty']
    #     #                                             + " -- Equipment Type:" + formattedData['EquipmentType']
    #     #                                             + " -- Equipment Serial Number:" + formattedData['SerialNumber']
    #     #                                             + " -- Equipment Make:" + formattedData['Make']
    #     #                                             + " -- Equipment Model:" + formattedData['Model']
    #     #                                             + " -- EquipmentFloor#/location:" + formattedData['EquipmentLocation']
    #     #                                             + " -- Equipment Name:" + formattedData['EquipmentName']
    #     #                                             + " -- UserID:webform",
    #     #                             "requestDate": submittedData['Preferred_Date'],
    #     #                             "poNumber": submittedData['Purchase_Order_Number'],
    #     #                             "submittedBy": "Web form"
    #     #                         }
    #     # )

    #     return {"submitFailed-sentEmail": responseContent}, formattedData

    # for testing
    # return {"testing": "testing"}, formattedData
    