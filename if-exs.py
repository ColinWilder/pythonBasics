omlet_ingred={"eggs":2,"mr":5,"pepper":1,"cheese":1,"milk":1}
fridge_cont={"eggs":1,"mr":20,"pepper":3,"cheese":2,"tom":4,"milk":15}
have_ingred=[False]
if fridge_cont["eggs"]>omlet_ingred["eggs"]:
    have_ingred[0]=True
have_ingred.append("eggs")

print(have_ingred)
if fridge_cont["mr"]>omlet_ingred["mr"]:
    if have_ingred[0]==False:
        have_ingred[0]=True
    have_ingred.append("mr")

print(have_ingred)
