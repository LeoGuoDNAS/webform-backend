import requests
from dotenv import load_dotenv
import os
import json
from models import FormModel
from io import BytesIO
from typing import List, Optional
from fastapi import UploadFile

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

async def ticketSubmission(authToken: str, formData: FormModel):
    headers = {
        f"Bearer {authToken}"
    }
    data = formData.json()
    # formData.json()

    response = requests.post("https://api.daynitetools.com/api/results", json=data, headers=headers)
    return response.json()

# def fetch_image_from_uri(url: URL):
#     response = requests.get(url.url)
#     response.raise_for_status()
#     image_data = BytesIO(response.content)
#     return image_data

async def imageUpload(images: Optional[List[UploadFile]]):
    return {"yes"}