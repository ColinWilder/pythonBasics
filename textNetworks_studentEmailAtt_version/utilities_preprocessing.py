# -*- coding: utf-8 -*- 
# Subcreated on Sunday Sept.15, 2013, with improvements periodically from 2013 to 2017. 
# @author: Colin F. Wilder
# Intellectual Property statement: This code is based on lots of other freely available code on the internet, especially lessons from the Programming Historian by Adam Crymble and William Turkel. The utilities to make bigrams are, I believe, fairly original to me, though not rocket science anyway.  Therefore I release it to thee, benevolent user, under a CC-BY license i.e. Creative Commons Attribution 2.0 Generic license, which is explained at https://creativecommons.org/licenses/by/2.0/.#
# Explanation of algorithms in this module:
# Below, I define a bunch of functions for preprocessing text. At the end, I wrap them all together in one function, called processTextFile, whose function is to open a text file and return simple, stripped, lowercase etc. text
# This could be improved by de-compartmentalizing - have your Main program call the preprocessing utilities individually. 

import re

def stripTags(textWithPointyBrackets):
    # strip out XML tags
    # CWCID part of this comes from The Programming Historian
    inside=0
    cleanedUpText=''
    for char in textWithPointyBrackets:
        if inside<0: inside=0        
        if char == '<':
            inside += 1
        elif (inside > 0 and char == '>'):
            inside -= 1
            cleanedUpText += " "
        elif inside > 0:
            continue
        else:
            cleanedUpText += char
    return cleanedUpText

def removeNumbers(textString):
    # remove numbers
    numberListString='0123456789'
    for i in range(0,10):
        textString = textString.replace(numberListString[i], '')
    return textString
    # NB returns a string
    
def removePunctuation(text):
    # remove punctuation
    # remove punct before turning text into list of words
    # do not replace apostrophes with white space
    text = text.replace('`', '')
    # replace dashes (-) with whitespace
    text = text.replace('-', ' ')
    # have decided NOT TO REPLACE WITH WHITESPACE
    punctuation2 = [ '\'', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '+', '=', '{', '[', '}', ']', '|', '\\', ';', ':', '"', '<', '.', '>', ',', '?', '/', '’' ]
    # exclusion: '_' # I plan to use this to stich together proper names to be excluded from lemmatizing. 
    for punct in punctuation2:
        text = text.replace(punct, '') # i.e. just delete the space
    return text

def removeExtraWhiteSpace(text):
    # remove any white space longer than a single character
    textList = text.split()
    textString = ' '.join(textList)
    return textString
    # NB returns a string
    
# English stop list
stopList=['a', 'about', 'above', 'across', 'after', 'afterwards', 'again', 'against', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'amoungst', 'amount', 'an', 'and', 'another', 'any', 'anyhow', 'anyone', 'anything', 'anyway', 'anywhere', 'are', 'around', 'as', 'at', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'below', 'beside', 'besides', 'between', 'beyond', 'bill', 'both', 'bottom', 'but', 'by', 'call', 'can', 'cannot', 'cant', 'co', 'computer', 'con', 'could', 'couldnt', 'cry', 'de', 'describe', 'detail', 'do', 'done', 'down', 'due', 'during', 'each', 'eg', 'eight', 'either', 'eleven', 'else', 'elsewhere', 'empty', 'enough', 'etc', 'even', 'ever', 'every', 'everyone', 'everything', 'everywhere', 'except', 'few', 'fifteen', 'fify', 'fill', 'find', 'fire', 'first', 'five', 'for', 'former', 'formerly', 'forty', 'found', 'four', 'from', 'front', 'full', 'further', 'get', 'give', 'go', 'had', 'has', 'hasnt', 'have', 'he', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herse\x94', 'him', 'himse\x94', 'his', 'how', 'however', 'hundred', 'i', 'ie', 'if', 'in', 'inc', 'indeed', 'interest', 'into', 'is', 'it', 'its', 'itse\x94', 'keep', 'last', 'latter', 'latterly', 'least', 'less', 'ltd', 'made', 'many', 'may', 'me', 'meanwhile', 'might', 'mill', 'mine', 'more', 'moreover', 'most', 'mostly', 'move', 'mr', 'mrs', 'much', 'must', 'my', 'myse\x94', 'name', 'namely', 'neither', 'never', 'nevertheless', 'next', 'nine', 'no', 'nobody', 'none', 'noone', 'nor', 'not', 'nothing', 'now', 'nowhere', 'of', 'off', 'often', 'on', 'once', 'one', 'only', 'onto', 'or', 'other', 'others', 'otherwise', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'part', 'per', 'perhaps', 'please', 'put', 'rather', 'same', 'see', 'seem', 'seemed', 'seeming', 'seems', 'serious', 'several', 'she', 'should', 'show', 'side', 'since', 'sincere', 'six', 'sixty', 'so', 'some', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhere', 'still', 'such', 'system', 'take', 'ten', 'than', 'that', 'the', 'their', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'therefore', 'therein', 'thereupon', 'these', 'they', 'thick', 'thin', 'third', 'this', 'those', 'though', 'three', 'through', 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'top', 'toward', 'towards', 'twelve', 'twenty', 'two', 'un', 'under', 'until', 'up', 'upon', 'us', 'very', 'via', 'was', 'we', 'well', 'were', 'what', 'whatever', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'with', 'within', 'without', 'would', 'yet', 'you', 'your', 'yours', 'yourself', 'yourselves']

