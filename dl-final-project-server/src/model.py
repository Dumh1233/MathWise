import numpy as np
import cv2
import os
from .remove_equation_line import remove_lines_from_equation

MAXIMUM_LINE_HEIGHT = 20


def line_array(array):
    list_x_upper = []
    list_x_lower = []
    for y in range(0, len(array)):
        s_a, s_p = strtline(y, array)
        e_a, e_p = endline(y, array)
        if s_a >= 7 and s_p >= 5:
            list_x_upper.append(y)
        if e_a >= 5 and e_p >= 7:
            list_x_lower.append(y)

    return list_x_upper, list_x_lower


def strtline(y, array):
    count_ahead = 0
    count_prev = 0
    if y < 10:
        count_prev = 10 - y
    for i in array[y:y + 10]:
        if i > 3:
            count_ahead += 1

    for i in array[y - 10:y]:
        if i == 0:
            count_prev += 1

    return count_ahead, count_prev


def endline(y, array):
    count_ahead = 0
    count_prev = 0
    if len(array) - y < 10:
        count_ahead = 10 - (len(array) - y)
    for i in array[y:y + 10]:
        if i == 0:
            count_ahead += 1

    for i in array[y - 10:y]:
        if i > 3:
            count_prev += 1

    return count_ahead, count_prev


def line_removal_array(array):
    list_x_upper = []
    list_x_lower = []
    for y in range(0, len(array)):
        s_a, s_p = strtlineToRemove(y, array)
        e_a, e_p = endlineToRemove(y, array)
        if s_a >= 1 and s_p >= 1:
            list_x_upper.append(y)
        if e_a >= 1 and e_p >= 1:
            list_x_lower.append(y)

    return list_x_upper, list_x_lower


def strtlineToRemove(y, array):
    count_ahead = 0
    count_prev = 0
    if y < 3:
        count_prev = 3 - y
    for i in array[y:y + 3]:
        if (i > 0) and (i < MAXIMUM_LINE_HEIGHT):
            count_ahead += 1

    for i in array[y - 3:y]:
        if i == 0 or i >= MAXIMUM_LINE_HEIGHT:
            count_prev += 1

    return count_ahead, count_prev


def endlineToRemove(y, array):
    count_ahead = 0
    count_prev = 0
    if len(array) - y < 3:
        count_ahead = 3 - (len(array) - y)
    for i in array[y:y + 3]:
        if i == 0 or i >= MAXIMUM_LINE_HEIGHT:
            count_ahead += 1

    for i in array[y - 3:y]:
        if (i > 0) and (i < MAXIMUM_LINE_HEIGHT):
            count_prev += 1

    return count_ahead, count_prev


def endline_word(y, array, a):
    count_ahead = 0
    count_prev = 0
    for i in array[y:y + 2 * a]:
        if i < 2:
            count_ahead += 1
    for i in array[y - a:y]:
        if i > 2:
            count_prev += 1
    return count_prev, count_ahead


def end_line_array(array, a):
    list_endlines = []
    for y in range(len(array)):
        e_p, e_a = endline_word(y, array, a)
        if e_a >= int(1.5 * a) and e_p >= int(0.7 * a):
            list_endlines.append(y)
    return list_endlines


def refine_endword(array):
    refine_list = []
    for y in range(len(array) - 1):
        if array[y] + 1 < array[y + 1]:
            refine_list.append(array[y])

    if len(array) != 0:
        refine_list.append(array[-1])
    return refine_list


def refine_array(array_upper, array_lower):
    upperlines = []
    lowerlines = []
    for y in range(len(array_upper) - 1):
        if array_upper[y] + 5 < array_upper[y + 1]:
            upperlines.append(max(array_upper[y] - 10, 0))
    for y in range(len(array_lower) - 1):
        if array_lower[y] + 5 < array_lower[y + 1]:
            lowerlines.append(array_lower[y] + 10)

    if len(array_upper) > 0:
        upperlines.append(max(array_upper[-1] - 10, 0))

    if len(array_lower) > 0:
        lowerlines.append(array_lower[-1] + 10)

    return upperlines, lowerlines


