a = list(map(int, input().split()))
k, c = map(int, input().split())
f = a[:k]
s = a[k:]
f.append(c)
f += s

a.append(int())
for i in range(len(a)):
    if i > k:
        pass

print(f)
