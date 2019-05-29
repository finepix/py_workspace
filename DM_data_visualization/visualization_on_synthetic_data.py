#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2019/5/29 18:46
# @File    : visualization_on_synthetic_data.py
# @Author  : shawn_zhu, zhuxin@hdu.edu.cn
"""

from scipy.io import loadmat
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sklearn
from sklearn.decomposition import PCA, kernel_pca
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import LocallyLinearEmbedding
import numpy as np
import time


# SYNTHETIC_DATA_NAME = 'toroidal_helix'
# SYNTHETIC_DATA_NAME = '3d_gaussian'
SYNTHETIC_DATA_NAME = 'swiss_roll'


def load_synthetic_data_from_mat_file():
    file_name = 'data/' + SYNTHETIC_DATA_NAME + '.mat'
    data = loadmat(file_name)
    fea = data['fea']
    colors = data['colors']
    return fea, colors

def visual_on_origin_data(fea, label):
    """

    :param fea:
    :param label:
    :return:
    """
    fea_min, fea_max = np.min(fea, 0), np.max(fea, 0)
    fea = (fea - fea_min) / (fea_max - fea_min)

    label_min, label_max = np.min(label), np.max(label)
    label = (label - label_min) / (label_max - label_min)

    fig = plt.figure()
    ax = Axes3D(fig)

    for i in range(fea.shape[0]):
        label_i = label[i, 0]
        ax.scatter(fea[i, 0], fea[i, 1], fea[i, 2], color=plt.cm.Set1(label_i))
        # ax.text(fea[i, 0], fea[i, 1], fea[i, 2], str(label_i), color=plt.cm.Set1(label_i / 10.),
        #          fontdict={'weight': 'bold', 'size': 9})

    plt.title('Visualization on {}'.format(SYNTHETIC_DATA_NAME))
    plt.show()


def plot_embedding(fea, label, title=None):
    fea_min, fea_max = np.min(fea, 0), np.max(fea, 0)
    fea = (fea - fea_min) / (fea_max - fea_min)

    label_min, label_max = np.min(label), np.max(label)
    label = (label - label_min) / (label_max - label_min)

    plt.figure()
    # ax = plt.subplot(111)
    for i in range(fea.shape[0]):
        label_i = label[i, 0]
        plt.scatter(fea[i, 0], fea[i, 1], c=plt.cm.Set1(label_i), s=10)
        # plt.text(fea[i, 0], fea[i, 1], str(label_i), color=plt.cm.Set1(label_i / 10.),
        #          fontdict={'weight': 'bold', 'size': 9})
    plt.xticks([]), plt.yticks([])
    if title is not None:
        plt.title(title)


def compute_pca(fea):
    """
        view on pca
    :return:
    """
    print("Computing PCA projection")
    t0 = time.time()
    fea_pca = PCA(n_components=2).fit_transform(fea)
    t1 = time.time()
    return fea_pca, t1 - t0


def compute_kernel_pca(fea):
    """
        view on pca
    :return:
    """
    print("Computing kernel PCA projection")
    t0 = time.time()
    fea_pca = kernel_pca.KernelPCA(kernel="rbf", n_components=2,
                                   fit_inverse_transform=True, gamma=2.).fit_transform(fea)
    t1 = time.time()
    return fea_pca, t1 - t0


def compute_lda(fea, label):
    """
        LDA
    :param fea:
    :param label:       cause lda is a supervised algorithm, so there should be a label for the corresponding data
    :return:
    """
    print("Computing Linear Discriminant Analysis projection")
    fea_copy = fea.copy()
    fea_copy.flat[::fea.shape[1] + 1] += 0.01  # Make X invertible
    t0 = time.time()
    fea_lda = LinearDiscriminantAnalysis(n_components=2).fit_transform(fea_copy, label)
    t1 = time.time()
    return fea_lda, t1 - t0


def compute_lle(fea, n_neighbors=20):
    print("Computing LLE embedding")
    clf = LocallyLinearEmbedding(n_neighbors, n_components=2, method='standard')

    t0 = time.time()
    fea_lle = clf.fit_transform(fea)
    t1 = time.time()
    print("Done. Reconstruction error: %g" % clf.reconstruction_error_)

    return fea_lle, t1 - t0


def compute_t_sne(fea):
    """
            t-SNE
    :return:
    """
    print("Computing t-SNE embedding")
    tsne = sklearn.manifold.TSNE(n_components=2, init='pca')
    t0 = time.time()
    fea_tsne = tsne.fit_transform(fea)
    t1 = time.time()

    return fea_tsne, t1 - t0



def run():
    """
        main function for the experiment
    :return:
    """

    [X, Y] = load_synthetic_data_from_mat_file()
    visual_on_origin_data(X, Y)

    # PCA
    X_pca, t = compute_pca(X)
    plot_embedding(X_pca, Y, "Principal Components projection of %s (time %.2fs)" % (SYNTHETIC_DATA_NAME, t))

    # TODO: cause LDA is a supervised algorithm, there is no information on label in this synthetic data,so we pick
    # TODO: up KPCA instead
    # LDA
    # X_lda, t = compute_lda(X, Y)
    # plot_embedding(X_lda, Y, "Linear Discriminant projection of %s (time %.2fs)" % t)

    # KPCA
    X_kpca, t = compute_kernel_pca(X)
    plot_embedding(X_kpca, Y, "kernel pca projection of %s (time %.2fs)" % (SYNTHETIC_DATA_NAME, t))


    # LLE
    X_lle, t = compute_lle(X)
    plot_embedding(X_lle, Y, "Locally Linear Embedding of %s (time %.2fs)" % (SYNTHETIC_DATA_NAME, t))

    # t-SNE
    X_tsne, t = compute_t_sne(X)
    plot_embedding(X_tsne, Y, "t-SNE embedding of %s (time %.2fs)" % (SYNTHETIC_DATA_NAME, t))


if __name__ == '__main__':
    run()