def refine_line_removal_array(array_upper, array_lower):
    upperlines = []
    lowerlines = []
    for y in range(len(array_upper) - 1):
        if array_upper[y] + 5 < array_upper[y + 1]:
            upperlines.append(max(array_upper[y] - 5, 0))
    for y in range(len(array_lower) - 1):
        if array_lower[y] + 5 < array_lower[y + 1]:
            lowerlines.append(array_lower[y] + 5)

    if len(array_upper) > 0:
        upperlines.append(max(array_upper[-1] - 5, 0))
    if len(array_lower) > 0:
        lowerlines.append(array_lower[-1] + 5)

    return upperlines, lowerlines


def letter_width(contours):
    letter_width_sum = 0
    count = 0
    for cnt in contours:
        if cv2.contourArea(cnt) > 20:
            x, y, w, h = cv2.boundingRect(cnt)
            letter_width_sum += w
            count += 1

    return letter_width_sum / count


def end_wrd_dtct(lines, i, bin_img, mean_lttr_width, total_width, final_thr):
    count_y = np.zeros(shape=total_width)
    for x in range(total_width):
        for y in range(lines[i][0], lines[i][1]):
            if bin_img[y][x] == 255:
                count_y[x] += 1

    end_lines = end_line_array(count_y, int(mean_lttr_width))
    endlines = refine_endword(end_lines)
    for x in endlines:
        final_thr[lines[i][0]:lines[i][1], x] = 255
    return endlines


def get_letter_rect(k, contours):
    "Helper function for properly identifying '=' symbol. OpenCV"
    "will treat 2 dashes of 'sign' as separate contours, thus this"
    "will help to identify and merge them into a single '=' contour"
    valid = True
    x, y, w, h = cv2.boundingRect(contours[k])
    for i in range(len(contours)):
        cnt = contours[i]
        if i == k:
            continue
        elif cv2.contourArea(cnt) < 50:
            continue

        x1, y1, w1, h1 = cv2.boundingRect(cnt)

        if abs(x1 + w1 / 2 - (x + w / 2)) < 50:
            if y1 > y:
                h = abs(y - (y1 + h1))
                w = abs(x - (x1 + w1))
            else:
                valid = False
            break

    if h * w < 100:
        valid = False
    return valid, x, y, w, h