# French stop list
frenchStopList=['la', 'le', 'les', 'au', 'aux']
# other stuff to be added later: a, amp, au, auec, aussi, autre, autres, aux, bien, car, ce, ces, cette, ceux, chose, choses, comme, d', dans, de, des, deux, dire, dont, du, elle, elles, en, encore, est, estre, et, faire, fait, faut, force, grande, ie, il, ils, l', la, le, les, leur, leurs, lors, luy, mais, mesme, n', ne, nous, on, ont, or, ou, par, parce, pas, peut, plus, plusieurs, point, pour, pourquoy, puis, qu', quand, que, qui, quoy, sa, sans, se, ses, si, soit, son, sont, sur, tous, tout, toutes, vn, vne, y

# Latin stop list
latinStopList=['ab', 'ac', 'ad', 'adhic', 'aliarum', 'aliqui', 'aliquis', 'aliquot', 'an', 'ante', 'apud', 'at', 'atque', 'aut', 'autem', 'cui', 'cum', 'cur', 'de', 'decem', 'deinde', 'demum', 'de\xc3\x9f', 'dum', 'ea', 'eae', 'eam', 'earum', 'eas', 'ego', 'ei', 'eis', 'eius', 'eiusdem', 'enim', 'eo', 'eorum', 'eorundem', 'eos', 'ergo', 'es', 'est', 'et', 'etiam', 'etsi', 'eum', 'ex', 'ff', 'fio', 'hac', 'hactenus', 'haud', 'hi', 'hic', 'iam', 'ibid', 'id', 'idem', 'igitur', 'ii', 'ille', 'in', 'infra', 'inter', 'interim', 'ipse', 'is', 'ita', 'item', 'iu', 'la', 'magis', 'me', 'mei', 'mihi', 'modo', 'mox', 'nam', 'ne', 'nec', 'necque', 'neque', 'nisi', 'nobis', 'non', 'nos', 'nostri', 'o', 'ob', 'per', 'possum', 'post', 'pro', 'qua', 'quae', 'quam', 'quare', 'quator', 'que', 'quelques', 'qui1', 'qui', 'quia', 'quibus', 'quicumque', 'quidem', 'quilibet', 'quinque', 'quis', 'quisnam', 'quisquam', 'quisque', 'quisquis', 'quo', 'quoniam', 'quotquot', 'sed', 'si', 'sic', 'siue', 'sive', 'suae', 'sua', 'suum', 'sub', 'sui', 'sum', 'sum1', 'sunt', 'super', 'suus', 'tam', 'tamen', 'te', 'tibi', 'trans', 'trias', 'tu', 'tui', 'tum', 'ubi', 'ue', 'uel', 'uero', 'uestri', 'uii', 'unus', 'unà', 'una', 'uo', 'uobis', 'uos', 'usq', 'ut', 'xii'] # oddly I had to make part of this myself # because I found that the stop lists on the web including the ones at Perseus (at Tufts) lacked about half of the forms of is (e.g. eius, if memory serves). 


