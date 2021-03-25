# html-to-freq-3.py

import obo

# create sorted dictionary of word-frequency pairs
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
text = obo.webPageToText(url)
fullwordlist = obo.stripNonAlphaNum(text)
wordlist = obo.removeStopwords(fullwordlist, obo.stopwords)
dictionary = obo.wordListToFreqDict(wordlist)
sorteddict = obo.sortFreqDict(dictionary)

# compile dictionary into string and wrap with HTML
outstring = ""
for s in sorteddict:
    outstring += str(s)
    outstring += "<br />"
obo.wrapStringInHTMLWindows("html-to-freq-3", url, outstring) # note that the method name varies for Mac and PC #########

# When you run this, nothing should appear in the output/console window pane below.  Look at your browser (!!) instead...

