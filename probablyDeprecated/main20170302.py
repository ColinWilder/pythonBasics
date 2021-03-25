# file name: main
# author: colin wilder, based on a few modules from the Programming Historian
# created Feb 16, 2017
# This file is going to be the main execution program for the Programming
# Historian lessons for HIST 700. It mostly uses the utilities module. 

# import modules we need
import urllib2, utilities

# go out and get text of web page
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
response = urllib2.urlopen(url)
html = response.read()

#pare down text to just the transcript part
text = utilities.findTrueTranscript(html).lower()

# turn the text from string into a list
fullwordlist = utilities.stripNonAlphaNum(text)

# remove stopwords
wordlist = utilities.removeStopwords(fullwordlist, utilities.sw)

# make and sort frequency dictionary
dictionary = utilities.wordListToFreqDict(wordlist)
sorteddict = utilities.sortFreqDict(dictionary)

# print it to the output to see what it looks like
#for s in sorteddict: print(str(s))
# this was in 2/23 but removed for 3/2

# new for Thurs. 3/2
# compile dictionary into string and wrap with HTML
outstring = ""
for s in sorteddict:
    outstring += str(s)
    outstring += "<br />"
utilities.wrapStringInHTMLWindows("html-to-freq-3", url, outstring)
