def station_useage(ignore, start_date, stations, start_station, end_station, startvisits, endvisits):
    """
    Main handler for station usage analysis.
    Calculates visit counts per station, prints the top 3 most used start/end stations,
    and optionally exports the results to a CSV file.
    """
    print("""
          
        Calcualting station data please wait...

          """)

    # Populate the stations, startvisits, and endvisits lists from journey data
    station_data(ignore, start_date, stations, start_station, end_station, startvisits, endvisits)

    # Initialise fixed-size arrays to track the top 3 visit counts for starts and ends
    starts = [0, 0, 0]  # Holds the top 3 start visit counts (ascending order)
    ends = [0, 0, 0]    # Holds the top 3 end visit counts (ascending order)

    print("The number of unique stations is: " + str(len(stations)))

    # Rolling window: iterate through all stations and maintain a sorted top-3 list
    for i in range(len(stations)):
        # If the current station's start count beats any value in the top 3, replace the lowest and re-sort
        if startvisits[i] > starts[0] or startvisits[i] > starts[1] or startvisits[i] > starts[2]:
            starts[0] = startvisits[i]  # Overwrite the current lowest value
            starts.sort()               # Re-sort ascending so starts[0] is always the smallest

        # Same logic applied to end visit counts
        if endvisits[i] > ends[0] or endvisits[i] > ends[1] or endvisits[i] > ends[2]:
            ends[0] = endvisits[i]
            ends.sort()

    # Build output messages listing the top 3 most-used start and end stations
    startmessage = "The three stations most started at are: "
    endmessage = "The three stations most ended at are: "

    # Counters to cap output at 3 stations in case multiple stations share the same visit count
    startapp = 3
    endapp = 3

    for i in range(len(stations)):
        # starts[0] is the smallest of the top 3, so any station matching or exceeding it qualifies
        if startvisits[i] >= starts[0]:
            if startapp > 0:
                startmessage = startmessage + (stations[i].replace('"', "")) + "; "  # Strip quotes for clean output
                startapp -= 1  # Decrement to enforce the 3-station cap

        if endvisits[i] >= ends[0]:
            if endapp > 0:
                endmessage = endmessage + stations[i].replace('"', "") + "; "  # Strip quotes for clean output
                endapp -= 1

    print(startmessage)
    print(endmessage)

    # Ask the user if they want the station data exported to a CSV file
    csv = inputvalidator()
    if csv.upper() == "Y":
        csvmaker(stations, startvisits, endvisits)
    return


def station_data(ignore, start_date, stations, start_station, end_station, startvisits, endvisits):
    """
    Iterates through all journeys and counts how many times each station
    appears as a start or end point. Skips any journey indices listed in ignore.
    Populates the stations, startvisits, and endvisits lists in place.
    """
    a = 0           # Pointer to track the current position in the ignore list
    ignore.append(0)  # Sentinel value to prevent index errors when ignore is empty

    for i in range(len(start_date)):
        # Skip this journey if its index is in the ignore list
        if i == ignore[a]:
            a += 1
            continue

        # --- Starting Stations ---
        newstat = True  # Assume this is a station not yet seen
        for m in range(len(stations)):
            if start_station[i] == stations[m]:
                newstat = False       # Station already exists in the list
                startvisits[m] += 1  # Increment its start visit count
        if newstat:
            # First time seeing this start station — add it with 1 start visit and 0 end visits
            stations.append(start_station[i])
            startvisits.append(1)
            endvisits.append(0)

        # --- Ending Stations ---
        newstat = True  # Reset flag for end station check
        for m in range(len(stations)):
            if end_station[i] == stations[m]:
                newstat = False      # Station already exists in the list
                endvisits[m] += 1   # Increment its end visit count
        if newstat:
            # First time seeing this end station — add it with 0 start visits and 1 end visit
            stations.append(end_station[i])
            startvisits.append(0)
            endvisits.append(1)


def inputvalidator():
    """
    Prompts the user for a Y/N response on whether to generate a CSV.
    Recursively re-prompts on invalid input. Returns the validated input string.
    """
    a = input("Would you like a CSV made? (Y/N): ")
    if a.upper() != "Y" and a.upper() != "N":
        print("Invalid input try again")
        a = inputvalidator()  # Retry on invalid input
    return a


def csvmaker(stations, startvisits, endvisits):
    """
    Writes station visit data to a CSV file named 'stations.csv'.
    Each row contains a station name, its start visit count, and its end visit count.
    """
    f = open("stations.csv", "w")  # Open (or create) the output file in write mode

    # Write the header row
    line = "Stations, Start, End \n"
    f.write(line)

    # Write one row per station with its corresponding visit counts
    for i in range(len(stations)):
        line = stations[i] + "," + str(startvisits[i]) + "," + str(endvisits[i]) + "\n"
        f.write(line)
    return