def text(word,pos):
    wordlength = len(word)
    if (ord(word[0]) >=65 and ord(word[0])<= 77) or (ord(word[0]) >=97 and ord(word[0])<= 109):
        word = word.upper()
    else:
        word = word.lower()
    while wordlength <10:
        word = word+" "
        wordlength = len(word)
    # | logic
    word = word+"|"
    return word

def real(word,pos):
    word = str(round(float(word),2))
    wordlength = len(word)
    while wordlength <10:
        word = " "+word
        wordlength = len(word)
    # | logic
    word = word+"|"
    return word

def integer(word,pos):
    wordlength = len(word)
    while wordlength<=8:
        new =(" "+word+" ")
        word = new
        wordlength = len(word)
    if wordlength == 9:
        word = " "+word
    # logic to add |
    word = word+"|"
    return word

def checkfloat(word):
    try:
        float(word)
        return True
    except ValueError:
        return False
    
message = ""
f = open("week10_file1.txt")
for line in f:
    if line.strip():
        words = line.split("#")
        length = len(words)
        pos = 0
        for yes in words:
            yes = yes.replace("\n","")
            floating = checkfloat(yes)
            if yes.isnumeric():
                final = integer(yes,pos)
            elif floating == True:
                final = real(yes,pos)
            else:
                final = text(yes,pos)
            pos+=1
            if pos == 6: final = final+"\n"            
            message = message+final

print(message)