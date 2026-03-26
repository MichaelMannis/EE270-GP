def checkfloat(new):
    try:
        float(new)
        return True
    except ValueError:
        return False

def checkint(new):
    try:
        int(new)
        return True
    except ValueError:
        return(checkfloat(new))

def linearsearch(arr):
    if len(arr) == 0:
        message = "array length 0 no values contained."
        return message
    large = arr[0]
    pos = 0
    for i in range (len(arr)): #len arr is a redunancy i think
        if arr[i]> large:
            pos = i
            large = arr[i]
    message = ("largest value is "+str(large)+" at position "+str(pos+1)) # in human numbers
    return message

def first():
    a = []
    go = True
    while go:
        new = input("Enter number or end: ")
        if new == "end":
            go = False
        elif checkint(new)==True:
            a.append(float(new))
        else:
            print("Input invalid. try again \n")
    message = linearsearch(a)
    print(message)

first()