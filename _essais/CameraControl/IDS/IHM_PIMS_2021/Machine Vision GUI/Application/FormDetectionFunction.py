import numpy as np
import cv2
import csv
import os

from Dictionary_EN import *
from PreProcessingFunction import func_contours_list

SHAPES_NAME_LIST = [STR_SQUARE, STR_TRIANGLE, STR_STAR, STR_CIRCLE, STR_HEXAGON, STR_PENTAGON]


def sort_shapes(index_detected_shapes_list):
    count_detected_shapes = np.zeros(6)

    for i in index_detected_shapes_list:
        count_detected_shapes[i] += 1

    return count_detected_shapes


def shape_2b_tested(img, cnt):
    x_min, x_max, y_min, y_max = coordinates(cnt)
    shape_img = np.zeros(img.shape, np.uint8)
    cv2.drawContours(shape_img, [cnt], 0, 255, -1)
    shape_img = crop_image_w_margin(shape_img, x_min, x_max, y_min, y_max)

    return shape_img


def cv2_to_outline(filename):
    outline = []
    file = open(filename, 'r')
    reader = csv.reader(file)
    for row in reader:
        if len(row) == 2:
            couple = [[int(row[0]), int(row[1])]]
            outline.append(couple)
    file.close()
    return [np.array(outline)]


def what_is_this_shape(shape, test_shapes_list):
    sim_coef_list = []
    for test_shape in test_shapes_list:
        sim_coef = cv2.matchShapes(shape, test_shape, cv2.CONTOURS_MATCH_I2, 0.0)
        sim_coef_list.append(sim_coef)

    return np.argmin(sim_coef_list)


def identify_shapes(shape_list, directory):
    detected_shapes_index_list = []
    test_shapes_list = get_test_img(directory)

    for shape in shape_list:
        shape_index = what_is_this_shape(shape, test_shapes_list)
        detected_shapes_index_list.append(shape_index)

    return detected_shapes_index_list


def get_img_shape_list(img, contours_list=None,):
    if contours_list is None:
        contours_list = func_contours_list(img, 50)

    img_shapes_list = []

    for cnt in contours_list:
        img_shape = shape_2b_tested(img, cnt)
        img_shapes_list.append(img_shape)

    return img_shapes_list


def get_test_contours(directory):
    test_contours_list = []
    for shape_index in range(6):
        shape_name = SHAPES_NAME_LIST[shape_index]
        folder = os.path.join(directory, shape_name)
        filename = os.path.join(folder, shape_name + str(0) + '.csv')
        test_cnt = cv2_to_outline(filename)
        test_contours_list.append(test_cnt[0])

    return test_contours_list


def get_test_img(directory):
    test_img = []
    for shape_index in range(6):
        shape_name = SHAPES_NAME_LIST[shape_index]
        folder = os.path.join(directory, shape_name)
        filename = os.path.join(folder, shape_name + str(0) + '.jpg')
        img = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
        test_img.append(img)
    return test_img


def crop_image(img, x_min, x_max, y_min, y_max):
    return img[y_min:y_max, x_min:x_max]


def coordinates(cnt):
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

    return leftmost[0], rightmost[0], topmost[1], bottommost[1]


def crop_image_w_margin(img, x_min, x_max, y_min, y_max):
    px = int((x_max - x_min) / 32)
    py = int((y_max - y_min) / 32)
    Y, X = img.shape
    if y_max + py >= Y:
        py = Y - y_max
    if x_max + px >= X:
        px = X - x_max
    if x_min - px <= 0:
        px = x_min
    if y_min - py <= 0:
        py = y_min
    img4 = crop_image(img, x_min - px, x_max + px, y_min - py, y_max + py)
    return img4


def write_csv_file(filename, outlines):
    fichier = open(filename, 'x')
    writer = csv.writer(fichier)
    for c in outlines:
        writer.writerow((c[0][0], c[0][1]))
    fichier.close()


def is_outside(cnt, img_size):
    leftmost = tuple(cnt[cnt[:, :, 0].argmin()][0])
    rightmost = tuple(cnt[cnt[:, :, 0].argmax()][0])
    topmost = tuple(cnt[cnt[:, :, 1].argmin()][0])
    bottommost = tuple(cnt[cnt[:, :, 1].argmax()][0])

    margin = 5

    if leftmost[0] <= margin:
        return True
    elif rightmost[0] >= img_size[1]-margin:
        return True
    elif topmost[1] <= margin:
        return True
    elif bottommost[1] >= img_size[0]-margin:
        return True

    return False