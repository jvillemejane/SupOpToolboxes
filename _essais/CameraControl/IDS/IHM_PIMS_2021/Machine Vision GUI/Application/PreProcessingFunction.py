import numpy as np
import cv2
import io

import matplotlib

import matplotlib.pyplot as plt
from Utils import convert_CV_64F_to_uint8


# def hist_curve(im):
#     bins = np.arange(256).reshape(256, 1)
#     h = np.zeros((300,256,3))
#
#     if len(im.shape) == 2:
#         color = [(255,255,255)]
#     elif im.shape[2] == 3:
#         color = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
#
#     for ch, col in enumerate(color):
#         hist_item = cv2.calcHist([im], [ch], None, [256], [0, 256])
#         cv2.normalize(hist_item, hist_item, 0, 255, cv2.NORM_MINMAX)
#         hist = np.int32(np.around(hist_item))
#         pts = np.int32(np.column_stack((bins, hist)))
#
#         cv2.polylines(h, [pts], False, col, 1)
#     y = np.flipud(h)
#
#     return y

def hist_curve(im):
    bins = np.arange(256).reshape(256, 1)
    h = np.zeros((300,256,3))

    if len(im.shape) == 2:
        color = 'k'
    elif im.shape[2] == 3:
        color = ('b','g','r')

    fig = plt.figure()
    for ch, col in enumerate(color):
        hist_item = cv2.calcHist([im], [ch], None, [256], [0, 256])
        plt.plot(hist_item, color=col)

    fig.canvas.draw()

    # Now we can save it to a numpy array.
    data = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    data = data.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return data


def func_erosion(img, kernel_size):
    """

    :param img:
    :param kernel_size:
    :return:
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.erode(img, kernel, iterations=1)


def func_dilatation(img, kernel_size):
    """

    :param img:
    :param kernel_size:
    :return:
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    return cv2.dilate(img, kernel, iterations = 1)


def func_opening(img, kernel_size=3):
    """
    !!! INPUT IMAGE MUST BE BINARIZED !!!

    Apply an opening of the input image (ei: erosion + dilatation). Useful to eliminate background noise (little
    white spot on the black background)

    :param img: Input image, must be binarized (ei: pixel = 0 or 1)
    :param kernel_size: Size of the matrix of convolution, default value = 3
    :return: Image after the opening process
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    return img


def func_closing(img, kernel_size=3):
    """
    !!! INPUT IMAGE MUST BE BINARIZED !!!

    Apply an closing of the input image (ei: dilatation + erosion). Useful to eliminate foreground noise (little dark
    spot on the white foreground)

    :param img: Input image, must be binarized (ei: pixel = 0 or 1)
    :param kernel_size: Size of the matrix of convolution, default value = 3
    :return: Image after the closing process
    """
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    return img


def func_gaus_blurring(img, kernel_size, sigma):
    """

    :param img:
    :param kernel_size:
    :param sigma:
    :return:
    """

    return cv2.GaussianBlur(img, (kernel_size, kernel_size), sigmaX=sigma, sigmaY=sigma, borderType=cv2.BORDER_DEFAULT)


def func_median_blur(img, kernel_size):
    """

    :param img:
    :param kernel_size:
    :return:
    """
    return cv2.medianBlur(img, kernel_size)


def func_bilateral_filter(img, size, sigma):
    """

    :param img:
    :param size:
    :param sigma:
    :return:
    """
    return cv2.bilateralFilter(img, size, sigma, sigma)


def func_equalization(img):
    """

    :param img:
    :return:
    """
    return cv2.equalizeHist(img)


def func_simple_thresholding(img, threshold):
    """
    Apply a thresholding on the input image (MUST BE IN GRAYSCALE). Pixels with a value above threshold will be set
    at 1 and those below at 0

    :param img: Input image, must be in grayscale (8 bit)
    :param threshold: Threshold
    :return: Image after thresholding, binarized image (ei: pixel = 0 or 1)
    """

    return cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]


def func_adaptive_thresholding(img, method, block_size, c):
    """

    :param img:
    :param method:
    :param block_size:
    :param c:
    :return:
    """
    if method == 0:
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, block_size, c)
    else:
        return cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, block_size, c)


def func_otsu_thresholding(img):
    """

    :return:
    """
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]


def func_ft(img):
    """

    :param img:
    :return:
    """

    if len(img.shape) == 3:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    dft = cv2.dft(np.float32(img), flags=cv2.DFT_COMPLEX_OUTPUT)
    dft_shift = np.fft.fftshift(dft)
    magnitude_spectrum = 20 * np.log(cv2.magnitude(dft_shift[:, :, 0], dft_shift[:, :, 1]))

    return convert_CV_64F_to_uint8(magnitude_spectrum)


def func_contours_list(img, area_min=0,area_max=100000):
    contours_list, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours_list_area = []
    for ctn in contours_list:
        area = cv2.contourArea(ctn)
        if area > area_min and area < area_max :
            contours_list_area.append(ctn)
    return contours_list_area
# donne la liste des coordonnes des points des contours des formes détectées dont l'aire est superieure à 50


def func_find_draw_contours(img, surface_min=0, contours_list=None):
    if contours_list is None:
        contours_list = func_contours_list(img, surface_min)

    contours_img = cv2.merge([img, img, img])
    cv2.drawContours(contours_img, contours_list, -1, (0, 0, 255), 3)

    return contours_img


def gray_to_binary(img, threshold, opening, closing, blur):
    if threshold == -1:
        binary_img = func_otsu_thresholding(img)
    else:
        binary_img = func_simple_thresholding(img, threshold)

    if opening:
        binary_img = func_opening(binary_img)
    if closing:
        binary_img = func_closing(binary_img)
    if blur:
        binary_img = func_gaus_blurring(binary_img, 5, 2)

    return binary_img



