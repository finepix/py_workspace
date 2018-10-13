import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D


def sdm(fun, gfun, x0, rho, sigma, epsilon):
    max_iter_k = 5000
    max_m = 20
    k = 0
    while k < max_iter_k:
        grad = gfun(x0)
        d = -grad
        if np.linalg.norm(d) < epsilon:
            break

        m = 0
        mk = 0
        while m < max_m:        # armijo 搜索
            print('f(x + rho^m * d) = {}'.format(fun(x0 + pow(rho, m) * d)))
            print('f(x) + sigma * rho^m * g * d = {}'.format(fun(x0) + sigma * pow(rho, m) * np.dot(grad.T, d)))
            if fun(x0 + pow(rho, m) * d) < fun(x0) + sigma * pow(rho, m) * np.dot(grad.T, d):
                mk = m
                break
            m += 1

        x0 = x0 + pow(rho, mk) * d
        k += 1

    print('iterations : {}'.format(k))
    return x0, fun(x0)


def obj(x):
    y = x[1]
    x = x[0]
    return 100 * pow(x * x - y, 2) + pow(x - 1, 2)


def obj_g(x):
    y = x[1]
    x = x[0]
    arr = [400 * x * (x * x - y) + 2 * (x - 1), -200 * (x * x - y)]
    return np.array(arr).T


def test_f(x):
    y = x[1]
    x = x[0]
    return (x - 1)**2 + (y - 2)**2


def test_f_g(x):
    y = x[1]
    x = x[0]
    arr = [2 * (x - 1), 2 * (y - 2)]
    return np.array(arr).T


if __name__ == '__main__':
    X = np.linspace(-3, 3, 100)
    Y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(X, Y)

    # Z = (X - 1)**2 + (Y - 2)**2
    Z = 100 * (X**2 - Y)**2 + (X - 1)**2

    fig = plt.figure()
    ax = Axes3D(fig)
    surf = ax.plot_surface(X, Y, Z, cmap=plt.cm.winter)

    ax.set_xlabel("x-label", color='r')
    ax.set_ylabel("y-label", color='g')
    ax.set_zlabel("z-label", color='b')

    plt.savefig('graph_for_function/obj_f.png')
    plt.show()

    x0 = np.array([0.0, 0.0]).T
    # print(sdm(test_f, test_f_g, x0, 0.5, 0.4, 1e-5))
    print(sdm(obj, obj_g, x0, 0.5, 0.4, 1e-5))
