from math import radians, cos, sin, asin, sqrt
from datetime import datetime

def time_valid(i, start_date, duration, enddate):
    """
    Checks whether the recorded duration of a journey matches the actual difference
    between its start and end timestamps.
    Returns True if they match, False if the duration is 0 or the values don't agree.
    """
    calcmin = 0

    # A duration of 0 is invalid — skip rather than risk a divide/compare on bad data
    if duration == 0:
        return False

    # Parse start and end timestamps, normalising "/" separators to "-" for strptime
    time_s = datetime.strptime((start_date[i].replace("/", "-")), "%d-%m-%Y %H:%M")
    time_e = datetime.strptime((enddate[i].replace("/", "-")), "%d-%m-%Y %H:%M")

    # Calculate the difference between end and start as a timedelta
    diff = time_e - time_s

    # Convert to minutes — timedelta only exposes total_seconds() directly
    calcmin = (diff.total_seconds() / 60)

    # Compare the calculated minutes against the recorded duration (rounded to nearest minute)
    if calcmin == round(float(duration[i]), 0):
        return True
    return False


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculates the great-circle distance in kilometres between two points
    on the Earth's surface given their longitude and latitude in decimal degrees.
    Uses the Haversine formula, which accounts for the curvature of the Earth.
    """
    # Convert all coordinates from decimal degrees to radians for trig functions
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # Compute the differences in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # Haversine formula: calculates the central angle between the two points
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    r = 6371  # Mean radius of the Earth in kilometres

    # Multiply the central angle by the Earth's radius to get the surface distance
    return c * r


def distance_valid(i, tripdist, slong, slat, elong, elat):
    """
    Checks whether the recorded trip distance matches the Haversine distance
    calculated from the journey's start and end coordinates.
    Returns True if they match, False if the recorded distance is 0 or the values don't agree.
    """
    calcdist = 0

    # A recorded distance of 0 is invalid — treat as suspicious without calculating
    if tripdist[i] == 0:
        return False

    # Calculate the expected distance from coordinates using the Haversine formula
    calcdist = haversine(float(slong[i]), float(slat[i]), float(elong[i]), float(elat[i]))

    # Round both values to 7 decimal places to avoid floating point precision mismatches
    if round(calcdist, 7) == round(float(tripdist[i]), 7):
        return True
    return False


def validate(start_date, is_suspicious, tripdist, duration, enddate, slong, slat, elong, elat):
    """
    Iterates through all journeys and flags each one as suspicious if its
    time or distance data appears inconsistent.
    Results are appended to is_suspicious as one of:
      - "Not"          — data looks valid
      - "Bad time"     — recorded duration doesn't match the timestamps
      - "Bad distance" — recorded distance doesn't match the coordinates
    Note: if both checks fail, the entry will be marked "Bad distance" (last write wins).
    """
    for i in range(len(start_date)):
        suspicious = "Not"  # Default assumption — data is valid unless a check fails

        # Override if the recorded duration doesn't match the calculated time difference
        if not(time_valid(i, start_date, duration, enddate)):
            suspicious = "Bad time"

        # Override if the recorded distance doesn't match the Haversine calculation
        # Note: this will overwrite "Bad time" if both checks fail
        if not(distance_valid(i, tripdist, slong, slat, elong, elat)):
            suspicious = "Bad distance"

        # Append the result for this journey to the suspicious flags list
        is_suspicious.append(suspicious)