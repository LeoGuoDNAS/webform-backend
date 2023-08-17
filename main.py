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
    headers = {
        'Access-Control-Allow-Origin' : "http://localhost:3000"
    }
    return JSONResponse(content=data, headers=headers)
    
@app.post("/api/v1/submit")
async def client_address_by_zip(data: FormData):
    # data = await clientAddressByZip(zip)
    # headers = {
    #     'Access-Control-Allow-Origin' : "http://localhost:3000"
    # }
    # return JSONResponse(content=data, headers=headers)

    # headers = {
    #     'Access-Control-Allow-Origin' : "http://localhost:3000"
    # }
    # return JSONResponse(content=data, headers=headers)
    return data