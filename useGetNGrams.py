# useGetNGrams.py

# What does this program do? 

import obo

wordstring = 'it was the best of times it was the worst of times '
wordstring += 'it was the age of wisdom it was the age of foolishness'
allMyWords = wordstring.split()

print(obo.getNGrams(allMyWords, 7))

# It just does a simple demonstration of making KWIC. 