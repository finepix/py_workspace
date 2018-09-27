'''

@author shawn

'''


import numpy as np


def cart(arr, start, end):
    if (end - start) <= 1:
        return None
    size = end - start + 1
    rs = []
    for i in range(start+1, start+size):
        c1 = arr[start:i]
        c2 = arr[i:start+size]
        rs.append((c1.std()**2)*c1.size + (c2.std()**2)*c2.size)

    index = np.argmin(rs) + start
    print(arr[np.argmin(rs)])
    cart(arr, start, index)
    cart(arr, index+1, end)


# 数据测试
y = np.array([4.5, 4.75, 4.91, 5.34, 5.8, 7.05, 7.9, 8.23, 8.7, 9])
cart(y, 0, y.size)






