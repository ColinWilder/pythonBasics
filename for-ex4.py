for food in ("pate","cheese","rotten apples","crackers","whip cream","rotten tomato soup"):
    if food[0:6]=="rotten":
        continue
    if food=="pate":
        continue    
    print("You can eat %s." %food)
