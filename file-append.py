# file-append.py
f = open('helloworld.txt','a') # note the "a" at the end. - it's called a flag
f.write('\n' + 'hello world') # adds a new line and the hello world phrase
f.close()

# run it then open the hellowrold.txt file and see how it changes
# run again, wash rinse repeat, etc. x3
