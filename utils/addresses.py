from geopy.geocoders import Nominatim
import uuid

def geolocator():
    return Nominatim(user_agent=f"kairy{uuid.uuid4()}")

center_memo = {}
def getCenter(country):
    if country in center_memo:
        return center_memo[country]
    location = geolocator().geocode(country)
    if location:
        center_memo[country] = (location.latitude, location.longitude) # type: ignore
        return center_memo[country]
    else:
        return None

name_memo = {}  
def getName(lat, lng):
    if (lat, lng) in name_memo:
        return name_memo[(lat, lng)]
    
    location = geolocator().reverse(f"{lat}, {lng}")
    name_memo[(lat, lng)] = location.address # type: ignore
    return name_memo[(lat, lng)]

lookfor_memo = {}
def lookFor(name):
    if name in lookfor_memo:
        return lookfor_memo[name]
    
    try:
        location = geolocator().geocode(name)
        if location:
            lookfor_memo[name] = (location.latitude, location.longitude) # type: ignore
            return lookfor_memo[name]
        else:
            return (None, None)
    except:
        return (None, None)