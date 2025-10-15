a = input()
new = ""
i=0
while i<len(a):
    if a[i] == "_":
        new += a[i + 1].upper()
        a = a[:i] + a[i+1:]
    else:
        new += a[i]
    i+=1
print(new)