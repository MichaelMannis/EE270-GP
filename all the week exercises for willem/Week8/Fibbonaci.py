def validate(a):
    try:
        n = int(a)
    except ValueError:
        print("Needs to be an integer")
        return False
    if n>0:
        return True
    print("Needs to be positive")
    return False

def main(n):
    if validate(n):
        seq = [1,1]
        n = int(n)
        b = 2
        while n >b:
            seq.append((seq[b-1]+seq[b-2]))
            b+=1
        print(seq)
    else:
        main(input("Write a number (better this time): "))

#  bootstrap
n = input("write a number: ")
main(n)
print(float("2.3"))
"2.3" ## isnt
2.3 # intable