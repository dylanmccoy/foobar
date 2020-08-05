def max_subset_product(panels):
    if len(panels) == 0:
        return str(0)
    if len(panels) == 1:
        return str(panels[0])
    least_neg = float('-inf')
    cur_product = 1
    num_zeroes = 0
    num_pos = 0
    num_neg = 0
    for panel_value in panels:
        if abs(panel_value) > 0:
            cur_product *= panel_value
            if panel_value < 0:
                num_neg += 1
                least_neg = max(least_neg, panel_value)
            else:
                num_pos += 1
        else:
            num_zeroes += 1
    if num_neg % 2 == 1:
        cur_product /= least_neg

    if num_neg == 1 and num_pos == 0 and num_zeroes > 0:
        cur_product = 0

    if num_zeroes == len(panels):
        cur_product = 0

    return str(cur_product)

a = [2, 0, 2, 2, 0]
b = [-2, -3, 4, -5]
c = [0, 0, 0, -1]
d = [0, 0, 0, 0]
e = []
f = [-1]
print(max_subset_product(a))
print(max_subset_product(b))
print(max_subset_product(c))
print(max_subset_product(d))
print(max_subset_product(e))
print(max_subset_product(f))
