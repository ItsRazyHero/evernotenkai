for _ in range(int(input())):
    n, k = map(int, input().split())
    prefix = [0, k]
    for i in range(1, n):
        prefix.append(prefix[i] + k + i)

    