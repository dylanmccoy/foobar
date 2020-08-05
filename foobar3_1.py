
import time
import random
def gen_triples(div_list, i, length):
    if length == 3:
        return 1
    else:
        count_triples = 0
        # print(div_list[i])
        for idx in div_list[i]:
            count_triples += gen_triples(div_list, idx, length + 1)
        return count_triples

def find_access(l):
    div_list = [[] for i in range(len(l))]
    for i in range(len(l)):
        for j in range(i):
            if l[i] % l[j] == 0:
                div_list[j].append(i)
    # print(div_list)

    count_triples = 0
    for i in range(len(l)):
        count_triples += gen_triples(div_list, i, 1)
    return count_triples

def gen_triples2(l, i, length):
    if length == 3:
        return 1
    else:
        count = 0
        for idx in range(i + 1, len(l)):
            if l[idx] % l[i] == 0:
                count += gen_triples2(l, idx, length + 1)
        return count

def find_access2(l):
    count = 0
    for i in range(len(l)):
        count += gen_triples2(l, i, 1)
    return count
a = [1, 2, 3, 4, 5, 6]
b = [1, 1, 1]

def check1(a):
    cur = time.time()
    print(find_access(a))
    print("time elapsed =", time.time() - cur)

def check2(a):
    cur = time.time()
    print(find_access2(a))
    print("time elapsed =", time.time() - cur)

def check3(a):
    print(find_access3(a))
def find_access3(l):
    count = 0

    for j in range(1, len(l) - 1):
        left_count = 0
        for i in range(0, j):
            if l[j] % l[i] == 0:
                left_count += 1
        right_count = 0
        for k in range(j + 1, len(l)):
            if l[k] % l[j] == 0:
                right_count += 1
        count += left_count * right_count
    return count
print("a")
check1(a)
check2(a)
check3(a)

print("b")
check1(b)
check2(b)
check3(b)

# print(random.randint(1, 999999))
c = [random.randint(1, 999999) for i in range(2000)]
# print(len(c), c)
print("c")
check1(c)
check2(c)
check3(c)

d = [1, 1]
e = [1, 2, 3]

check1(d)
check2(d)
check1(e)
check2(e)

f = [6, 5, 4, 3, 2, 1]

check1(f)
check2(f)

# g = [1 for i in range(2000)]

# check1(g)
# check2(g)

# def generate_multiples(l):

