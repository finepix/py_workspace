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
            phiq = phi(q)
        k = k + 1
        h = b - a
        G[k, :] = [a, p, q, b]
        print(k)
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
