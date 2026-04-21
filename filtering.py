wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

def filterhandle(startdate, startday, ignore, startstation, endstation, tripdist, suspicious):
    """
    This function handles all filtering operations.
    Presents a menu to the user and calls the appropriate filter function based on their selection.
    Multiple filters can be applied sequentially by adding indices to the ignore list.
    """
    repeat = True
    area = ""  # Stores the area name when filtering by start/end area

    while repeat:
        # Display filter selection menu
        print("""
          ---------------------------
          Which filter would you like
          1. Day of the Week
          2. Distance Greater than X
          3. Journeys starting in a specific area
          4. Journeys ending in a specific area
          5. Suspicious data (has values that dont match)
          6. No filter
          """)

        selection = input("- ")

        # Validate input — keep prompting until a valid option (1-6) is entered
        while selection != "1" and selection != "2" and selection != "3" and selection != "4" and selection != "5" and selection != "6":
            selection = input("Bad input enter a number 1-5: ")

        # Call the appropriate filter function based on user selection
        if selection == "1":
            dayfilter(startdate, startday, ignore)
        elif selection == "2":
            bigdistfilter(startdate, tripdist, ignore)
        elif selection == "3":
            # Validate the area input before filtering by start station
            area = areavalid(startdate, startstation, endstation)
            startareafilter(area, startdate, startstation, ignore)
        elif selection == "4":
            # Validate the area input before filtering by end station
            area = areavalid(startdate, startstation, endstation)
            endareafilter(area, startdate, endstation, ignore)
        elif selection == "5":
            suspiciousdatafilter(startdate, suspicious, ignore)
        elif selection == "6":
            return()  # Exit immediately with no filter applied

        # Ask whether the user wants to apply an additional filter
        go = input("Would you like to add another filter? (Y/N):")
        while go.upper() != "Y" and go.upper() != "N":
            print("Bad input")
            go = input("Would you like to add another filter? (Y/N):")

        # Continue looping if user wants another filter, otherwise exit
        if go.upper() == "Y":
            repeat = True
        else:
            repeat = False
    return()


def dayfilter(startdate, startday, ignore):
    """Adds the index of any journey to ignore if it didn't occur on the target day."""
    day = dayinputvalidation()  # Get and validate the target day from user
    for i in range(len(startdate)):
        if startday[i] != day:
            ignore.append(i)  # Mark journey for exclusion if day doesn't match
    return()


def dayinputvalidation():
    """
    Prompts the user for a day of the week and validates the input.
    Recursively re-prompts on bad input. Returns a correctly-cased day string.
    """
    targetday = input("which day of the week are you interested in?: ")
    goodinput = False

    # Check if the input matches any day in the list (case-insensitive)
    for i in range(7):
        if targetday.upper() == wd[i].upper():
            goodinput = True
            targetday = wd[i]  # Normalise casing to match the wd list

    if goodinput:
        return targetday
    else:
        # Recursively prompt again on invalid input
        print("Bad input please enter a day of the week: ")
        targetday = dayinputvalidation()
        return targetday


def bigdistfilter(startdate, tripdist, ignore):
    """
    Prompts the user for a minimum distance and adds any journey index
    to ignore if its distance falls below that threshold.
    """
    a = input("Enter a minmum distance: ")

    # Validate that the input can be parsed as a float
    invalid = True
    while invalid:
        try:
            float(a)
            invalid = False  # Input is valid, exit loop
        except ValueError:
            a = input("Enter a float: ")
            invalid = True  # Input was not a valid number, retry

    a = float(a)

    # Exclude any journey shorter than the minimum distance
    for i in range(len(startdate)):
        if tripdist[i] < a:
            ignore.append(i)
    return()


def areavalid(startdate, startstation, endstation):
    """
    Prompts the user for an area name and checks whether it appears in any
    start or end station. Offers a retry if no matches are found.
    Returns the entered area string.
    """
    matching = False
    area = input("Please enter an area: ")
    area = area.replace(" ", "")  # Strip spaces for comparison
    go = ""

    # Search all journeys to see if the area appears in any station name
    for i in range(len(startdate)):
        # Extract the area portion (after the comma) from end station
        end_data = endstation[i].split(",")
        endnew = end_data[1]

        # Extract the area portion (after the comma) from start station
        start_data = startstation[i].split(",")
        new = start_data[1]

        # Normalise both values by stripping spaces and quotes
        endnew = endnew.replace(" ", "").replace('"', "")
        new = new.replace(" ", "").replace('"', "")

        # Check if the input area matches either station area
        if area.upper() == new.upper() or area.upper() == endnew.upper():
            matching = True

    # If no matching area was found, offer the user a chance to retry
    if matching == False:
        print("There were no results found for this area do you wish to retry")
        go = input("Y/N: ")
        while go.upper() != "Y" and go.upper() != "N":
            print("Bad input")
            go = input("There were no results found for this area do you wish to retry (Y/N): ")

    if go.upper() == "Y":
        area = areavalid()  # Recursively retry area input
        return area
    elif go.upper() == "N":
        return area
    return area  # Also returned if a match was found without needing retry


def startareafilter(area, startdate, startstation, ignore):
    """
    Adds the index of any journey to ignore if its start station area
    does not match the target area.
    """
    for i in range(len(startdate)):
        data = startstation[i].split(",")
        new = data[1]  # Extract the area portion after the comma

        # Normalise and compare; exclude journey if start area doesn't match
        if area.upper().replace(" ", "") != new.upper().replace(" ", "").replace('"', ""):
            ignore.append(i)
    return()


def endareafilter(area, startdate, endstation, ignore):
    """
    Adds the index of any journey to ignore if its end station area
    does not match the target area.
    """
    for i in range(len(startdate)):
        data = endstation[i].split(",")
        new = data[1]  # Extract the area portion after the comma

        # Normalise and compare; exclude journey if end area doesn't match
        if area.upper().replace(" ", "") != new.upper().replace(" ", "").replace('"', ""):
            ignore.append(i)
    return()


def suspiciousdatafilter(startdate, suspicious, ignore):
    """
    Adds the index of any journey to ignore if it has been flagged
    as suspicious (i.e. its suspicious field is not "Not").
    """
    for i in range(len(startdate)):
        if suspicious[i] != "Not":
            ignore.append(i)  # Exclude flagged journeys
    return()