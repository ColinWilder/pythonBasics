# file name: utilities
# author: colin wilder, based on the Programming Historian obo.py
# created Feb 16, 2017
# This file is going to be my collection of tools for the
# Programming Historian lessons for HIST 700. Its complement is the main program. 

def findTrueTranscript(pageContents):
    startLoc = pageContents.find("<p>")
    endLoc = pageContents.rfind("<br/>")

    pageContents = pageContents[startLoc:endLoc]

    inside = 0
    text = ''

    for char in pageContents:
        if char == '<':
            inside = 1
        elif (inside == 1 and char == '>'):
            inside = 0
        elif inside == 1:
            continue
        else:
            text += char
    return text


# Thurs. 2/16/2017 from lesson 'Normalizing Textual Data with Python'
# Given a text string, remove all non-alphanumeric
# characters (using Unicode definition of alphanumeric).
def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)


#for class on Thurs. 2/23/2017 from lesson 'Counting Word Frequencies with Python'
# Given a list of words, return a dictionary of
# word-frequency pairs.
def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(zip(wordlist,wordfreq))


#for class on Thurs. 2/23/2017 from lesson 'Counting Word Frequencies with Python'
# Sort a dictionary of word-frequency pairs in
# order of descending frequency.
def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


#for class on Thurs. 2/23/2017 from lesson 'Counting Word Frequencies with Python'
# Given a list of words, remove any that are
# in a list of stop words.
import stopwordsFile
sw=stopwordsFile.stopwords
def removeStopwords(wordlist, sw):
    return [w for w in wordlist if w not in sw]

# note that the above utilities were prepared for class on 2/23 and we (just barely) finished them that day

# #for class on Thurs. 3/2/17 from lesson "Output data as HTML file"
# # Given a URL, return string of lowercase text from page.
# def webPageToText(url):
#     import urllib2
#     response = urllib2.urlopen(url)
#     html = response.read()
#     text = stripTags(html).lower()
#     return text
# # I think that we are not actually using this one. 

#for class on Thurs. 3/2/17 from lesson "Output data as HTML file"
# Given name of calling program, a url and a string to wrap,
# output string in html body with basic metadata
# and open in Firefox tab.
def wrapStringInHTMLWindows(program, url, body):
    import datetime
    from webbrowser import open_new_tab
    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = program + '.html'
    f = open(filename,'w')
    wrapper = """<html>
    <head>
    <title>%s output - %s</title>
    </head>
    <body><p>URL: <a href=\"%s\">%s</a></p><p>%s</p></body>
    </html>"""
    whole = wrapper % (program, now, url, url, body)
    f.write(whole)
    f.close()
    open_new_tab(filename)

# for class on Thurs. 3/16/17 (no class last week - spring break) from lesson "Keywords in Context (Using n-grams)"
# Given a list of words and a number n, return a list
# of n-grams.
# There are two versions of this, one witha proper for loop and one with a list comprehension. 
def getNGrams(wordlist, n):
    ngrams = []
    for i in range(len(wordlist)-(n-1)):
        ngrams.append(wordlist[i:i+n])
    return ngrams


# for class on Thurs. 3/16/17 from lesson "Output Keywords in Context in an HTML File with Python"
# Given a list of n-grams **identify the index of the keyword.**
# throwaway version 1
def nGramsToKWICDict(ngrams):
    keyindex = len(ngrams[0]) // 2
    return keyindex

# final version 2
# Given a list of n-grams, **return a dictionary of KWICs, indexed by keyword.** NOTE THIS IS DIFFERENT

def nGramsToKWICDict(ngrams):
    keyindex = len(ngrams[0]) // 2
    kwicdict = {}
    for k in ngrams:
        if k[keyindex] not in kwicdict:
            kwicdict[k[keyindex]] = [k]
        else:
            kwicdict[k[keyindex]].append(k)
    return kwicdict


# Given a KWIC, return a string that is formatted for
# pretty printing.

def prettyPrintKWIC(kwic):
    n = len(kwic)
    keyindex = n // 2
    width = 10

    outstring = ' '.join(kwic[:keyindex]).rjust(width*keyindex)
    outstring += str(kwic[keyindex]).center(len(kwic[keyindex])+6)
    outstring += ' '.join(kwic[(keyindex+1):])

    return outstring

