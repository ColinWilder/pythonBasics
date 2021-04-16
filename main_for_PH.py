# main file
# a main file is basically where the major commands are. this file will import and call on others. the real action is here, you might say.
# this file is a compilation of all commands from save-webpage, string-to-list, count-list-items-1, html-to-freq, html-to-freq2, open-webpage, trial-content, html-to-list1, and html-to-freq3, in other words, basically all stuff *other than* the definitions of functions (which are rather in the utilities_for_PH.py file).

# foundations
import urllib.request, urllib.error, urllib.parse, utilities_for_PH
# url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
# url = 'https://tile.loc.gov/storage-services/service/rbc/rbnawsa/n4439/n4439.xml'
# url = 'https://sourcebooks.fordham.edu/mod/1914Pankhurst.asp'
url = 'https://archive.org/stream/revolution-1868-02-26/1868-02-26_djvu.txt'

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

# compile dictionary into string and wrap with an HTML
# https://programminghistorian.org/en/lessons/output-data-as-html-file
outstring = ""
for s in sortedDict:
    outstring += str(s) # write each dictionary entry
    outstring += "<br />" # adding a line break
utilities_for_PH.wrapStringInHTMLWindows ("sorted word-type frequency dictionary", url, outstring)