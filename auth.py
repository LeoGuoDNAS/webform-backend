from msal import ConfidentialClientApplication
from fastapi import HTTPException
from urllib.parse import urlencode
from dotenv import load_dotenv
import os

load_dotenv()

tenant_id_azure = os.getenv('tenant_id_azure')
client_id_azure = os.getenv('client_id_azure')
client_secret_azure = os.getenv('client_secret_azure')

# Define the required parameters
authority = f'https://login.microsoftonline.com/{tenant_id_azure}'
scope = ["https://graph.microsoft.com/.default"]

app = ConfidentialClientApplication(client_id_azure, authority=authority, client_credential=client_secret_azure)

async def acquire_access_token_without_user():
    result = None
    try:
        result = app.acquire_token_for_client(scopes=scope)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to acquire access token")

    if "access_token" in result:
        access_token = result['access_token']
        return access_token
    else:
        raise HTTPException(status_code=500, detail="Access token not found")

