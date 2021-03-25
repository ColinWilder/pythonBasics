# trial-content.py

import urllib2, obo

url = 'http://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'

# Rebecca Hall's cookbook pages project:
# url = 'http://www.gutenberg.org/cache/epub/6677/pg6677.html'
# <h1 id="id00014" style="margin-top: 7em">
# <p id="id00686">



response = urllib2.urlopen(url)
HTML = response.read()

print(obo.stripTags(HTML))