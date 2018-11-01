from urllib.request import urlopen
import json
import time
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import csv

token = "TOKEN_VK"

def get_multicity():
"""Get localities in the region. 1157049 - Republic of Tuva"""
    url = "https://api.vk.com/method/database.getCities.json?region_id=1157049&country_id=1&count=200&access_token=%s&v=5.52" % token
    response = urlopen(url)
    data = response.read()
    city = json.loads(data)
    return city
    
def get_count():
"""Parser function and geolocation"""
    place = []
    for i in get_multicity()["response"]["items"]:
        url = "https://api.vk.com/method/users.search.json?sort=1&city=%s&online=1&access_token=%s&v=5.84" % (i["id"],token)
        response = urlopen(url)
        time.sleep(3)
        data = response.read()
        cn = json.loads(data)
        count = (cn["response"]["count"])
        i["count"] = count
        
        ad = {"city": i["title"], "region": i["region"]}
        geolocator = Nominatim() #user_agent="shaltay@inbox.ru"
        location = geolocator.geocode(ad,timeout=10)
        
        if location is not None:
            lat_point = location.latitude 
            lot_point = location.longitude
            i["lat"] = lat_point
            i["lot"] = lot_point
        else:
            i["lat"] = 0
            i["lot"] = 0

        place.append(i)
        print (i)
    return place
    
def save_cvs():
"""Save to CSV"""
    datagroup = get_count()
    with open( "/parser_result.cvs", "w", encoding='utf-8' ) as file:
        fieldnames = ['id', 'title', 'region', 'count', 'lat', 'lot']
        writer = csv.DictWriter( file, fieldnames=fieldnames )
        writer.writeheader()
        for sgroup in datagroup:
            idg = (sgroup["id"])
            nmg = (sgroup["title"])
            tyg = (sgroup["region"])
            phg = (sgroup["count"])
            cig = (sgroup["lat"])
            lto = (sgroup["lot"])
save_cvs()
            writer.writerow({'id': idg, 'title': nmg, 'region': tyg, 'count': phg, 'lat': cig, 'lot': lto})
