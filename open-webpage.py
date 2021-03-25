# open-webpage.py

import urllib2

#url = 'https://www.gutenberg.org/cache/epub/10657/pg10657.txt' # Caesar, Gallic Wars
url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33' # Old Bailey Online - the Bowsey trial
#url = 'https://sourcebooks.fordham.edu/source/columbus1.asp' # Columbus

response = urllib2.urlopen(url)
webContent = response.read()
print(webContent[0:300])
