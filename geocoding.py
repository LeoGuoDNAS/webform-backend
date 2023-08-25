import requests
import os
from dotenv import load_dotenv
from typing import List

load_dotenv()
gcp_key = os.getenv('gcp_maps_key')

def address_validation(addressLine: List[str], city, state, zip):
    base_url = "https://addressvalidation.googleapis.com/v1:validateAddress"
    # gcp_key = os.getenv('gcp_maps_key')
    params = {
        "key": gcp_key
    }

    response = requests.post(base_url, params=params, json={
        "address": {
            "regionCode": "US",
            "locality": city,
            "administrativeArea": state,
            "postalCode": zip,
            "addressLines": addressLine
        }
    })
    return response.json()
    # if response.status_code == 200 and response.json()['status'] == 'OK':
    #     return "Address is valid"
    # else:
    #     return "Address is NOT valid"

# def get_lat_lng(address):
def get_lat_lng(addressLine: List[str], city, state, zip):
    """
    Return the latitude and longitude of a location using Google Geocoding API.
    """
    address = ""
    for line in addressLine:
        address += line + ", "
    address += city + ", "
    address += state + ", "
    address += zip
    
    base_url = "https://maps.googleapis.com/maps/api/geocode/json"
    params = {
        "address": address,
        "key": gcp_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200 and response.json()['status'] == 'OK':
        latitude = response.json()['results'][0]['geometry']['location']['lat']
        longitude = response.json()['results'][0]['geometry']['location']['lng']
        return latitude, longitude
    else:
        return None, None

# Example Usage
# API_KEY = gcp_key
# address_input = input("Enter an address: ")
# lat, lng = get_lat_lng(API_KEY, address_input)

# if lat and lng:
#     print(f"Latitude: {lat}, Longitude: {lng}")
# else:
#     print(f"Couldn't retrieve coordinates. {gcp_key}")

# street = input("Enter an street address: ")
# city = input("Enter an city: ")
# state = input("Enter an state: ")
# zip = input("Enter an zip: ")
# validation = address_validation(API_KEY, addressLine=[street], city=city, state=state, zip=zip)
# print(validation)