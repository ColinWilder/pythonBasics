import utilities

text1 = 'hel&lo wo%%r*ld'
print(utilities.stripNonAlphaNum(text1))

text2 = 'hello <heres some annoying XML tag> world'
print(utilities.stripNonAlphaNum(text2))

text3 = 'hello #$%^$*%(@ world'
print(utilities.stripNonAlphaNum(text3))