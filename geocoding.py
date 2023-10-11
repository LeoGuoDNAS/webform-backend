import requests
import os
from dotenv import load_dotenv
from typing import List
from math import radians, sin, cos, sqrt, atan2
from samproAPIs import clientAddressByZip
from models import kitchen, hvac, ref, plumb
import json

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
    
# returns haversine distance of two sets of coords in km
def haversine_distance(coord1, coord2):
    R = 6371  # Radius of Earth in kilometers

    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # if lat1 is None or lon1 is None or lat2 is None or lon2 is None:
    #     return None

    # Convert latitude and longitude from degrees to radians
    rLat1, rLon1, rLat2, rLon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dLat = rLat2 - rLat1
    dLon = rLon2 - rLon1

    a = sin(dLat / 2)**2 + cos(rLat1) * cos(rLat2) * sin(dLon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c  # Distance in kilometers
    return distance

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

def siteMatchingViaLatLng(
        formLat, 
        formLng, 
        site, 
        possibleSites,
        equipmentName, 
        equipmentId, 
        equipmentRn, 
        siteId, 
        siteRn,
        minDist
):
    # equipmentName, equipmentId, equipmentRn, siteId, siteRn = "", "", "", "", ""
    siteLat, siteLng = get_lat_lng(
        addressLine=[site['clntste_addrss_shp_addrss_strt']], 
        city=site['clntste_addrss_shp_addrss_cty'], 
        state=site['clntste_addrss_shp_addrss_stte'],
        zip=site['clntste_addrss_shp_addrss_zp']
    )
    if siteLat != None and siteLng != None:
        dist = haversine_distance([formLat, formLng], [siteLat, siteLng])

        if dist <= 5:
            # possibleSites.append([site['clntste_nme'], site['clntste_id']])
            possibleSites.append(site['clntste_id'])
            if dist <= 1 and dist < minDist:
                minDist = dist
                equipmentName = site['clntsteeqpmnt_nme']
                equipmentId = site['clntsteeqpmnt_id']
                equipmentRn = site['clntsteeqpmnt_rn']
                siteId = site['clntste_id']
                siteRn = site['clntste_rn']
    return equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites, minDist
    

async def matchSiteToClientAddress(submittedData: dict):
    sites = await clientAddressByZip(submittedData['Zip'])

    minDist = 100
    equipmentName, equipmentId, equipmentRn, siteId, siteRn = "", "", "", "", ""
    possibleSites = []
    # for site in sites:
    #     possibleSites.append([site['clntste_nme'], site['clntste_id']])

    # Filter by distance (<=1km)
    formLat, formLng = get_lat_lng(
        addressLine=[submittedData['Street_1']], 
        city=submittedData['City'], 
        state=submittedData['State'],
        zip=submittedData['Zip']
    )
    for site in sites:
        # is hvac
        if submittedData['Type'] == "HVAC" and site['clntsteeqpmnt_nme'] in hvac:
            equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites, minDist = siteMatchingViaLatLng(formLat, formLng, site, possibleSites, equipmentName, equipmentId, equipmentRn, siteId, siteRn, minDist)
    # if 
        elif submittedData['Type'] == "Refrigeration" and site['clntsteeqpmnt_nme'] in ref:
            equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites, minDist = siteMatchingViaLatLng(formLat, formLng, site, possibleSites, equipmentName, equipmentId, equipmentRn, siteId, siteRn, minDist)
            
        elif submittedData['Type'] == "Kitchen" and site['clntsteeqpmnt_nme'] in kitchen:
            equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites, minDist = siteMatchingViaLatLng(formLat, formLng, site, possibleSites, equipmentName, equipmentId, equipmentRn, siteId, siteRn, minDist)
            
        elif submittedData['Type'] == "Plumbing" and site['clntsteeqpmnt_nme'] in plumb:
            equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites, minDist = siteMatchingViaLatLng(formLat, formLng, site, possibleSites, equipmentName, equipmentId, equipmentRn, siteId, siteRn, minDist)
     
    return equipmentName, equipmentId, equipmentRn, siteId, siteRn, json.dumps(possibleSites)
    # return equipmentName, equipmentId, equipmentRn, siteId, siteRn, possibleSites