def letter_segmentation(lines_img, x_lines, i, base_img_lines, dir_path):
    letter_k = []

    copy_img = lines_img[i].copy()
    x_linescopy = x_lines[i].copy()
    contours, hierarchy = cv2.findContours(
        copy_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for k in range(len(contours)):
        cnt = contours[k]
        if cv2.contourArea(cnt) < 50:
            continue

        valid, x, y, w, h = get_letter_rect(k, contours)
        if valid:
            letter_k.append((x, y, w, h))

    letter = sorted(letter_k, key=lambda student: student[0])

    word = 1
    letter_index = 0
    for e in range(len(letter)):
        if letter[e][0] < x_linescopy[0]:
            letter_index += 1

            bot_x = max(letter[e][1] - 5, 0)
            top_x = min(letter[e][1] + letter[e][3] + 5, len(base_img_lines[i]) - 1)
            bot_y = max(letter[e][0] - 5, 0)
            top_y = min(letter[e][0] + letter[e][2] + 5, len(base_img_lines[i][0]) - 1)
            letter_img_tmp = base_img_lines[i][bot_x:top_x, bot_y:top_y]

            letter_img = letter_img_tmp
            if letter_img.any():
                letter_img = cv2.bitwise_not(letter_img_tmp)
                file_name = dir_path + "/" + format(i + 1, '02d') + '_' + format(word, '02d') + '_' + format(letter_index, '02d') + '.jpg'
                cv2.imwrite(file_name, 255 - letter_img)
                remove_lines_from_equation(file_name)
        else:
            x_linescopy.pop(0)
            word += 1
            letter_index = 1

            bot_x = max(letter[e][1] - 5, 0)
            top_x = min(letter[e][1] + letter[e][3] + 5, len(base_img_lines[i]) - 1)
            bot_y = max(letter[e][0] - 5, 0)
            top_y = min(letter[e][0] + letter[e][2] + 5, len(base_img_lines[i][0]) - 1)
            letter_img_tmp = base_img_lines[i][bot_x:top_x, bot_y:top_y]

            letter_img_tmp = cv2.bitwise_not(letter_img_tmp)
            if letter_img_tmp is not None and letter_img_tmp.any():
                letter_img = cv2.resize(letter_img_tmp, dsize=(28, 28), interpolation=cv2.INTER_AREA)
                file_name = dir_path + "/" + format(i + 1, '02d') + '_' + format(word, '02d') + '_' + format(
                    letter_index, '02d') + '.jpg'
                cv2.imwrite(file_name, 255 - letter_img)
                remove_lines_from_equation(file_name)


def is_line_to_char(start_line, end_line, count_y):
    count = 0
    before = start_line
    past = end_line

    if before < 5:
        count = 5 - before
    for i in count_y[past:past + 5]:
        if i > MAXIMUM_LINE_HEIGHT:
            count += 1

    for i in count_y[before - 5:before]:
        if i > MAXIMUM_LINE_HEIGHT:
            count += 1

    return count > 2


def image_segmentation(filepath):
    width = 1500
    pixel_set = 255
    kernel_size = 99
    normalized_mean = 30
    x_lines = []
    lines_img = []
    base_img_lines = []

    dir_path = filepath.rsplit("/", 3)[0] + "/segmentations/" + filepath.split("/")[-1].split(".")[0]
    os.makedirs(dir_path, exist_ok=True)
    print("\nStart Segmentation Pre-Processing \n")
    src_img = cv2.imread(filepath, cv2.IMREAD_GRAYSCALE)
    orig_height, orig_width = src_img.shape

    height = int(width * orig_height / orig_width)
    src_img = cv2.resize(src_img, dsize=(width, height),
                         interpolation=cv2.INTER_AREA)

    bin_img = cv2.adaptiveThreshold(src_img, pixel_set, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, kernel_size,
                                    normalized_mean)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 90))
    morph = cv2.morphologyEx(bin_img, cv2.MORPH_CLOSE, kernel)
    morph_copy = morph.copy()

    print("Start segmentation")
    count_x = np.zeros(shape=height)
    for y in range(height):
        for x in range(width):
            if bin_img[y][x] == pixel_set:
                count_x[y] += 1

    upper_lines, lower_lines = line_array(count_x)
    upperlines, lowerlines = refine_array(upper_lines, lower_lines)
    if len(lower_lines) > 0:
        lowerlines[-1] = min(lower_lines[-1], height - 1)

    if len(upperlines) == len(lowerlines):
        lines = []
        for y in upperlines:
            morph[y][:] = pixel_set
        for y in lowerlines:
            morph[y][:] = pixel_set
        for y in range(len(upperlines)):
            lines.append((upperlines[y], lowerlines[y]))
    else:
        return

    lines = np.array(lines)
    if len(lines) > 1:
        lines = [(lines[0][0], lines[len(lines) - 1][1])]
    no_of_lines = len(lines)

    for i in range(no_of_lines):
        lines_img.append(morph_copy[lines[i][0]:lines[i][1], :])
        base_img_lines.append(src_img[lines[i][0]:lines[i][1], :])

        count_y = np.zeros(shape=width)
        row_min_height = lines[i][0]
        row_max_height = lines[i][1]
        row_height = (row_max_height - row_min_height)
        row_start_height = int((row_max_height - row_min_height) * 0.60)
        count_y_top = np.zeros(shape=width)
        for y in range(row_height):
            for x in range(width):
                if lines_img[i][y][x] == pixel_set:
                    count_y[x] += 1
                    if y < row_start_height:
                        count_y_top[x] += 1

        for x in range(len(count_y_top)):
            if count_y_top[x] > 0:
                count_y[x] = row_height

        start_lines, end_lines = line_removal_array(count_y)
        startlines, endlines = refine_line_removal_array(start_lines, end_lines)
        if len(endlines) > 0:
            endlines[-1] = min(endlines[-1], width - 1)

        if len(startlines) == len(endlines):
            lines_in_lines = []
            for y in range(len(startlines)):
                if is_line_to_char(startlines[y], endlines[y], count_y):
                    lines_in_lines.append((startlines[y], endlines[y]))

            for line in lines_in_lines:
                for x in range(line[0], line[1]):
                    for y in range(row_start_height, row_height):
                        base_img_lines[i][y][x] = 255
                        lines_img[i][y][x] = 0

    contours, hierarchy = cv2.findContours(
        morph_copy, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    mean_letter_width = letter_width(contours)

    for i in range(len(lines_img)):
        x_lines.append(end_wrd_dtct(lines, i, bin_img, mean_letter_width, width, morph))

    for i in range(len(x_lines)):
        x_lines[i].append(width)

    for i in range(len(lines)):
        letter_segmentation(lines_img, x_lines, i, base_img_lines, dir_path)
