# string-to-list.py

# First, define some strings
s1 = 'hello world'
s2 = 'howdy world'

# list of characters
charlist = []
for char in s1:
    charlist.append(char)
print(charlist)

# illustration of how the split method works
wordlist = s2.split()
print(wordlist)
