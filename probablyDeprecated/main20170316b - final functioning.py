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


# new for Thurs. 3/26 # no class on 3/29 because of spring break
# begin with lesson "Keywords in Context (Using n-grams)"; see utilities new function there
# then do throwaway demo file called useGetNGrams
# moving on to lesson "Output Keywords in Context in an HTML File with Python"
# first do throwaway demo file called get-keywords, in two versions

# Next I am going to incorporate _some_ code from html-to-pretty-print.py
# NB cannot use all of html-to-pretty-print.py because we have altered code in this main file and it no longer reflects the PH lessons precisely
n=7
ngrams = utilities.getNGrams(fullwordlist, n)
worddict = utilities.nGramsToKWICDict(ngrams)
print(worddict["black"]) # print KWIC for word "black"

# from codeblock # html-to-kwic.py
# output KWIC and wrap with html
target = 'black'
outstr = '<pre>'
if worddict.has_key(target):
    for k in worddict[target]:
        outstr += utilities.prettyPrintKWIC(k) # changed from obo
        outstr += '<br />'
else:
    outstr += 'Keyword not found in source'

outstr += '</pre>'
utilities.wrapStringInHTMLWindows('html-to-kwic', url, outstr) # changed from obo # also changed wrapStringInHTML to wrapStringInHTMLWindows


