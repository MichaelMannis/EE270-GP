import Validation as valid
import filtering as filtering
import stationdata as stationdata
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
ignore = []
is_suspicious = [] # an array to tell if data is funky
wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def readvalidate(data, i): # Return True if data would mess up later
    a= 0
    b=0.0
    if len(data) != 25:
        print("data on line "+str(i)+" is an invalid length and will be ignored")
        return True
    try:
        a = int(data[6]) # bikenumber cast
        b= float(data[8]) # duration cast
        a = int(data[14])
        a =int(data[15])
        b= float(data[17])
        b= float(data[18])
        b= float(data[19])
        b= float(data[20])
        b= float(data[21])
        b= float(data[22])
        b= float(data[23])
        b= float(data[24])# just trust that this works.
    except ValueError:
        print("Data of incorrect type in row "+str(i)+" and will be ignored")
        return True
def reading():
    a=1
    f = open("01_london_bike_trips_enriched_02.csv")
    for pos, lines in enumerate(f):
        if a ==1: #this chunk just ignores the first line
            a=0
            continue
        # below just reads the data into the arrays
        data = lines.split(",")
        if readvalidate(data, pos):
            continue
        start_date.append(data[0])
        temp = (data[1]+","+data[2])
        start_station.append(temp)
        end_date.append(data[3])
        temp = (data[4]+","+data[5])
        end_station.append(temp)
        bike_number.append(data[6])
        bike_model.append(data[7])
        duration_min.append(float(data[8]))
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
        trip_distance_km.append(float(data[23]))
        avg_speed.append(data[24])
    f.close()

def suspiciousanalysis():
    counter = 0 
    for i in is_suspicious:
        if i != "Not":
            counter+=1
    percentage = str(round(counter/len(is_suspicious)*100,4))+"%"
    print("The percentage of suspicious data is "+percentage)

def analysis(ignore):
    if len(start_date)== 0:
        print("There is no matching data for your current filters.")
        return
    a = 0
    number_of_journeys= 0 
    minduration = duration_min[0] #
    maxduration = 0 # duration cant be negative 
    avg_duration = 0
    maxdist = 0 # dist cant be negative
    mindist = trip_distance_km[0] # will change from 0 in program
    avgdist = 0
    ignore.append(-1)

    for i in range(len(start_date)):
        if i ==ignore[a]:
            a+=1
            continue

        number_of_journeys+=1
        if duration_min[i]<minduration:
                minduration=duration_min[i]
        if duration_min[i]>maxduration: # duration cant be negative 
            maxduration=duration_min[i]
        avg_duration+=duration_min[i] # add all values and divide at end
        if trip_distance_km[i]>maxdist:
            maxdist= trip_distance_km[i]
        if trip_distance_km[i]<mindist:
            mindist=trip_distance_km[i]
        avgdist+=trip_distance_km[i]
    if number_of_journeys>0:
        avg_duration = avg_duration/number_of_journeys # makes an average
        avgdist = avgdist/number_of_journeys # makes an average
    #---------Below is just printing
    print("The total number of journeys made is "+str(number_of_journeys))
    print("The maximum duration of journeys made is "+str(maxduration))
    print("The minimum duration of journeys made is "+str(minduration))
    print("The average duration of journeys made is "+str(avg_duration))
    print("The maximum distance of journeys made is "+str(maxdist))
    print("The minimum distance of journeys made is "+str(mindist))
    print("The average distance of journeys made is "+str(avgdist))

 
reading()
valid.validate(start_date,is_suspicious,trip_distance_km,duration_min,end_date,start_long,start_lat,end_long,end_lat)
suspiciousanalysis()
filtering.filterhandle(start_date,start_day,ignore,start_station,end_station,trip_distance_km,is_suspicious)
analysis(ignore)
stationdata.station_useage(ignore,start_date,stations,start_station,end_station,startvisits,endvisits)