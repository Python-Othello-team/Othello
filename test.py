import copy

a = [1, 2, 3, 4]
b = copy.deepcopy(a)
b.append(34)

print(a)
print(b)