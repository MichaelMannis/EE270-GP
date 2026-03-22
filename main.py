#imports
from datetime import datetime
from math import radians, cos, sin, asin, sqrt

#define blank arrays for all data
stations = []
startvisits= []
endvisits = []
start_date = []
start_station = []
end_date = []
end_station = []
bike_number = []
bike_model = []
duration_min = []
trip_category = []
trip_type = []
start_hour = []
start_day = []
start_month = []
is_weekend = []
is_rush_hour = []
rush_period = []
station_risk_score = []
bike_instability_score = []
start_lat = []
start_long= []
end_lat = []
end_long = []
trip_distance_km= []
avg_speed= []
is_suspicious = [] # an array to tell if data is funky
dayofweek = []

def reading():
    a=1 
    f = open("01_london_bike_trips_enriched_reduced.csv")
    for lines in f:
        if a ==1: #this chunk just ignores the first line
            a=0
            continue
        # below just reads the data into the arrays
        data = lines.split(",")
        if len(data)<24:
            print("not enough data in this line")
            continue
        start_date.append(data[0])
        temp = (data[1]+","+data[2])
        start_station.append(temp)
        end_date.append(data[3])
        temp = (data[4]+","+data[5])
        end_station.append(temp)
        bike_number.append(data[6])
        bike_model.append(data[7])
        duration_min.append(data[8])
        trip_category.append(data[9])
        trip_type.append(data[10])
        start_hour.append(data[11])
        start_day.append(data[12])
        start_month.append(data[13])
        is_weekend.append(data[14])
        is_rush_hour.append(data[15])
        rush_period.append(data[16])
        station_risk_score.append(data[17])
        bike_instability_score.append(data[18])
        start_lat.append(data[19])
        start_long.append(data[20])
        end_lat.append(data[21])
        end_long.append(data[22])
        trip_distance_km.append(data[23])
        avg_speed.append(data[24])
    f.close()
#above works
def time_valid(i):
    calcmin = 0
    time_s = datetime.strptime((start_date[i].replace("/","-")), "%d-%m-%Y %H:%M")
    time_e = datetime.strptime((end_date[i].replace("/","-")), "%d-%m-%Y %H:%M")
    diff = time_e-time_s
    calcmin = (diff.total_seconds()/60) #datetime only has seconds 
    if calcmin == round(float(duration_min[i]),0):
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

def distance_valid(i):
    calcdist = 0
    calcdist = haversine(float(start_long[i]),float(start_lat[i]),float(end_long[i]),float(end_lat[i])) # i hate this but were required to use haversine
    if round(calcdist,7) == round(float(trip_distance_km[i]),7): # maths is always funky so round to avoid floating point errors 
        return True
    return False

def validate():
    for i in range(len(start_date)): # once for each set of data
        suspicious = "Not"
        if not(time_valid(i)):
            suspicious = "Bad time"
        if not(distance_valid(i)):
            if suspicious =="Not":
                suspicious = "Bad distance"
            else:
                suspicious = suspicious+" & Bad Distance" # never happens but good for future proofing
        is_suspicious.append(suspicious)

def station_data():
    for i in range(len(start_date)):
#STARTING STATIONS
        newstat = True
        for m in range(len(stations)):
            if start_station[i] == stations[m]:
                newstat = False
                startvisits[m]+=1
        if newstat:
            stations.append(start_station[i])
            startvisits.append(1)
            endvisits.append(0)
#-----------------------------
#ending stations
        newstat = True
        for m in range(len(stations)):
            if end_station[i] == stations[m]:
                newstat = False
                endvisits[m]+=1
        if newstat:
            stations.append(end_station[i])
            startvisits.append(0)
            endvisits.append(1)
#-----------------------------------
def inputvalidator():
    a = input("Would you like a CSV made? (Y/N): ")
    if a.upper() != "Y" and a.upper() != "N":
        print("Invalid input try again")
        a = inputvalidator()
    return a


def csvmaker():
    f = open("stations.csv","w")
    line = "Stations, Start, End \n"
    f.write(line)
    for i in range(len(stations)):
        line = stations[i]+","+str(startvisits[i])+","+str(endvisits[i])+"\n"
        f.write(line)
    return
        
def finddays():
    wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    for i in range(len(start_date)):
        time_s = datetime.strptime((start_date[i].replace("/","-")), "%d-%m-%Y %H:%M")
        day = wd[time_s.weekday()]
        dayofweek.append(day)
    return

def days_analysis():
    finddays()


def station_useage():
    station_data()
    starts = [0,0,0] #full define array so it can be immutable at compilation
    ends = [0,0,0] # ^
    print("The number of unique stations is: "+str(len(stations)))
# This is a rolling window
    for i in range(len(stations)): # top 3
        if startvisits[i] > starts[0] or startvisits[i] > starts[1] or startvisits[i] > starts[2]:
            starts.append(startvisits[i]) # adds to list 
            starts.sort() # sorts ascending
            starts.pop(0) # pops lowest
        if endvisits[i] > ends[0] or endvisits[i] > ends[1] or endvisits[i] > ends[2]:
            ends.append(endvisits[i]) # adds to list 
            ends.sort() # sorts ascending
            ends.pop(0) # pops lowest
#---------------------------------
    startmessage = "The three stations most started at are: "
    endmessage = "The three stations most ended at are: "
    startapp=3 #cant append more than 3 times (if stations have the same number of starts/ends)
    endapp = 3 # ^
    for i in range(len(stations)):
        if startvisits[i] >= starts[0]: # sorted array so only needs to be greater than smallest value
            if startapp>0:
                startmessage = startmessage +(stations[i].replace('"',""))+"; " # formatting 
                startapp+=-1
        if endvisits[i] >= ends[0]:
            if endapp>0:
                endmessage = endmessage +stations[i].replace('"',"")+"; " # formatting
                endapp+=-1
    print(startmessage)
    print(endmessage)
    csv = inputvalidator()
    if csv.upper() == "Y":
        csvmaker() 
    return


    

reading()
validate()
#print(is_suspicious)
station_useage()
#print(avg_speed)
#print(stations)