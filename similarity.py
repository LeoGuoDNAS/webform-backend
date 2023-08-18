from difflib import SequenceMatcher

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def most_similar(target, address_objects):
    return max(address_objects, key=lambda address: similar(
        target, 
        address['clntste_addrss_shp_addrss_strt'] + " " + 
        address['clntste_addrss_shp_addrss_strt_2'] + " " +
        address['clntste_addrss_shp_addrss_strt_3'] + " " +
        address['clntste_addrss_shp_addrss_strt_4'] + " " +
        address['clntste_addrss_shp_addrss_cty'] + " " +
        address['clntste_addrss_shp_addrss_stte'] + " " +
        address['clntste_addrss_shp_addrss_zp']
    ))
