from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks, File, UploadFile, Depends
from fastapi.responses import JSONResponse, StreamingResponse
# from dotenv import load_dotenv
import io
from mangum import Mangum
from samproAPIs import clientAddressByZip
# load_dotenv()
# client_state = os.getenv('sampro_api_key')
from models import create_form_model, Address
# from models import FormModel
from fastapi.middleware.cors import CORSMiddleware
from similarity import most_similar
from strapiAPIs import getAuthToken, ticketSubmission
from io import BytesIO
from typing import List, Optional
from pydantic import ValidationError
from geocoding import address_validation, get_lat_lng
import json

app = FastAPI()
handler = Mangum(app)

origins = [
    "*"
    # "http://localhost:3000",
    # "https://leoguodnas.github.io"
]

# data = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
async def root():
    return {
        "Hello": "mundo", 
        "Go to": "/docs for api documentation"
    }

@app.get("/api/v1/clientAddressByZip/{zip}")
async def client_address_by_zip(zip: int):
    data = await clientAddressByZip(zip)
    return data

@app.post("/api/v1/submit")
async def formSubmit(
        data: dict = Depends(create_form_model)
    ):
    authKey = (await getAuthToken())['jwt']
    # return await ticketSubmission(authKey, data)
    try:
        # msg = ""
        # global data
        # data = []
        if (data['Images']):
            msg = ""
            for image in data['Images']:
                msg += image.filename + " "
            objectReceivedMsg = {
                "Object received" : json.dumps({k: v for k, v in data.items() if k != 'Images'}), 
                "Images received" : f"Uploaded {len(data['Images'])} images! Here are the file names: {msg}"
            }
        else:
            objectReceivedMsg = {
                "Object received" : json.dumps({k: v for k, v in data.items() if k != 'Images'}), 
                "Images received" : "None"
            }
        submissionMsg, formData = await ticketSubmission(authKey, data)
        
        # return objectReceivedMsg
        return {
            "Image Receive Msg": objectReceivedMsg,
            "Submission Msg": submissionMsg,
            "Formatted FormData": formData
        }
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    # return data

@app.post("/api/v1/validateAddress")
async def validateAddress(address: Address):
    response = address_validation(addressLine=address.addressLine, 
                       city=address.city,
                       state=address.state,
                       zip=address.zip)
    return response
    
@app.post("/api/v1/latlng")
async def geocde(address: Address):
    response = get_lat_lng(addressLine=address.addressLine,
                           city=address.city,
                           state=address.state,
                           zip=address.zip)
    return response
# @app.get("/api/v1/image/")
# async def image():
#     global data
#     return StreamingResponse(io.BytesIO(data[0]), media_type="image/jpeg")

# @app.post("/api/v1/imageUpload")
# async def uploadImage(Images: Optional[List[UploadFile]]):
#     msg = ""
#     global data
#     data = []
#     if (Images):
#         for image in Images:
#             msg += image.filename + " "
#             data.append(await image.read())
#     return f"Uploaded {len(Images)} images! Here are the file names: {msg}"

