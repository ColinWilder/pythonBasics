# practice using the stripTags function

import obo

myText = "This is my <p>HTMdadasdasdasd <madeUpTag> transcirpt about B<br/> message"
print(myText)

theResult = obo.stripTags(myText)

print(theResult)

# distinguishing between single and double quotation marks

v = '<a href="http://www.sheffield.ac.uk/hri/">'

