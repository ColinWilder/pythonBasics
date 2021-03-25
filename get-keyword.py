#get-keyword.py
# throwaway demo file

import utilities_for_PH # changed from obo

test = 'this test sentence has eight words in it'

ngrams = utilities_for_PH.getNGrams(test.split(), 5) # changed from obo

print(utilities_for_PH.nGramsToKWICDict(ngrams)) # changed from obo