def station_useage(ignore,start_date,stations,start_station,end_station,startvisits,endvisits):
    print("""
          
        Calcualting station data please wait...

          """)
    station_data(ignore,start_date,stations,start_station,end_station,startvisits,endvisits)
    starts = [0,0,0] #full define array so it can be immutable at compilation
    ends = [0,0,0] # ^
    print("The number of unique stations is: "+str(len(stations)))
# This is a rolling window
    for i in range(len(stations)): # top 3
        if startvisits[i] > starts[0] or startvisits[i] > starts[1] or startvisits[i] > starts[2]:
            starts[0] = startvisits[i] # adds to list 
            starts.sort() # sorts ascending
        if endvisits[i] > ends[0] or endvisits[i] > ends[1] or endvisits[i] > ends[2]:
            ends[0] = endvisits[i] # adds to list 
            ends.sort() # sorts ascending
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
        csvmaker(stations,startvisits,endvisits) 
    return

def station_data(ignore,start_date,stations,start_station,end_station,startvisits,endvisits):
    a = 0
    ignore.append(0)
    for i in range(len(start_date)):
        if i ==ignore[a]:
            a+=1
            continue
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

def csvmaker(stations,startvisits,endvisits):
    f = open("stations.csv","w")
    line = "Stations, Start, End \n"
    f.write(line)
    for i in range(len(stations)):
        line = stations[i]+","+str(startvisits[i])+","+str(endvisits[i])+"\n"
        f.write(line)
    return