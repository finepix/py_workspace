import cv2
import matplotlib.pyplot as plt


def edge_detect(im):
    """
            利用canny进行边缘检测，步骤如下：
                1、高斯模糊
                2、灰度转化
                3、计算梯度
                4、非最大信号抑制
                5、高低阈值输出二值图像
    :param im: 图像
    :return: 返回边缘图像（二值化图像）
    """

    blurred = cv2.GaussianBlur(im, (3, 3), 0)
    gray = cv2.cvtColor(blurred, cv2.COLOR_RGB2GRAY)

    x_grad = cv2.Sobel(gray, cv2.CV_16SC1, 1, 0)
    y_grad = cv2.Sobel(gray, cv2.CV_16SC1, 0, 1)

    edge_out = cv2.Canny(x_grad, y_grad, 30, 120)

    return edge_out


if __name__ == '__main__':
    img = cv2.imread('edge_detection.jpg')

    edge_output = edge_detect(img.copy())

    plt.figure(figsize=(20, 8))

    plt.subplot(121)
    plt.imshow(img[:, :, ::-1])

    plt.subplot(122)
    plt.imshow(edge_output)

    plt.tight_layout()
    plt.show()

