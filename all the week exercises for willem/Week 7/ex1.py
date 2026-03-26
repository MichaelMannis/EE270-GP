results= {
    ">10":0,
    "10-1000":0,
    "1000+":0
}

f = open("frankenstein.txt")

for line in f:
    if line.strip():
        new = line.split(" ")
        length = len(new)
        if length <10:
            results[">10"]+=1
        elif length <1000:
            results["10-1000"]+=1
        elif length >=1000:
            results["1000+"]+=1
        else:
            print("broke :(")

for key, value in results.items():
    print(key)
    print(str(value))