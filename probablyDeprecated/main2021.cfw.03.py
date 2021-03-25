import obo

url="https://sourcebooks.fordham.edu/source/g7-dictpap.asp" # dictatus papae

print("Running main...")
x=obo.webPageToText(url)
print("Type: " + str(type(x)))
print("Printing (part of) string of web page contents: " + x[0:60])
# print(x.decode('utf-8'))