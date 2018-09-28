@[TOC](黄金分割法)
## 条件

 - 函数在所选区间为单峰函数
 - 大概知道极值所在的一个区间
 在这种条件下其算法有效性很高

## 代码如下

```python
import numpy as np
import math
import matplotlib.pyplot as plt


def phi(x):
    return x * x - 2 * x + 1


def golds_search(phi, a, b, delta, epsilon):
    '''
        黄金分割法，p15
    :param phi: 目标函数
    :param a:   做端点
    :param b:   右端点
    :param delta:   参数
    :param epsilon: 参数
    :return:
    '''
    # 初始参数
    G = np.zeros((1000, 4))
    t = (math.sqrt(5) - 1) / 2
    h = b - a
    phia = phi(a)
    phib = phi(b)
    p = a + (1 - t) * h
    q = a + t * h
    phip = phi(p)
    phiq = phi(q)
    # 记录参数G
    k = 0
    G[k, :] = [a, p, q, b]
    while abs(phip - phiq) > epsilon or h > delta:
        if phip < phiq:
            b = q
            phiq = phip
            q = p
            p = a + (1 - t) * (b - a)
            phip = phi(p)
        else:
            a = p
            phip = phiq
            p = q
            q = a + t * (b - a)
        k = k + 1
        h = b - a
        G[k, :] = [a, p, q, b]
    if phip <= phiq:
        min_value = phip
        min_point = p
    else:
        min_value = phiq
        min_point = q
    return min_point, min_value


if __name__ == '__main__':
    x = np.linspace(-2, 2, 100)
    plt.plot(x, phi(x))
    plt.show()
    result = golds_search(phi, float(-2), float(2), 0.001, 0.001)
    print(result)

```

## 结果
所示函数如下
![在这里插入图片描述](https://img-blog.csdn.net/20180928165548409?watermark/2/text/aHR0cHM6Ly9ibG9nLmNzZG4ubmV0L3FxXzI2NDc5NjU1/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70)
输出结果
```
(0.9999086424263046, 8.346206281650836e-09)
```

> 代码放在github上：https://github.com/finepix/py_workspace/tree/master/optimization_algorithm
