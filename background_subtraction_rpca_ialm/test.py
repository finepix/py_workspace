from scipy import misc
import numpy as np
from glob import glob
from inexact_augmented_lagrange_multiplier import inexact_augmented_lagrange_multiplier
from scipy.io import savemat
import os
import sys
import matplotlib.pyplot as plt
from scipy.io import loadmat
import numpy as np
from matplotlib import cm
import matplotlib


def rgb2gray(rgb):
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
    return gray / 255


def make_video(alg, cache_path='./matrix_IALM_tmp'):
    name = alg
    if not os.path.exists(cache_path):
        os.mkdir(cache_path)
    # If you generate a big
    if not os.path.exists('%s/%s_tmp' % (cache_path, name)):
        os.mkdir("%s/%s_tmp" % (cache_path, name))
    mat = loadmat('./%s_background_subtraction.mat' % (name))
    org = X.reshape(d1, d2, X.shape[1]) * 255.
    fig = plt.figure()
    ax = fig.add_subplot(111)
    usable = [x for x in sorted(mat.keys()) if "_" not in x][0]
    sz = min(org.shape[2], mat[usable].shape[2])
    for i in range(sz):
        ax.cla()
        ax.axis("off")
        ax.imshow(np.hstack([mat[x][:, :, i] for x in sorted(
            mat.keys()) if "_" not in x] + [org[:, :, i]]), cm.gray)
        fname_ = '%s/%s_tmp/_tmp%03d.png' % (cache_path, name, i)
        if (i % 25) == 0:
            print('Completed frame', i, 'of', sz, 'for method', name)
        fig.tight_layout()
        fig.savefig(fname_, bbox_inches="tight")
    plt.close()


if __name__ == "__main__":
    names = sorted(glob("./ShoppingMall/*.bmp"))
    d1, d2, channels = misc.imread(names[0]).shape
    d1 = 128
    d2 = 160
    num = len(names)
    X = np.zeros((d1, d2, num))
    for n, i in enumerate(names):
        X[:, :, n] = misc.imresize(
            rgb2gray(misc.imread(i).astype(np.double)) / 255., (d1, d2))

    X = X.reshape(d1 * d2, num)
    clip = 100
    sz = clip
    A, E = inexact_augmented_lagrange_multiplier(X[:, : sz])
    A = A.reshape(d1, d2, sz) * 255.
    E = E.reshape(d1, d2, sz) * 255.
    savemat("./IALM_background_subtraction.mat", {"1": A, "2": E})
    make_video('IALM')
