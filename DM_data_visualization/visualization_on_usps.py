#!/usr/bin/env python
# encoding: utf-8
"""
# @Time    : 2019/5/28 15:53
# @File    : visualization_on_usps.py
# @Author  : shawn_zhu, zhuxin@hdu.edu.cn
"""
from scipy.io import loadmat
import matplotlib.pyplot as plt
import sklearn
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.manifold import LocallyLinearEmbedding
import numpy as np
import time


def load_usps_data_from_mat_file():
    file_name = 'data/usps_1000.mat'
    data = loadmat(file_name)
    fea = data['fea']
    gnd = data['gnd'] - 1
    return fea, gnd

def visual_on_origin_data(fea, margin=0, img_size=(16, 16), n_img_per_row=20):
    """
    :param fea:             feature for usps
    :param margin:          width between imgages
    :param img_size:
    :param n_img_per_row:
    :return:
    """
    img_width = img_size[1]
    width = img_width + margin

    img = np.zeros((width * n_img_per_row, width * n_img_per_row))
    for i in range(n_img_per_row):
        ix = width * i
        for j in range(n_img_per_row):
            iy = width * j
            img[ix:ix + img_width, iy:iy + img_width] = fea[i * n_img_per_row + j].reshape(img_size)

    plt.imshow(img, cmap=plt.cm.binary)
    plt.xticks([])
    plt.yticks([])
    plt.title('Visualization on USPS')


def plot_embedding(fea, label, title=None):
    fea_min, fea_max = np.min(fea, 0), np.max(fea, 0)
    fea = (fea - fea_min) / (fea_max - fea_min)

    plt.figure()
    # ax = plt.subplot(111)
    for i in range(fea.shape[0]):
        label_i = label[i, 0]
        plt.text(fea[i, 0], fea[i, 1], str(label_i), color=plt.cm.Set1(label_i / 10.),
                 fontdict={'weight': 'bold', 'size': 9})

    # if hasattr(offsetbox, 'AnnotationBbox'):
    #     # only print thumbnails with matplotlib > 1.0
    #     shown_images = np.array([[1., 1.]])  # just something big
    #     for i in range(X.shape[0]):
    #         dist = np.sum((X[i] - shown_images) ** 2, 1)
    #         if np.min(dist) < 4e-3:
    #             # don't show points that are too close
    #             continue
    #         shown_images = np.r_[shown_images, [X[i]]]
    #         imagebox = offsetbox.AnnotationBbox(
    #             offsetbox.OffsetImage(digits.images[i], cmap=plt.cm.gray_r),
    #             X[i])
    #         ax.add_artist(imagebox)
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


def compute_lle(fea, n_neighbors=5):
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
    [X, Y] = load_usps_data_from_mat_file()
    visual_on_origin_data(X)

    # PCA
    X_pca, t = compute_pca(X)
    plot_embedding(X_pca, Y, "Principal Components projection of USPS (time %.2fs)" % t)

    # LDA
    X_lda, t = compute_lda(X, Y)
    plot_embedding(X_lda, Y, "Linear Discriminant projection of USPS (time %.2fs)" % t)

    # LLE
    X_lle, t = compute_lle(X)
    plot_embedding(X_lle, Y, "Locally Linear Embedding of USPS (time %.2fs)" % t)

    # t-SNE
    X_tsne, t = compute_t_sne(X)
    plot_embedding(X_tsne, Y, "t-SNE embedding of USPS (time %.2fs)" % t)


if __name__ == '__main__':
    run()
