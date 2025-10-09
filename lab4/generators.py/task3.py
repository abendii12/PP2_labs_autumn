def divisible_th_fr():
    for i in range(0, n+1, 12):
        yield i
n = int(input())
a = divisible_th_fr()
print(",".join(map(str, a)))    