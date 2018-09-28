import numpy as np
import matplotlib.pyplot as plt
import math


def phi(x):
    '''
        测试函数1
    :param x:
    :return:
    '''
    return x * x - 2 * x + 1


def complicated_func(x):
    '''
        测试函数2
    :param x:
    :return:
    '''
    return x * x * x + 5 * math.sin(2 * x)


def parabolic_search(f, a, b, epsilon=1e-1):
    '''
        抛物线法，迭代函数
    :param f: 目标函数
    :param a:   起始点
    :param b:   终止点
    :param epsilon: 阈值
    :return:
    '''
    h = (b - a) / 2
    s0 = a
    s1 = a + h
    s2 = b
    f0 = f(s0)
    f1 = f(s1)
    f2 = f(s2)
    h_mean = (4 * f1 - 3 * f0 - f2) / (2 * (2 * f1 - f0 - f2)) * h
    s_mean = s0 + h_mean
    f_mean = f(s_mean)
    # 调试
    k = 0
    while s2 - s0 > epsilon:
        h = (s2 - s0) / 2
        h_mean = (4 * f1 - 3 * f0 - f2) / (2 * (2 * f1 - f0 - f2)) * h
        s_mean = s0 + h_mean
        f_mean = f(s_mean)
        if f1 <= f_mean:
            if s1 < s_mean:
                s2 = s_mean
                f2 = f_mean
                # 重新计算一次，书上并没有写，所以导致一直循环
                s1 = (s2 + s0)/2
                f1 = f(s1)
            else:
                s0 = s_mean
                f0 = f_mean
                s1 = (s2 + s0)/2
                f1 = f(s1)
        else:
            if s1 > s_mean:
                s2 = s1
                s1 = s_mean
                f2 = f1
                f1 = f_mean
            else:
                s0 = s1
                s1 = s_mean
                f0 = f1
                f1 = f_mean
        # print([k, (s2 - s0), f_mean, s_mean])
        print(k)
        k += 1
    return s_mean, f_mean


# 课后习题
def p_27_2_f(x):
    return x * x * x - 2 * x + 1


if __name__ == '__main__':
    # x = np.linspace(1, 3, 200)
    # y = []
    # index = 0
    # for i in x:
    #     y.append(complicated_func(x[index]))
    #     index += 1
    # plt.plot(x, y)
    # plt.show()
    #
    # result = parabolic_search(complicated_func, 1.0, 3.0)
    # print(result)

    # x = np.linspace(0, 2, 200)
    # plt.plot(x, phi(x))
    # plt.show()
    # result = parabolic_search(phi, 0, 2.0)
    # print(result)

    # p27 习题解答
    x = np.linspace(0, 3, 1000)
    y = []
    index = 0
    for i in x:
        y.append(p_27_2_f(x[index]))
        index += 1
    plt.plot(x, y)
    plt.show()
    result = parabolic_search(p_27_2_f, 0.0, 3.0, 0.01)
    print(result) 

