def squares():
    for i in range(N):
        yield i*i
N = int(input())
a = squares()
for b in a:
    print(b)