dairy_section=["milk","eggs","cheese","cream"]
print("%s, %s" % (dairy_section[0],dairy_section[-1]))
milk_expiration=(12,10,2009)
print("The milk will expire on %s/%s/%s." % (milk_expiration[0],milk_expiration[1],milk_expiration[2]))
milk_carton={}
milk_carton["expiration_date"]=milk_expiration
milk_carton["fl_oz"]=64
milk_carton["Cost"]=1.99
milk_carton["brand_name"]="Laughing Cow"
print(list(milk_carton.values()))
print(6*milk_carton["Cost"])
cheeses=["gorgonzola","smoked gouda","parm","brie"]
dairy_section.extend(cheeses)
print(dairy_section)
dairy_section.pop(7)
dairy_section.pop(6)
dairy_section.pop(5)
dairy_section.pop(4)
print(dairy_section)
print(len(cheeses))
print(cheeses[0][0:5])
