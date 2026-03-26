n = input("write a number: ")
seq = [1,1]
n = int(n)
b = 2 
while n >b:
    seq.append((seq[b-1]+seq[b-2]))
    b+=1
print(seq)

"""
ASSUME INPUT VALID


Define muteable array with values [1,1]
Ask user for integer input
Loop for value of user input
    Calculate new value with previous 2 values
    Append new value to array
Exit loop
Print array
"""