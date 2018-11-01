import folium
from folium.features import DivIcon
import csv
import re
import datetime

def cvs_read():
    point = []
    file = "/parser_result.cvs" #see parser_data.py
    with open(file, encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        for i in rows:
            title = (i["title"])
            count = (i["count"])
            lat = (i["lat"])
            lot = (i["lot"])
            if lat != "0":
                poi = title,count,lat,lot
                point.append(poi)
    return point

kyzyl = (51.7190995,94.4300627)
m = folium.Map(location=kyzyl, tiles='Stamen Toner', zoom_start=7, width=900, height=550) #Stamen Toner Stamen Terrain 

for i in cvs_read():
    lat = float(i[2])
    lot = float(i[3])
    title = (i[0])
    count = str(i[1])
    folium.Marker((lat,lot), icon=DivIcon(html="<h6>"+title+"-"+count+"</h6>")).add_to(m)
    
    if int(i[1]) < 1000:
        folium.CircleMarker((lat,lot), radius=1, color='#ff0000', fill_color='#ff0000', popup=(i[1])).add_to(m)
    else:
        folium.CircleMarker((lat,lot), radius=10, color='#ff0000', fill_color='#ff0000', popup=(i[1])).add_to(m)

now = datetime.datetime.now()
time =  now.strftime("%d-%m-%Y %H:%M")
legend_html = "<h3>Активность пользователей сети ВК на %s</h3>" % time
m.get_root().html.add_child(folium.Element(legend_html))
m
