# turn a string into a list of words
# alphabetize the list
# de-duplicate it

string="""
decisio causa summum tribunal regius vismariensis delatus cura Johann_Jacob_von_Ryssel
gehalten reichstag abschied satzung
tractatus commissarius commissio camera imperialis
corpus constitutio imperialis
"""

tokenList=sorted(list(set(string.lower().split())))

for token in tokenList:
    print token

