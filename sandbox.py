import urllib.request
# url="https://sourcebooks.fordham.edu/source/g7-dictpap.asp" # dictatus papae
url='https://www.oldbaileyonline.org/browse.jsp?id=t17800628-33&div=t17800628-33'
start=0
end=100
response = urllib.request.urlopen(url)
# print(type(response)) # print
html = response.read()
print("Type of html variable: " + str(type(html))) # print type of html variable
text = html.lower()
print("Type of text variable: " + str(type(text))) # print type of html variable
print("text variable (portion): " + str(text[start:end])) # print
print(text.decode('utf-8'))
inside = 0
newText = ''

for char in str(text[start:end]):
    if char == '<':
        inside = 1
    elif (inside == 1 and char == '>'):
        inside = 0
    elif inside == 1:
        continue
    else:
        newText += char

print("newText variable (portion): " + str(newText[start:end])) # print
print(type(newText))


'''
# identify type
t=''
print(type(t))

# bites b problem
b = b'1234'
print(type(b))
print(b.decode('utf-8'))  # '1234'
'''