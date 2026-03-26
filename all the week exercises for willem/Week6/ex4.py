english_to_french = {
    'dog' : 'chien',
    'snake' : 'serpent',
    'goldfish' : 'poisson rouge',
    'towel' : 'serviette',
    'banana' : 'banane',
    'chicken' : 'poulet',
    'potato' : 'pomme de terre',
    'cow' : 'vache',
    'cake' : 'gâteau'
    }

fr = input("Enter french: ")
for eng, word in english_to_french.items():
    if fr == word:
        print(eng)
# adding copies of data is invalid in dictionaries and therefore would override the towel line :    poi