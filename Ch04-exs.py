## Exercise 1

if 0==True:
    print("0 is true.")
else:
    print("0 is false.")
if 1==True:
    print("1 is true.")
else:
    print("1 is false.")
if 2==True:
    print("2 is true.")
else:
    print("2 is false.")

print("\n")

## Exercise 2
v=9
if v>=0 and v<=9:
    print("V passes the 0-9 test.")
else:
    print("V fails test.")

print("\n")

## Exercise 3

l=["a","d","c"]
if l[0]=="b":
    print("quarry is in list l")
elif l[1]=="b":
    print("quarry is in list l")
else:
    print("quarry is NOT in list l")


## Exercise 4
print("\n")

fridge={}
fridge["milk"]="creamy"
fridge["eggs"]="protein-filled"
fridge["cheese"]="bluecheezy"
food_sought=input("What food do you seek? ")

for food in fridge:
    if food == food_sought:
        print(food, fridge.get(food))
        break
else:
    print("sought-after food is not in fridge")


## Exercise 5
print("\n")

fridge={}
fridge["milk"]="creamy"
fridge["eggs"]="protein-filled"
fridge["cheese"]="bluecheezy"
food_sought=input("What food do you seek? ")

fridge_list=list(fridge.keys())

while len(fridge_list)>0:
    current_key=fridge_list[0]
    if current_key==food_sought:
        print("sought-after food is in fridge and is %s" % fridge[food_sought])
        break
    fridge_list.pop(0)
    if len(fridge_list)==0:
        print("sought-after food is NOT in fridge")


## Exercise 6
print("\n")

fridge={}
fridge["milk"]="creamy"
fridge["eggs"]="protein-filled"
fridge["cheese"]="bluecheezy"
food_sought=input("What food do you seek? ")

try:
    if fridge[food_sought]=="bluecheezy":
        print("you must like blue cheese!")
except (KeyError) as error:
    print("none of that here, I'm afraid")

