# -*- coding: utf-8 -*-

def week_day_analysis():

    import csv
    
    
    def dataimport():
        
        #store rows from excel in list
        dataset = []
        
        #open and read 
        d = open('merged.csv','r')
        
        #turns each line into a dictionary
        data = csv.DictReader(d)
        
        #loop through each row in file
        for row in data:
            #changing the required records into floats
            row['trip_distance_km'] = float(row['trip_distance_km'])
            row['duration_min'] = float(row['duration_min'])
            
            #start_day doesnt need to be changed when it is used
            
            #stores the changed and non changed data into dataset to be used later
            dataset.append(row)
    
        d.close()
        return dataset
    
    
    def inputvalidation ():
        #create list with day names
        dayNames = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        #create valiud input boolean variable
        validInput = False
        
        #loop until valid input is found
        while validInput == False:
            userInput = input("enter the name of a day to search: ")
            
            #check if input is valid by comparing to list of valid names
            if userInput in dayNames:
                validInput = True
            else:
                print("enter a valid capitalilsed day name with capital")
                
        
        return userInput
    
    
    def weekdayanalysis (inputuser, importedData):
    
        #initialise variables
        #min is infinite so new min is always smaller
        #max is 0 so new max is always bigger
        minDuration = float('inf')
        maxDuration = 0
        minDistance = float('inf')
        maxDistance = 0
        
        totalDistance = 0
        totalDuration = 0
        totalDays = 0
        
        
        #for loop which goes through dataset
        for row in importedData:
            #check if input matches day
            if row['start_day'] == inputuser:
                #add one to total
                totalDays += 1
                
                #compare to min duration
                if row['duration_min'] < minDuration:
                    #update min to new min
                    minDuration = row['duration_min']
                
                #compare to max duration
                if row['duration_min'] > maxDuration:
                    #update max to new max
                    maxDuration = row['duration_min']
                
                #running total for duration
                totalDuration += row['duration_min']
                
                
                #compare to min distance
                if row['trip_distance_km'] < minDistance:
                    #update min to new min
                    minDistance = row['trip_distance_km']
                
                #compare to max distance
                if row['trip_distance_km'] > maxDistance:
                    #update max to new max
                    maxDistance = row['trip_distance_km']
                
                
                #running total for distance
                totalDistance += row['trip_distance_km']
        
        #calculate averages
        if totalDays > 0:
            
            averageDuration = totalDuration/totalDays
            averageDistance = totalDistance/totalDays
            
            print("the stats for day: ", inputuser)
            print("total number of journeys: ", totalDays)
            print("minimum journey duration: ", minDuration)
            print("maximum journey duration: ", maxDuration)
            print("average journey duration: ", averageDuration)
            print("minimum trip distance: ", minDistance)
            print("maximum trip distance: ", maxDistance)
            print("average trip distance: ", averageDistance)
            print("Week Day Analysis Complete :)")
        else:
            print("no data :(")
                
    #runs the function to get a user input and save it        
    inputuser = inputvalidation()
    #runs the function to import the data from the excel spreadsheet and saves in a list
    importedData = dataimport()
    #runs the analysis section using the values returned from the other functions
    weekdayanalysis(inputuser, importedData)     
   