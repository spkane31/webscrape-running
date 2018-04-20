a = [0, 4, 2 ,2 , 6 ,11]
new = [0]
for u in a:
    if u not in new:
        new = new + [u]

print(new)
