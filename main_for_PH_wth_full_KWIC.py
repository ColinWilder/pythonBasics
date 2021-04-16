# main file
# a main file is basically where the major commands are. this file will import and call on others. the real action is here, you might say.
# this file is a compilation of all commands from save-webpage, string-to-list, count-list-items-1, html-to-freq, html-to-freq2, open-webpage, trial-content, html-to-list1, and html-to-freq3, in other words, basically all stuff *other than* the definitions of functions (which are rather in the utilities_for_PH.py file).

# foundations
import urllib.request, urllib.error, urllib.parse, utilities_for_PH
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

# get info and read from internet
response = urllib.request.urlopen(url)
HTML = response.read()

# checking type and test prints to make sure everything is OK
# print(type(HTML))
# print(HTML[0:500]) # prints ugly stuff in command output
# print(HTML.decode('utf-8')[0:500]) # prints pretty in command output

# open a new empty file and write the full, original HTML to it
# f = open('obo-t17800628-33.html', 'wb')
# f.write(HTML) # the write method needs a bytes object, not string
# f.close

# open a new empty file and write the full, original HTML to it
f = open('obo-t17800628-33.html', 'wb') # note difference between w and wb
f.write(HTML) # this is writing the full HTML, incl all tags
f.close

# strip out tags
HTML=HTML.decode('utf-8') # gets rid of r/n/ ugliness so that command output will be readable by a human!
primarySourceTextItself = utilities_for_PH.stripTags(HTML)
# print(primarySourceTextItself[0:400])
# print(type(primarySourceTextItself))

# note it is at this point that PH introduces a "bundle... of the code", namely the webPageToText function. See https://programminghistorian.org/en/lessons/output-data-as-html-file. I'm going to ignore and not use that function. I prefer to see everything written out and explained with comments, line by line. 

# strip all non-alphanumeric characters
fullWordList = utilities_for_PH.stripNonAlphaNum(primarySourceTextItself)
# print(wordList[0:100])

# remove stop words
wordList = utilities_for_PH.removeStopwords(fullWordList)

# count words (types), put counts into a dictionary, and sort
dictionary = utilities_for_PH.wordListToFreqDict(wordList)
sortedDict = utilities_for_PH.sortFreqDict(dictionary)

# produce an output file (.html) of the word-type frequency dictionary
outstring = ""
for s in sortedDict:
    outstring += str(s) # write each dictionary entry
    outstring += "<br />" # adding a line break
utilities_for_PH.wrapStringInHTMLWindows ("word-type-frequency-dictionary", url, outstring)

# TO DO: write the word-type frequency dictionary out as a .csv as well, for easy subsequent analysis, graphing, etc. Keep in mind though that Voyant does this pretty well already and I believe has an export feature, so this is really not something you need to do yourself here. 

# create dictionary of n-grams for KWIC output
lengthOfKWICS = 13 # so they will be 13-grams!! that is, lists of 13 words, at the central position of which is the keyword itself
ngrams = utilities_for_PH.getNGrams(fullWordList, lengthOfKWICS) # note we're using the full word list - so it does *not* remove stop words. in this case that is good since we want to see the full sentences in the KWIC printout we're going to make. 
worddict = utilities_for_PH.nGramsToKWICDict(ngrams)

'''
# make a KWIC output using the hardcoded KW "black", then wrap with HTML and open in browser
# This is the functionality shown in PH.
target = 'black'
outstr = '<pre>'
if target in worddict:
    for k in worddict[target]:
        #print(k)
        outstr += utilities_for_PH.prettyPrintKWIC(k)
        outstr += '<br />'
else:
    outstr += 'Keyword not found in source'

outstr += '</pre>'
utilities_for_PH.wrapStringInHTMLWindows('html-to-kwic', url, outstr)
'''

# look for each KW in a list of KWs then wrap them in HTML and open
# TO DO: have the targeted keywords be put into a config file by student/user, rather than hardcoded here. 
targetListOfKeywords = ['black', 'house', 'evil', 'good', 'man', 'prisoner', 'lady']
for item in targetListOfKeywords:
    print(item)
    outstr = '<pre>'
    if item in worddict:
        for k in worddict[item]:
            # print(k)
            outstr += utilities_for_PH.prettyPrintKWIC(k)
            outstr += '<br />'
    else:
        outstr += 'Keyword not found in source'
    outstr += '</pre>'
    # print(outstr)
    utilities_for_PH.wrapStringInHTMLWindows(item, url, outstr)
