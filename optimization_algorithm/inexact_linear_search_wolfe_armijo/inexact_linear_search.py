import numpy as np
import math
import matplotlib.pyplot as plt


def armijo(f, gf, x_k, d_k, beta=0.5, sigma=0.1):
    m = 0
    m_k = 0
    while True:
        if f(x_k + pow(beta, m) * d_k) > f(x_k) + \
                sigma * pow(beta, m) * gf(x_k) * d_k:
            m += 1
        else:
            m_k = m
            break
    alpha = pow(beta, m_k)
    new_x_k = x_k + alpha * d_k
    f_k = f(x_k[0], xk[1])
    newf_k = f(new_x_k[0], new_x_k[1])
    return f_k, newf_k

# 目标函数


def obj_func(x1, x2):
    return 100 * pow((x1 * x1 - x2), 2) + pow((x1 - 1), 2)


# 目标函数的梯度
def grad_func(x1, x2):
    return 400 * x1 * (x1 * x1 - x2) + 2 * (x1 - 1), -200 * (x1 * x1 - x2)


if __name__ == '__main__':
    x = np.linspace(0, 3, 1000)
    y = []
    index = 0
    for i in x:
        y.append(obj_func(x[index]))
        index += 1
    plt.plot(x, y)
    plt.show()
    result = golds_search(obj_func, 0, 3, 0.15, 0.15)
    print(result)
