#html-to-list1.py
import urllib2, obo

url = 'http://www.oldbaileyonline.org/print.jsp?div=t17800628-33'

response = urllib2.urlopen(url)
html = response.read()
text = obo.stripTags(html).lower() # here is the new change we are making today
#wordlist = text.split() # old version from Fri 11/9
wordlist = obo.stripNonAlphaNum(text)

# the new version will be:
# wordlist = obo.stripNonAlphaNum(text)


print(wordlist[0:120]) # old version

# print(wordlist) # new version