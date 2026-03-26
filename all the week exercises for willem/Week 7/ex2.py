results=["linenumber,","a,","e,","i,","o,","u,","\n"]
p=0

f = open("frankenstein.txt")

for line in f:
    if line.strip():
        p+=1
        print(p)
        new = [p,0,0,0,0,0]
        for i in range(len(line)):
            if line[i] =="a":
                new[1]+=1
            elif line[i] =="e":
                new[2]+=1
            elif line[i]=="i":
                new[3]+=1
            elif line[i]=="o":
                new[4]+=1
            elif line[i] == "u":
                new[5]+=1
        for i in range(len(new)):
            message = (str(new[i])+",")
            results.append(message)
        results.append("\n")

#print(results)
f.close()
f = open("results.csv","a")
for i in range(len(results)):
    message = (str(results[i]))
    #print (message)
    f.write(message)
