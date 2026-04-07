import operator
wd = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
def filterhandle(startdate,startday,ignore,startstation,endstation,tripdist,suspicious):
    repeat = True
    area = ""
    while repeat:
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
        while selection != "1" and selection != "2" and selection != "3" and selection !="4" and selection != "5" and selection !="6": # worst input validation ive ever done
            selection = input("Bad input enter a number 1-5: ")
        if selection =="1":
            dayfilter(startdate,startday,ignore)
        elif selection =="2":
            bigdistfilter(startdate,tripdist,ignore)
        elif selection =="3":
            area = areavalid(startdate,startstation,endstation)
            startareafilter(area,startdate,startstation,ignore)
        elif selection == "4":
            area = areavalid(startdate,startstation,endstation)
            endareafilter(area,startdate,endstation,ignore)
        elif selection =="5":
            suspiciousdatafilter(startdate,suspicious,ignore)
        elif selection =="6":
            return()
        go = input("Would you like to add another filter? (Y/N):")
        while go.upper()!="Y" and go.upper()!="N":
            print("Bad input")
            go = input("Would you like to add another filter? (Y/N):")
        if go.upper() == "Y":
            repeat = True
        else: repeat = False
    return()

def dayfilter(startdate,startday,ignore):
    day = dayinputvalidation()
    for i in range (len(startdate)):
        if startday[i] != day:
            ignore.append(i)
    return()
def dayinputvalidation():
    targetday = input("which day of the week are you interested in?: ")
    goodinput = False
    for i in range(7):
        if targetday.upper()==wd[i].upper(): #.upper to ignore capitalisation
            goodinput = True
            targetday = wd[i] # use this to ignore capitalisation in future
    if goodinput:
        return targetday
    else:
        print("Bad input please enter a day of the week: ")
        targetday = dayinputvalidation()
        return targetday

def bigdistfilter(startdate,tripdist,ignore):
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
    for i in range(len(startdate)):
        if tripdist[i]<a:
            ignore.append(i)
    return()

def areavalid(startdate,startstation,endstation):
    matching = False
    area = input("Please enter an area: ")
    area = area.replace(" ","")
    go = ""
    for i in range(len(startdate)):
        end_data = endstation[i].split(",")
        endnew = end_data[1]
        start_data = startstation[i].split(",")
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
    

def startareafilter(area,startdate,startstation,ignore):
    for i in range(len(startdate)):
        data = startstation[i].split(",")
        new = data[1] # gets the bit after the comma
        if area.upper().replace(" ","") != new.upper().replace(" ","").replace('"',""):#remove spaces and "
            ignore.append(i)
    return()


def endareafilter(area,startdate,endstation,ignore):

    for i in range(len(startdate)):
        data = endstation[i].split(",")
        new = data[1] # gets the bit after the comma
        if area.upper().replace(" ","") != new.upper().replace(" ","").replace('"',""):#remove spaces and "
            ignore.append(i)
    return()

        

def suspiciousdatafilter(startdate,suspicious,ignore):
    for i in range(len(startdate)):
        if suspicious[i] !="Not":
            ignore.append(i)
    return()
