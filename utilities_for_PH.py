# utilities for PH Python lessons
# for HIST Dig Hist class, Spring 2021
# not actually copyright Colin Wilder
# this is mostly based on the PH's obo.py file

# stripTags
# Isolates a certain chunk of central HTML between two given tags.
# Removes all tags. 
def stripTags(pageContents):
    pageContents = str(pageContents)
    startLoc = pageContents.find("<p>") # varies by webpage!
    endLoc = pageContents.rfind("<br/>") # varies by webpage!
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


# stripNonAlphaNum
# Given a text string, remove all non-alphanumeric characters (using Unicode definition of alphanumeric).
# see https://programminghistorian.org/en/lessons/normalizing-data
def stripNonAlphaNum(text):
    import re
    return re.compile(r'\W+', re.UNICODE).split(text)


# wordListToFreqDict
# Given a list of words, return a dictionary of word-frequency pairs.
# see https://programminghistorian.org/en/lessons/counting-frequencies
def wordListToFreqDict(wordlist):
    wordfreq = [wordlist.count(p) for p in wordlist]
    return dict(list(zip(wordlist,wordfreq)))


# sortFreqDict
# Sort a dictionary of word-frequency pairs in order of descending frequency.
# see https://programminghistorian.org/en/lessons/counting-frequencies
def sortFreqDict(freqdict):
    aux = [(freqdict[key], key) for key in freqdict]
    aux.sort()
    aux.reverse()
    return aux


# removeStopwords
# https://programminghistorian.org/en/lessons/counting-frequencies # but the function is different in that
# Given a list of words, remove any that are in a list of stop words.
def removeStopwords(wordlist):
    import stopwordsFile # note this is unusual; we could alternatively just do the import at the top of the file
    sw=stopwordsFile.stopwords
    return [w for w in wordlist if w not in sw]


# wrapStringInHTMLWindows
# Given name of calling program, a url and a string to wrap, output string in html body with basic metadata and open in Firefox tab.
# https://programminghistorian.org/en/lessons/output-data-as-html-file
def wrapStringInHTMLWindows(program, url, body): ### These are the PC instructions !! #############
    import datetime
    from webbrowser import open_new_tab
    now = datetime.datetime.today().strftime("%Y%m%d-%H%M%S")
    filename = program + '.html'
    f = open(filename,'w') # not wb?
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



###################################################
########## final, KWIC-related utilities ##########
###################################################

# from lesson "Keywords in Context (Using n-grams)"
# Given a list of words and a number n, return a list of n-grams.
# There are two versions of this, one with a proper for loop and one with a list comprehension. 
def getNGrams(wordlist, n):
    ngrams = []
    for i in range(len(wordlist)-(n-1)):
        ngrams.append(wordlist[i:i+n])
    return ngrams

# from lesson "Output Keywords in Context in an HTML File with Python"
# Given a list of n-grams, return a dictionary of KWICs, indexed by keyword. 
def nGramsToKWICDict(ngrams):
    keyindex = len(ngrams[0]) // 2
    kwicdict = {}
    for k in ngrams:
        if k[keyindex] not in kwicdict:
            kwicdict[k[keyindex]] = [k]
        else:
            kwicdict[k[keyindex]].append(k)
    return kwicdict

# from lesson "Output Keywords in Context in an HTML File with Python"
# Given a KWIC, return a string that is formatted for pretty printing.
def prettyPrintKWIC(kwic):
    n = len(kwic)
    keyindex = n // 2
    width = 10

    outstring = ' '.join(kwic[:keyindex]).rjust(width*keyindex)
    outstring += str(kwic[keyindex]).center(len(kwic[keyindex])+6)
    outstring += ' '.join(kwic[(keyindex+1):])

    return outstring
