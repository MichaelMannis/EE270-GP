Numbers = [0,1,2]
list2 = ["blue","ryesd","orange","purple"]
list3 = [1,2,5]
list4 = [1,5,2]
list5 = ["purple"]
def func1():
    tot = sum(Numbers)/len(Numbers)
    print(tot)
def func2():
    i=0
    while i <len(list2):
        message = "The index is " + str(i+1)+" and the item is "+str(list2[i])
        print(message)
        i +=1
def func3():
    valid = 0 
    for i in range(len(list2)):
        if list2[i] == "red":
            valid =1
            list2.append("burgandy")
    if valid == 1:
        for i in range(len(list2)):
            message = "The index is " + str(i+1)+" and the item is "+str(list2[i])
            print(message)
    else:
        print("no red")
    

def func4(a,b):
    match = 0
    if len(a) ==len(b):
        for i in range(len(a)):
            for m in range(len(a)):
                if a[i] ==b[m]:
                    match+=1
                    break
    else:
        return False
    if match == len(a):
        return True
    return False
print(str(func4(list3,list4)))
