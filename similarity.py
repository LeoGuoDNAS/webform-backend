from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def most_similar(target, address_objects):
    return max(address_objects, key=lambda address: similar(
        target, 
        address['clntste_addrss_shp_addrss_strt'].strip().lower() + " " + 
        address['clntste_addrss_shp_addrss_strt_2'].strip().lower() + " " +
        address['clntste_addrss_shp_addrss_strt_3'].strip().lower() + " " +
        address['clntste_addrss_shp_addrss_strt_4'].strip().lower() + " " +
        address['clntste_addrss_shp_addrss_cty'].strip().lower() + " " +
        address['clntste_addrss_shp_addrss_stte'].strip().lower() + " " +
        address['clntste_addrss_shp_addrss_zp'].strip().lower()
    ))
    # return address_objects
