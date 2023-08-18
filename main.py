from fastapi import FastAPI, HTTPException, Request, Response, BackgroundTasks
from fastapi.responses import JSONResponse
# from dotenv import load_dotenv
# import os
from mangum import Mangum
from samproAPIs import clientAddressByZip
# load_dotenv()
# client_state = os.getenv('sampro_api_key')
from models import FormData
from fastapi.middleware.cors import CORSMiddleware
from similarity import most_similar

app = FastAPI()
handler = Mangum(app)

origins = [
    "http://localhost:3000"
]

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
        "Hello": "mundo"
    }

@app.get("/api/v1/clientAddressByZip/{zip}")
async def client_address_by_zip(zip: int):
    data = await clientAddressByZip(zip)
    # headers = {
    #     'Access-Control-Allow-Origin' : "http://localhost:3000"
    # }
    # return JSONResponse(content=data, headers=headers)
    return data

@app.post("/api/v1/submit")
async def client_address_by_zip(data: FormData):
    zip = data.Zip
    addresses = await clientAddressByZip(zip=zip)
    input_address_str = (
        data.Street_1 + " " + 
        data.Street_2 + " " +
        data.Street_3 + " " +
        data.Street_4 + " " +
        data.City + " " +
        data.State + " " +
        data.Zip
    )

    return most_similar(input_address_str, addresses)