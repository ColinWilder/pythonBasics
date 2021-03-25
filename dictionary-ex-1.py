menu_specials = {}
menu_specials["breakfast"] = "Canadian ham"
menu_specials["lunch"] = "tuna surprise"
menu_specials["dinner"] = "cheeseburger!"

print(menu_specials)

print(menu_specials["breakfast"])

hungry=menu_specials.keys()
print(list(hungry))
print(menu_specials.get("dinner"))
