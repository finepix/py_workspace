from time import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import (manifold, datasets, random_projection)
import scipy.io


# 加载数据
usps = scipy.io.loadmat('data/USPS.mat')
processed_f = scipy.io.loadmat('data/ProcessedF.mat')
f = processed_f['F']
gnd = usps['gnd']

# 数据截断
f = f[:2000, :]
gnd = gnd[:2000, :]

source_data = np.hstack((f, gnd))
print(source_data.shape)


#%%
# 将降维后的数据可视化,2维
def plot_embedding_2d(X, title=None):
    y = X[:, -1]
    x = X[:, :-1]
    # 坐标缩放到[0,1]区间
    x_min, x_max = np.min(x, axis=0), np.max(x, axis=0)
    x = (x - x_min) / (x_max - x_min)

    # 降维后的坐标为（X[i, 0], X[i, 1]），在该位置画出对应的digits
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    for i in range(x.shape[0]):
        ax.text(x[i, 0], x[i, 1], str(int(y[i])),
                color=plt.cm.Set1(y[i] / 10.),
                fontdict={'weight': 'bold', 'size': 4})

    if title is not None:
        plt.title(title)


#%%
# 将降维后的数据可视化,3维
def plot_embedding_3d(X, title=None):
    y = X[:, -1]
    x = X[:, :-1]
    # 坐标缩放到[0,1]区间
    x_min, x_max = np.min(x, axis=0), np.max(x, axis=0)
    x = (x - x_min) / (x_max - x_min)

    # 降维后的坐标为（X[i, 0], X[i, 1],X[i,2]），在该位置画出对应的digits
    fig = plt.figure()
    ax = Axes3D(fig)
    for i in range(x.shape[0]):
        ax.text(x[i, 0], x[i, 1], x[i, 2], str(int(y[i])),
                color=plt.cm.Set1(y[i] / 10.),
                fontdict={'weight': 'bold', 'size': 4})

    if title is not None:
        plt.title(title)


#%%
# t-SNE
print("Computing t-SNE embedding")
tsne = manifold.TSNE(n_components=3, init='pca', random_state=0)
t0 = time()
X_tsne = tsne.fit_transform(source_data[:, :-1])
print(X_tsne.shape)
tsne_data = np.hstack((X_tsne, gnd))
plot_embedding_2d(tsne_data, "t-SNE 2D")
plot_embedding_3d(tsne_data, "t-SNE 3D")

plt.show()
