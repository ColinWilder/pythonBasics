import pypandoc
# output = pypandoc.convert_file('somefile.md', 'rst')
# print(output)

output = pypandoc.convert_file('somefile.md', 'docx', outputfile="somefile.docx")
assert output == ""