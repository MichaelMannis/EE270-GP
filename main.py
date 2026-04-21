# --- Imports ---
import Validation as valid          # Handles suspicious data detection (time and distance checks)
import filtering as filtering       # Handles user-driven journey filtering
import stationdata as stationdata   # Handles station usage analysis and CSV export

# --- Data Arrays ---
# All journey data is stored in parallel arrays — each index corresponds to one journey
stations = []                   # Unique station names discovered during analysis
startvisits = []                # Visit counts for each station as a start point
endvisits = []                  # Visit counts for each station as an end point
start_date = []                 # Journey start datetime strings
start_station = []              # Journey start station (name + area combined)
end_date = []                   # Journey end datetime strings
end_station = []                # Journey end station (name + area combined)
bike_number = []                # Bike identifier number
bike_model = []                 # Bike model name/type
duration_min = []               # Journey duration in minutes
trip_category = []              # Category label for the trip
trip_type = []                  # Type label for the trip
start_hour = []                 # Hour of day the journey started
start_day = []                  # Day of the week the journey started
start_month = []                # Month the journey started
is_weekend = []                 # Flag indicating whether the journey was on a weekend
is_rush_hour = []               # Flag indicating whether the journey was during rush hour
rush_period = []                # Which rush period the journey fell in (if any)
station_risk_score = []         # Risk score associated with the start station
bike_instability_score = []     # Instability score for the bike used
start_lat = []                  # Latitude of the start station
start_long = []                 # Longitude of the start station
end_lat = []                    # Latitude of the end station
end_long = []                   # Longitude of the end station
trip_distance_km = []           # Recorded trip distance in kilometres
avg_speed = []                  # Average speed of the journey
ignore = []                     # Indices of journeys to exclude from analysis (populated by filters)
is_suspicious = []              # Suspicion flag per journey: "Not", "Bad time", or "Bad distance"
wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']  # Valid days for the day filter

# -------------------------
# Actual Code Starts from below
# -------------------------

def readvalidate(data, i):
    """
    Validates a single row of CSV data before it is appended to any array.
    Checks that the row has the expected number of fields and that all
    fields which must be numeric can be successfully cast.
    Returns True if the row should be skipped, False (implicitly) if it is valid.
    """
    a = 0    # Placeholder for integer cast attempts
    b = 0.0  # Placeholder for float cast attempts

    # Every valid row should have exactly 25 comma-separated fields
    if len(data) != 25:
        print("data on line " + str(i) + " is an invalid length and will be ignored")
        return True

    try:
        # Attempt to cast each field that must be a specific numeric type
        # If any cast fails a ValueError is raised and the row is rejected
        a = int(data[6])    # Bike number must be an integer
        b = float(data[8])  # Duration must be a float
        a = int(data[14])   # is_weekend must be an integer
        a = int(data[15])   # is_rush_hour must be an integer
        b = float(data[17]) # Station risk score must be a float
        b = float(data[18]) # Bike instability score must be a float
        b = float(data[19]) # Start latitude must be a float
        b = float(data[20]) # Start longitude must be a float
        b = float(data[21]) # End latitude must be a float
        b = float(data[22]) # End longitude must be a float
        b = float(data[23]) # Trip distance must be a float
        b = float(data[24]) # Average speed must be a float
    except ValueError:
        # Notify the user which row was rejected and why
        print("Data of incorrect type in row " + str(i) + " and will be ignored")
        return True


