import urllib.request, urllib.error, urllib.parse, utilities_for_PH

urls = ["https://sourcebooks.fordham.edu/ancient/cicero-republic1.asp",
        "https://sourcebooks.fordham.edu/ancient/cicero-laws1.asp",
        "http://web.archive.org/web/20021002004103/http://www.princeton.edu/~champlin/cla218/polybi.htm",
        "https://sourcebooks.fordham.edu/ancient/54candidate.asp",
        "http://www.csun.edu/~hcfll004/12tables.html"]

for u in urls:
    print(u)
    response = urllib.request.urlopen(u)
    HTML = response.read()
    HTML=HTML.decode('utf-8')
    primarySourceTextItself = utilities_for_PH.stripTags(HTML)
    fullWordList = utilities_for_PH.stripNonAlphaNum(primarySourceTextItself.lower())
    wordList = utilities_for_PH.removeStopwords(fullWordList)
    dictionary = utilities_for_PH.wordListToFreqDict(wordList)
    sortedDict = utilities_for_PH.sortFreqDict(dictionary)
    outstring = ""
    for s in sortedDict:
        outstring += str(s)
        outstring += "<br />"
    utilities_for_PH.wrapStringInHTMLWindows ("sorted word-type frequency dictionary", u, outstring)