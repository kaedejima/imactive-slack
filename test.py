x = 2
y = 4
while (x < y):
    n = y % x
    if not (n == 0):
        x += 1
    else:
        break
    pass
print('out', x, y)