# German stop list
germanStopList=['a', 'ab', 'aber', 'ach', 'achte', 'achten', 'achter', 'achtes', 'ag', 'alle', 'allein', 'allem', 'allen', 'aller', 'allerdings', 'alles', 'allgemeinen', 'als', 'also', 'am', 'an', 'ander', 'andere', 'anderem', 'anderen', 'anderer', 'anderes', 'anderm', 'andern', 'anderr', 'anders', 'au', 'auch', 'auf', 'aus', 'ausser', 'ausserdem', 'außer', 'außerdem', 'b', 'bald', 'bei', 'beide', 'beiden', 'beim', 'beispiel', 'bekannt', 'bereits', 'besonders', 'besser', 'besten', 'bin', 'bis', 'bisher', 'bist', 'c', 'd', 'd.h', 'da', 'dabei', 'dadurch', 'dafür', 'dagegen', 'daher', 'dahin', 'dahinter', 'damals', 'damit', 'danach', 'daneben', 'dank', 'dann', 'daran', 'darauf', 'daraus', 'darf', 'darfst', 'darin', 'darum', 'darunter', 'darüber', 'das', 'dasein', 'daselbst', 'dass', 'dasselbe', 'davon', 'davor', 'dazu', 'dazwischen', 'daß', 'dein', 'deine', 'deinem', 'deinen', 'deiner', 'deines', 'dem', 'dementsprechend', 'demgegenüber', 'demgemäss', 'demgemäß', 'demselben', 'demzufolge', 'den', 'denen', 'denn', 'denselben', 'der', 'deren', 'derer', 'derjenige', 'derjenigen', 'dermassen', 'dermaßen', 'derselbe', 'derselben', 'des', 'deshalb', 'desselben', 'dessen', 'deswegen', 'dich', 'die', 'diejenige', 'diejenigen', 'dies', 'diese', 'dieselbe', 'dieselben', 'diesem', 'diesen', 'dieser', 'dieses', 'dir', 'doch', 'dort', 'drei', 'drin', 'dritte', 'dritten', 'dritter', 'drittes', 'du', 'durch', 'durchaus', 'durfte', 'durften', 'dürfen', 'dürft', 'e', 'eben', 'ebenso', 'ehrlich', 'ei', 'ei,', 'eigen', 'eigene', 'eigenen', 'eigener', 'eigenes', 'ein', 'einander', 'eine', 'einem', 'einen', 'einer', 'eines', 'einig', 'einige', 'einigem', 'einigen', 'einiger', 'einiges', 'einmal', 'eins', 'elf', 'en', 'ende', 'endlich', 'entweder', 'er', 'ernst', 'erst', 'erste', 'ersten', 'erster', 'erstes', 'es', 'etwa', 'etwas', 'euch', 'euer', 'eure', 'eurem', 'euren', 'eurer', 'eures', 'f', 'folgende', 'früher', 'fünf', 'fünfte', 'fünften', 'fünfter', 'fünftes', 'für', 'g', 'gab', 'ganz', 'ganze', 'ganzen', 'ganzer', 'ganzes', 'gar', 'gedurft', 'gegen', 'gegenüber', 'gehabt', 'gehen', 'geht', 'gekannt', 'gekonnt', 'gemacht', 'gemocht', 'gemusst', 'genug', 'gerade', 'gern', 'gesagt', 'geschweige', 'gewesen', 'gewollt', 'geworden', 'gibt', 'ging', 'gleich', 'gott', 'gross', 'grosse', 'grossen', 'grosser', 'grosses', 'groß', 'große', 'großen', 'großer', 'großes', 'gut', 'gute', 'guter', 'gutes', 'h', 'hab', 'habe', 'haben', 'habt', 'hast', 'hat', 'hatte', 'hatten', 'hattest', 'hattet', 'heisst', 'her', 'heute', 'hier', 'hin', 'hinter', 'hoch', 'hätte', 'hätten', 'i', 'ich', 'ihm', 'ihn', 'ihnen', 'ihr', 'ihre', 'ihrem', 'ihren', 'ihrer', 'ihres', 'im', 'immer', 'in', 'indem', 'infolgedessen', 'ins', 'irgend', 'ist', 'j', 'ja', 'jahr', 'jahre', 'jahren', 'je', 'jede', 'jedem', 'jeden', 'jeder', 'jedermann', 'jedermanns', 'jedes', 'jedoch', 'jemand', 'jemandem', 'jemanden', 'jene', 'jenem', 'jenen', 'jener', 'jenes', 'jetzt', 'k', 'kam', 'kann', 'kannst', 'kaum', 'kein', 'keine', 'keinem', 'keinen', 'keiner', 'keines', 'kleine', 'kleinen', 'kleiner', 'kleines', 'kommen', 'kommt', 'konnte', 'konnten', 'kurz', 'können', 'könnt', 'könnte', 'l', 'lang', 'lange', 'leicht', 'leide', 'lieber', 'los', 'm', 'machen', 'mag', 'magst', 'mahn', 'mal', 'man', 'manche', 'manchem', 'manchen', 'mancher', 'manches', 'mehr', 'mein', 'meine', 'meinem', 'meinen', 'meiner', 'meines', 'mensch', 'menschen', 'mich', 'mir', 'mit', 'mittel', 'mochte', 'mochten', 'morgen', 'muss', 'musst', 'musste', 'mussten', 'muß', 'mußt', 'möchte', 'mögen', 'möglich', 'mögt', 'müssen', 'müsst', 'müßt', 'n', 'na', 'nach', 'nachdem', 'nahm', 'natürlich', 'neben', 'nein', 'neue', 'neuen', 'neun', 'neunte', 'neunten', 'neunter', 'neuntes', 'nicht', 'nichts', 'nie', 'niemand', 'niemandem', 'niemanden', 'noch', 'nun', 'nur', 'o', 'ob', 'oben', 'oder', 'offen', 'oft', 'ohne', 'p', 'q', 'r', 'rechter', 'richtig', 'rund', 's', 'sa', 'sagt', 'sagte', 'sah', 'satt', 'schlecht', 'schon', 'sechs', 'sechste', 'sechsten', 'sechster', 'sechstes', 'sehr', 'sei', 'seid', 'seien', 'sein', 'seine', 'seinem', 'seinen', 'seiner', 'seines', 'seit', 'seitdem', 'selbst', 'sich', 'sie', 'sieben', 'siebente', 'siebenten', 'siebenter', 'siebentes', 'sind', 'so', 'solang', 'solche', 'solchem', 'solchen', 'solcher', 'solches', 'soll', 'sollen', 'sollst', 'sollt', 'sollte', 'sollten', 'sondern', 'sonst', 'soweit', 'sowie', 'später', 'startseite', 'statt', 'steht', 'suche', 't', 'tel', 'tritt', 'trotzdem', 'tun', 'u', 'uhr', 'um', 'und', 'und?', 'uns', 'unse', 'unsem', 'unsen', 'unser', 'unsere', 'unserer', 'unses', 'unter', 'v', 'vergangenen', 'viel', 'viele', 'vielem', 'vielen', 'vielleicht', 'vier', 'vierte', 'vierten', 'vierter', 'viertes', 'vom', 'von', 'vor', 'w', 'wahr?', 'wann', 'war', 'waren', 'warst', 'wart', 'warum', 'was', 'weg', 'wegen', 'weil', 'weit', 'weiter', 'weitere', 'weiteren', 'weiteres', 'welche', 'welchem', 'welchen', 'welcher', 'welches', 'wem', 'wen', 'wenig', 'wenige', 'weniger', 'weniges', 'wenigstens', 'wenn', 'wer', 'werde', 'werden', 'werdet', 'weshalb', 'wessen', 'wie', 'wieder', 'wieso', 'will', 'willst', 'wir', 'wird', 'wirklich', 'wirst', 'wissen', 'wo', 'woher', 'wohin', 'wohl', 'wollen', 'wollt', 'wollte', 'wollten', 'worden', 'wurde', 'wurden', 'während', 'währenddem', 'währenddessen', 'wäre', 'würde', 'würden', 'x', 'y', 'z', 'z.b', 'zehn', 'zehnter', 'zehntes', 'zeit', 'zu', 'zuerst', 'zugleich', 'zum', 'zunächst', 'zur', 'zurück', 'zusammen', 'zwanzig', 'zwar', 'zwei', 'zweite', 'zweiten', 'zweiter', 'zweites', 'zwischen', 'zwölf', 'über', 'überhaupt', 'übrigen']

def removeStopWords(textString):
    # remove stop words
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if word in stopList: # requires stop list, which is given just above
            continue
        else:
            TextListNew.append(word)
            textString = ' '.join(TextListNew)
    return textString
    # NB returns a string

def removeStopWordsFromSpecialList(textString,stopWordList=stopList):
    # remove stop words
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if word in stopWordList:
            continue
        else:
            TextListNew.append(word)
            textString = ' '.join(TextListNew)
    return textString
    # NB returns a string


def removeSingletons(textString):
    # remove strings in text that are single letters, aside from i and a
    textList = textString.split()
    TextListNew=[]
    for word in textList:
        if len(word)<2 and word.lower() != "i" and word.lower() != "a":
            continue
        else:
            TextListNew.append(word)
    textString = ' '.join(TextListNew)
    return textString
    # NB returns a string

# do some of the above functions
def processTextFile(file):
    # open the file
    TextFile = open(file)
    # turn file into a string
    Text=TextFile.read()
    # make everything lower case
    Text=Text.lower()
    # strip tags
    Text=stripTags(Text)
    # remove punctuation here
    Text=removePunctuation(Text)
    # remove stop words    
    Text=removeStopWords(Text)
    return Text

