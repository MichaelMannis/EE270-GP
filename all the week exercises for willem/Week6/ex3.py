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
new = dict(sorted(english_to_french.items()))

for key, value in new.items():
    print ("english-> "+ key+ " French-> "+ value)
