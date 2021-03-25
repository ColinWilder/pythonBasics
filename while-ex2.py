age=0
while True:
    how_old=input("Enter your age: ")
    if how_old=="No":
        print("Don't be ashamed of your age!")
        break
    num=int(how_old)
    age=age+num
    print("Your age is %s - that's old!" %age)
