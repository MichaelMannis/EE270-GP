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
wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def readvalidate(data, i): # Return True if data would mess up later
    a= 0
    b=0.0
    if len(data) != 25:
        print("data on line "+str(i)+" is an invalid length and will be ignored")
        return True
    try:
        a = 1
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
    f = open("01_london_bike_trips_enriched_reduced.csv")
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
        

def dayinputvalidation():
    targetday = input("which day of the week are you interested in?: ")
    goodinput = False
    for i in range(7):
        if targetday.upper()==wd[i].upper(): #.upper to ignore capitalisation
            goodinput = True
            targetday = wd[i] # use this to ignore capitalisation in future
    if goodinput:
        print(targetday)
        return targetday
    else:
        print("Bad input please enter a day of the week: ")
        targetday = dayinputvalidation()
        return targetday

def popping(popitems):
    popitems.sort(reverse=True) # sort desc so pop doesnt change array traversal
    for i in range(len(popitems)):
        start_date.pop(popitems[i])
        start_station.pop(popitems[i])
        end_date.pop(popitems[i])
        end_station.pop(popitems[i])
        bike_number.pop(popitems[i])
        bike_model.pop(popitems[i])
        duration_min.pop(popitems[i])
        trip_category.pop(popitems[i])
        trip_type.pop(popitems[i])
        start_hour.pop(popitems[i])
        start_day.pop(popitems[i])
        start_month.pop(popitems[i])
        is_weekend.pop(popitems[i])
        is_rush_hour.pop(popitems[i])
        rush_period.pop(popitems[i])
        station_risk_score.pop(popitems[i])
        bike_instability_score.pop(popitems[i])
        start_lat.pop(popitems[i])
        start_long.pop(popitems[i])
        end_lat.pop(popitems[i])
        end_long.pop(popitems[i])
        trip_distance_km.pop(popitems[i])
        avg_speed.pop(popitems[i])
        is_suspicious.pop(popitems[i])
    return
        
def dayfilter():
    day = dayinputvalidation()
    popitems=[]
    for i in range (len(start_date)):
        if start_day[i] != day:
            popitems.append(i)
    popping(popitems)

def bigdistfilter():
    a= input("Enter a minmum distance: ")
    invalid = True
    while invalid:
        try:
            float(a)
            invalid = False
        except ValueError:
            a = input("Enter a float: ")
            invalid = True
    a = float(a)
    popitems = []
    for i in range(len(start_date)):
        if trip_distance_km[i]<a:
            popitems.append(i)
    popping(popitems)

def areavalid():
    matching = False
    area = input("Please enter an area: ")
    area = area.replace(" ","")
    go = ""
    for i in range(len(start_date)):
        end_data = end_station[i].split(",")
        endnew = end_data[1]
        start_data = start_station[i].split(",")
        new = start_data[1] # gets the bit after the comma
        endnew = endnew.replace(" ","").replace('"',"")
        new = new.replace(" ","").replace('"',"")
        if area.upper() == new.upper() or area.upper() == endnew.upper():
            matching= True
    if matching== False:
        print("There were no results found for this area do you wish to retry")
        go = input("Y/N: ")
        while go.upper() != "Y" and go.upper() != "N":
            print("Bad input")
            go = input("There were no results found for this area do you wish to retry (Y/N): ")
    if go.upper() == "Y":
        area = areavalid()
        return area
    elif go.upper() == "N":
        return area
    return area
    

def startareafilter(area):
    popitems = []
    for i in range(len(start_date)):
        data = start_station[i].split(",")
        new = data[1] # gets the bit after the comma
        if area.upper().replace(" ","") != new.upper().replace(" ","").replace('"',""):#remove spaces and "
            popitems.append(i)
    popping(popitems)

def endareafilter(area):
    popitems = []
    for i in range(len(start_date)):
        data = end_station[i].split(",")
        new = data[1] # gets the bit after the comma
        if area.upper().replace(" ","") != new.upper().replace(" ","").replace('"',""):#remove spaces and "
            popitems.append(i)
    popping(popitems)
        

def suspiciousdatafilter():
    popitems = []
    for i in range(len(start_date)):
        if is_suspicious[i] !="Not":
            popitems.append(i)
    popping(popitems)

def analysis():

    number_of_journeys= 0 
    minduration = 0 # will change from 0 in program
    maxduration = 0 # duration cant be negative 
    avg_duration = 0
    maxdist = 0 # dist cant be negative
    mindist = 0 # will change from 0 in program
    avgdist = 0
    if len(start_date)== 0:
        print("There is no matching data for your current filters.")
        return
    for i in range(len(start_date)):
        number_of_journeys+=1
        if duration_min[i]<minduration or minduration==0:
                minduration=duration_min[i]
        if duration_min[i]>maxduration: # duration cant be negative 
            maxduration=duration_min[i]
        avg_duration+=duration_min[i] # add all values and divide at end
        if trip_distance_km[i]>maxdist:
            maxdist= trip_distance_km[i]
        if trip_distance_km[i]<mindist or mindist==0:
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

def filterhandle():
    area = ""
    print("""
          ---------------------------
          Which filter would you like
          1. Day of the Week
          2. Distance Greater than X
          3. Journeys starting in a specific area
          4. Journeys ending in a specific area
          5. Suspicious data (has values that dont match)
          Continue later
          """)
    selection = input("- ")
    while selection != "1" and selection != "2" and selection != "3" and selection !="4" and selection != "5":
        selection = input("Bad input enter a number 1-5: ")
    if selection =="1":
        dayfilter()
    elif selection =="2":
        bigdistfilter()
    elif selection =="3":
        area = areavalid()
        startareafilter(area)
    elif selection == "4":
        area = areavalid()
        endareafilter(area)
    elif selection =="5":
        suspiciousdatafilter()



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
#station_useage()
filterhandle()
analysis()