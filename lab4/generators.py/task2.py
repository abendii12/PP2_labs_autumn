def even_nums():
    for i in range(0, n+1, 2):
        yield i
n = int(input())
a = even_nums()
print(", ".join(map(str, a)))