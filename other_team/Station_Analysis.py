# -*- coding: utf-8 -*-

def station_analysis():

    # Python opens merged.csv for reading and stations.csv for writing
    f = open('merged.csv', 'r')
    g = open('stations.csv', 'w')
    
    # The headings are written into the new stations.csv output file
    g.write("Stations, Start, End\n")
    
    # Empty list to add unique stations into
    no_unique_stations = []
    
    # Empty dictionarys for most frequent start and end stations
    most_freq_start_station = {}
    most_freq_end_station = {}
    
    # Creating an index to skip the first line which only includes headers
    index = 0
    
    # Creating a for loop to analyse the stations
    for line in f:
        
        # If statement skips the first line containing only headers
        if index == 0:
            
            index = 1
            continue
        
        # strip() removes the hidden characters from the line and split(',') will split the line
        # into a list so its easier to analyse
        row = line.strip().split(',')
        
        # Creating variables only containing the info that needs to be analysed, since python 
        # will split the station name into its two parts using split(','), since it is seperated
        # by a comma, they must be rejoined. 
        start_station = ",".join(row[1:3])
        end_station = ",".join(row[4:6])
        
        # Checking if start station has been put in unique stations yet
        if start_station not in no_unique_stations:
            
            # If start station isn't in unique stations it is added
            no_unique_stations.append(start_station)
            
        # Same check but for end station this time    
        if end_station not in no_unique_stations:
            
            no_unique_stations.append(end_station)
            
        # Checking how many times start station appears in merged.csv
        if start_station not in most_freq_start_station:
            
            # If start station is not in most frequent start stations, it is added and a
            # value of 1 is given to indicate it has appeared 
            most_freq_start_station[start_station] = 1
        
        if start_station in most_freq_start_station:
            
            #If start station is in most frequent start stations, 1 is added to the value
            most_freq_start_station[start_station] += 1
            
        # Same checks but for end station 
        if end_station not in most_freq_end_station:
            
           most_freq_end_station[end_station] = 1
        
        if end_station in most_freq_end_station:
            
            most_freq_start_station[start_station] += 1
        
    # Now that the dictionarys and list has been made these can now be analysed
    
    # Finding the length of the number of unique stations list to give how many unique stations there is 
    unique_stations = len(no_unique_stations)
    
    print("The number of unique stations is:", unique_stations)
    
    # Sort unique stations into alphabetical order for ease of analysis
    
    alphabetical_stations = sorted(no_unique_stations)
    
    # For loop to write station data into stations.csv
    for station in alphabetical_stations:
        
        # .get() gets the value of the station in the dictionary and makes it a variable
        # if the station is not in the dictionary a value of 0 is given
        start = most_freq_start_station.get(station, 0)
        end = most_freq_end_station.get(station, 0)
        
        # Writing the station, its start station frequency and its ned station frequency into
        # stations.csv
        g.write(f'"{station}", {start}, {end}\n')
        
    # Now making the in window analysis
    
    # This function makes python only look at the frequency part of the station frequency pair, allowing
    # it to be easily sorted in the next step. Making a function here means I can reuse it when finding top 
    # three end frequencys too
    def station_frequency(pair):
        return pair[1]
    
    # sorted reverse = True makes python sort from highest to lowest, items splits the dictionary into a 
    # tuple and key calls the function station_frequency to make python only look at the frequency
    sorted_start_stations = sorted(most_freq_start_station.items(), key = station_frequency, reverse = True)
    
    # Gives the top 3 start stations
    top_3_start = sorted_start_stations[:3]
    
    # Same but for end stations this time
    sorted_end_stations = sorted(most_freq_end_station.items(), key = station_frequency, reverse = True)
    top_3_end = sorted_end_stations[:3]
    
    print("The top 3 start stations are:", top_3_start)
    print("The top 3 end stations are:", top_3_end)
    
    # Closes merged.csv and stations.csv
    f.close()
    g.close()
        
    print("Station Analysis Complete :)")

    