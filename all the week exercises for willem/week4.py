import math
def func1(a,x):
    if x<0:
        return(0)
    else:
        temp = a*math.exp(-a*x)
        return(temp)
    
def NOT(b):
    return(not(b))
def AND(b,c):
    return(bool(b*c))
def OR(b,c):
    return(b+c)
def XOR(b,c):
    return(b^c)
def NAND(b,c):
    return(not(AND(b,c)))
def NOR(b,c):
    return(not(OR(b,c)))
#
# 

def third(x,y):
    next = 1/3 *(2*x+ y/(x**2))
    return(next)
def fourth(x,z):
    next = 1/4 *(3*x+ z/(x**3))
    return(next)
def main(a):
    y= int(a)
    e3 = y
    e4 = y
    new3 = third(e3,y)
    
    if y>0:
        new4 = fourth(e4,y)
        for i in range(100):
        #print("Iteration "+str(i+1))
        #print("Estimate: "+str(new)+" Difference: " +str(new-est)+ " ")
            if ((abs(new3-e3))<=thresh)+((abs(new4-e4))<=thresh):
                return
            e3 = new3
            e4 = new4
            new3 = third(e3,y)
            new4 = fourth(e4,y)
            print("current number is "+str(y)+" and the third root estimate is "+str(e3))
            print("current number is "+str(y)+" and the fourth root estimate is "+str(e4))
    else:
        print("Fourth Invalid can't be negative")
        for i in range(100):
        #print("Iteration "+str(i+1))
        #print("Estimate: "+str(new)+" Difference: " +str(new-est)+ " ")
            if ((abs(new3-e3))<=thresh):
                return
            e3 = new3
            new3 = third(e3,y)
            print("current number is "+str(y)+" and the third root estimate is "+str(e3))

thresh = 0.001
main(int(input("What number: ")))
#print(func1(3,0))
#print(AND(True,True))