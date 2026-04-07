from math import radians, cos, sin, asin, sqrt
from datetime import datetime
def time_valid(i,start_date,duration,enddate):
    calcmin = 0
    if duration ==0:
        return False
    time_s = datetime.strptime((start_date[i].replace("/","-")), "%d-%m-%Y %H:%M")
    time_e = datetime.strptime((enddate[i].replace("/","-")), "%d-%m-%Y %H:%M")
    diff = time_e-time_s
    calcmin = (diff.total_seconds()/60) #datetime only has seconds 
    if calcmin == round(float(duration[i]),0):
        return True
    return False

def haversine(lon1, lat1, lon2, lat2): # just trust me this works dw about it
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Km assumption
    return c * r

def distance_valid(i,tripdist,slong,slat,elong,elat):
    calcdist = 0
    if (tripdist[i] == 0):
        return False
    calcdist = haversine(float(slong[i]),float(slat[i]),float(elong[i]),float(elat[i])) # i hate this but were required to use haversine
    if round(calcdist,7) == round(float(tripdist[i]),7): # maths is always funky so round to avoid floating point errors 
        return True
    return False

def validate(start_date,is_suspicious,tripdist,duration,enddate,slong,slat,elong,elat):
    for i in range(len(start_date)): # once for each set of data
        suspicious = "Not"
        if not(time_valid(i,start_date,duration,enddate)):
            suspicious = "Bad time"
        if not(distance_valid(i,tripdist,slong,slat,elong,elat)):
            suspicious = "Bad distance"
        is_suspicious.append(suspicious)