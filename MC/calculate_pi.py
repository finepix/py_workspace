import numpy as np
import matplotlib.pyplot as plt


def main():
    # 估计值
    n = 1000000
    x = np.random.rand(n, 2)
    inside = x[np.sqrt(x[:, 0]**2 + x[:, 1]**2) < 1]
    estimate = len(inside)/len(x) * 4
    print('pi:\t {}'.format(estimate))

    # 绘图
    plt.figure(figsize=(8, 8))
    plt.scatter(x[:, 0], x[:, 1], s=.5, c='red')
    plt.scatter(inside[:, 0], inside[:, 1], s=.5, c='blue')
    plt.show()


if __name__ == '__main__':
    main()
