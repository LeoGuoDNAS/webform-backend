from pydantic import BaseModel
from typing import Optional
from enum import Enum

class YesOrNo(Enum):
    EMPTY = "-"
    YES = "Yes"
    NO = "No"

class EquipmentType(Enum):
    REFRIGERATION = "Refrigeration"
    HVAC = "HVAC"
    KITCHEN = "Kitchen"
    PLUMBING = "Plumbing"

class PreferredTime(Enum):
    TIME_6_9 = "6-9"
    TIME_9_12 = "9-12"
    TIME_12_2_30 = "12-2:30"

class FormData(BaseModel):
    Street_1: str
    Street_2: Optional[str] = ""
    Street_3: Optional[str] = ""
    Street_4: Optional[str] = ""
    City: str
    State: str
    Zip: str
    First_Name: str
    Last_Name: Optional[str] = ""
    Email_Address: str
    Phone_Number: int
    Phone_Number_Ext: Optional[str] = ""
    Alternative_Phone_Number: Optional[str] = ""
    Alternative_Phone_Number_Ext: Optional[str] = ""
    Manufacturer: Optional[str] = ""
    Model: Optional[str] = ""
    Under_Manufacturer_Warranty: YesOrNo
    Recently_Serviced: YesOrNo
    Service_Info: Optional[str] = ""
    Require_PO_number: YesOrNo
    Purchase_Order_Number: Optional[str] = ""
    Location: str
    Type: EquipmentType
    Description: str
    Preferred_Date: str
    Preferred_Time: PreferredTime
    OT_Approved: YesOrNo
    Comments: Optional[str] = ""