def reading():
    """
    Opens the CSV data file, skips the header row, and reads each subsequent
    row into the corresponding parallel arrays. Rows that fail validation
    via readvalidate() are silently skipped.
    Station name and area are concatenated with a comma so they can be
    split apart again later during area filtering.
    """
    a = 1  # Flag used to skip the header row on the first iteration
    f = open("01_london_bike_trips_enriched_02.csv")

    for pos, lines in enumerate(f):
        # Skip the first line (CSV header row)
        if a == 1:
            a = 0
            continue

        # Split the line into individual fields by comma delimiter
        data = lines.split(",")

        # Validate the row — skip it entirely if validation fails
        if readvalidate(data, pos):
            continue

        # Append each field to its corresponding data array
        start_date.append(data[0])

        # Combine station name and area into a single string (split again later by area filters)
        temp = (data[1] + "," + data[2])
        start_station.append(temp)

        end_date.append(data[3])

        # Same combination for end station
        temp = (data[4] + "," + data[5])
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

    # Close the file once all rows have been processed
    f.close()


def suspiciousanalysis():
    """
    Counts how many journeys were flagged as suspicious and prints the
    result as a percentage of the total number of journeys read.
    """
    counter = 0
    for i in is_suspicious:
        if i != "Not":
            counter += 1  # Count every journey that wasn't marked clean

    # Round to 4 decimal places for a readable but precise percentage
    percentage = str(round(counter / len(is_suspicious) * 100, 4)) + "%"
    print("The percentage of suspicious data is " + percentage)


def analysis(ignore):
    """
    Calculates and prints summary statistics for all non-ignored journeys:
      - Total number of journeys
      - Max, min, and average duration (minutes)
      - Max, min, and average distance (km)
    Journeys whose index appears in the ignore list are skipped.
    """
    # Guard against the case where all data has been filtered out
    if len(start_date) == 0:
        print("There is no matching data for your current filters.")
        return

    a = 0               # Pointer into the ignore list
    number_of_journeys = 0

    # Initialise min values to the first data point rather than 0,
    # since 0 would always win as the minimum otherwise
    minduration = duration_min[0]
    maxduration = 0     # Duration can't be negative so 0 is a safe starting maximum
    avg_duration = 0

    maxdist = 0         # Distance can't be negative so 0 is a safe starting maximum
    mindist = trip_distance_km[0]
    avgdist = 0

    # Append a sentinel value so the ignore pointer never goes out of bounds
    ignore.append(-1)

    for i in range(len(start_date)):
        # Skip this journey if its index is in the ignore list
        if i == ignore[a]:
            a += 1
            continue

        number_of_journeys += 1

        # Update duration min/max
        if duration_min[i] < minduration:
            minduration = duration_min[i]
        if duration_min[i] > maxduration:
            maxduration = duration_min[i]

        avg_duration += duration_min[i]  # Accumulate for averaging later

        # Update distance min/max
        if trip_distance_km[i] > maxdist:
            maxdist = trip_distance_km[i]
        if trip_distance_km[i] < mindist:
            mindist = trip_distance_km[i]

        avgdist += trip_distance_km[i]  # Accumulate for averaging later

    # Avoid division by zero if somehow no journeys passed the filter
    if number_of_journeys > 0:
        avg_duration = avg_duration / number_of_journeys
        avgdist = avgdist / number_of_journeys

    # --- Print Results ---
    print("The total number of journeys made is " + str(number_of_journeys))
    print("The maximum duration of journeys made is " + str(maxduration))
    print("The minimum duration of journeys made is " + str(minduration))
    print("The average duration of journeys made is " + str(avg_duration))
    print("The maximum distance of journeys made is " + str(maxdist))
    print("The minimum distance of journeys made is " + str(mindist))
    print("The average distance of journeys made is " + str(avgdist))


# -------------------------
# Main Execution
# -------------------------
reading()# Read all journey data from the CSV into the parallel arrays
valid.validate(start_date, is_suspicious, trip_distance_km,duration_min, end_date, start_long, start_lat, end_long, end_lat)
suspiciousanalysis()    # Print the percentage of journeys flagged as suspicious
filtering.filterhandle(start_date, start_day, ignore, start_station, end_station, trip_distance_km, is_suspicious)
analysis(ignore) # Print summary statistics for all non-ignored journeys
stationdata.station_useage(ignore, start_date, stations, start_station, end_station, startvisits, endvisits)