import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()
sampro_api_key = os.getenv('sampro_api_key')

async def clientAddressByZip(zip: int):
    headers = {
        'Authorization': f'api_key {sampro_api_key}',
        'Content-Type': 'application/json'    
    }

    data = {
        'tokenList': [['@zip@', zip, zip, 'variable']],
        'queryName': 'ClientSiteAddressByZip'
    }

    response = requests.post(
        'https://sampro.wearetheone.com/DBAnalytics/SAMProAPI.svc/postKPIData', 
        headers=headers, 
        json=data
    )
    text = response.text
    if text.startswith('"') and text.endswith('"'):
        text = text[1:-1]

    text = text.replace('\\"', '"')

    data = json.loads(text)
    return data