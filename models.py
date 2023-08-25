from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from fastapi import File, UploadFile, Form, UploadFile
import os
from dotenv import load_dotenv
import json

load_dotenv()
username = os.getenv('strapi_username')

class Address(BaseModel):
    addressLine: List[str]
    city: str
    state: str
    zip: str

# class YesOrNo(Enum):
#     EMPTY = "-"
#     YES = "Yes"
#     NO = "No"

# class EquipmentType(Enum):
#     REFRIGERATION = "Refrigeration"
#     HVAC = "HVAC"
#     KITCHEN = "Kitchen"
#     PLUMBING = "Plumbing"

# class PreferredTime(Enum):
#     TIME_6_9 = "6-9"
#     TIME_9_12 = "9-12"
#     TIME_12_2_30 = "12-2:30"

# class EnumEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Enum):
#             return obj.value
#         return super().default(obj)

# class FormModel(BaseModel):
#     Street_1: str
#     Street_2: Optional[str] = ""
#     Street_3: Optional[str] = ""
#     Street_4: Optional[str] = ""
#     City: str
#     State: str
#     Zip: str
#     First_Name: str
#     Last_Name: Optional[str] = ""
#     Email_Address: str
#     Phone_Number: int
#     Phone_Number_Ext: Optional[str] = ""
#     Alternative_Phone_Number: Optional[str] = ""
#     Alternative_Phone_Number_Ext: Optional[str] = ""
#     Manufacturer: Optional[str] = ""
#     Model: Optional[str] = ""
#     Under_Manufacturer_Warranty: YesOrNo
#     Recently_Serviced: YesOrNo
#     Service_Info: Optional[str] = ""
#     Require_PO_number: YesOrNo
#     Purchase_Order_Number: Optional[str] = ""
#     Location: str
#     Type: EquipmentType
#     Description: str
#     Preferred_Date: str
#     Preferred_Time: PreferredTime
#     OT_Approved: YesOrNo
#     Comments: Optional[str] = ""
#     Images: Optional[List[UploadFile]] = None
class FormModel:
    POCName: str
    POCPhoneNumber: str
    SiteID: str
    ProblemDescription: str
    EquipmentRN: str
    SiteRN: str
    POCEmail: str
    RequestDate: str
    AdditionalNotes: str
    EquipmentName: str
    EquipmentServiced: bool
    PORequired: bool
    EquipAccessStart: str
    EquipmentQrCode: str
    EquipAccessEnd: str
    EquipmentID: str
    # createdAt: str
    # updatedAt: str
    # publishedAt: str
    EmergencyTicket: Optional[bool]
    EquipmentLocation: Optional[str]
    # WeblogID: Optional[str]
    ClientPO: Optional[str]
    # AccessDate: Optional[str]
    UnderWarranty: Optional[bool]
    SerialNumber: Optional[str]
    Make: Optional[str]
    Model: Optional[str]
    EquipmentType: Optional[str]
    # WorkorderId: Optional[str]
    # WorkorderRn: Optional[str]
    StreetOne: Optional[str]
    StreetTwo: Optional[str]
    StreetThree: Optional[str]
    StreetFour: Optional[str]
    City: Optional[str]
    State: Optional[str]
    Zip: Optional[str]
    POCPhoneTwo: Optional[str]
    POCPhoneTwoExt: Optional[str]
    OTApproved: Optional[bool]
    PossibleSites: Optional[str]
    POCPhoneNumberExt: Optional[str]

        



def create_form_model(
    Street_1: str = Form(...),
    Street_2: Optional[str] = Form(""),
    Street_3: Optional[str] = Form(""),
    Street_4: Optional[str] = Form(""),
    City: str = Form(...),
    State: str = Form(...),
    Zip: str = Form(...),
    First_Name: str = Form(...),
    Last_Name: Optional[str] = Form(""),
    Email_Address: str = Form(...),
    Phone_Number: str = Form(...),
    Phone_Number_Ext: Optional[str] = Form(""),
    Alternative_Phone_Number: Optional[str] = Form(""),
    Alternative_Phone_Number_Ext: Optional[str] = Form(""),
    Manufacturer: Optional[str] = Form(""),
    Model: Optional[str] = Form(""),
    Under_Manufacturer_Warranty: str = Form(...),
    Recently_Serviced: str = Form(...),
    Service_Info: Optional[str] = Form(""),
    Require_PO_number: str = Form(...),
    Purchase_Order_Number: Optional[str] = Form(""),
    Location: str = Form(...),
    Type: str = Form(...),
    Description: str = Form(...),
    Preferred_Date: str = Form(...),
    Preferred_Time: str = Form(...),
    OT_Approved: str = Form(...),
    Comments: Optional[str] = Form(""),
    Images: Optional[List[UploadFile]] = File(None)
    # Uncomment for images
    # Images: List[UploadFile] = File(...)
):
    return {
        "Street_1": Street_1,
        "Street_2": Street_2,
        "Street_3": Street_3,
        "Street_4": Street_4,
        "City": City,
        "State": State,
        "Zip": Zip,
        "First_Name": First_Name,
        "Last_Name": Last_Name,
        "Email_Address": Email_Address,
        "Phone_Number": Phone_Number,
        "Phone_Number_Ext": Phone_Number_Ext,
        "Alternative_Phone_Number": Alternative_Phone_Number,
        "Alternative_Phone_Number_Ext": Alternative_Phone_Number_Ext,
        "Manufacturer": Manufacturer,
        "Model": Model,
        "Under_Manufacturer_Warranty": Under_Manufacturer_Warranty,
        "Recently_Serviced": Recently_Serviced,
        "Service_Info": Service_Info,
        "Require_PO_number": Require_PO_number,
        "Purchase_Order_Number": Purchase_Order_Number,
        "Location": Location,
        "Type": Type,
        "Description": Description,
        "Preferred_Date": Preferred_Date,
        "Preferred_Time": Preferred_Time,
        "OT_Approved": OT_Approved,
        "Comments": Comments,
        "Images": Images
        # Uncomment for images
        # "Images": Images
    }
