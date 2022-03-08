import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d
import os
import json
import base64
from pathlib import Path
import torch
import mocban_pix2pix as pix2pix
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def create_a_polygon(all_points_x, all_points_y):
    polygon_coordinate = []
    for i in range(len(all_points_x)):
        polygon_coordinate.append((all_points_x[i], all_points_y[i]))
    polygon = Polygon(polygon_coordinate)
    return polygon


def is_inside_polygon(all_points_x, all_points_y, contours):
    """This function help check the contours whether are in the polygon
        param:
            --all_points_x: polygon x coordinates
            --all_points_y: polygon y coordiantes
            --contours: all_contours[index]
        return:
            True: points are found inside polygon
            False: no points are found inside polygon
            range_of_all_line_of_contours_in_polygon: contains the range=[start_point, end_point]
                                                    : length is usually equal 1
                                                    : length = 2 meaning there are two range
                                                            [start of cnt ->point inside polygon]
                                                            [point inside polygon -> end of cnt]
        NOTE: line and range represents [start_point, end_point] inside the contour
    """
    polygon = create_a_polygon(all_points_x, all_points_y)
    set_of_points_in_cnt = list_contours(contours) # transfer shape (n0_points, xn, yn) -> [(x1,x2),..(xn, yn)]
    range_of_all_line_of_contours_in_polygon = []
    i = 0
    while i < len(set_of_points_in_cnt):
        px, py = set_of_points_in_cnt[i]  # coordinate of point
        if polygon.contains(Point(px, py)): # check if points inside the polygon
            start_of_new_line = i
            end_of_new_line = i
            range_of_new_line = [start_of_new_line]
            while end_of_new_line < len(set_of_points_in_cnt):
                px, py = set_of_points_in_cnt[end_of_new_line]  # coordinate of point
                if polygon.contains(Point(px, py)):
                    end_of_new_line += 1
                else:
                    break

            range_of_new_line.append(end_of_new_line)
            range_of_all_line_of_contours_in_polygon.append(range_of_new_line)
            i = end_of_new_line
        i += 1

    if len(range_of_all_line_of_contours_in_polygon) > 0:
        # has found line inside this contour inside polygon
        return True, range_of_all_line_of_contours_in_polygon
    else:
        # no line is found inside this contour inside polygon
        return False, range_of_all_line_of_contours_in_polygon



def extract_coordinate_from_contours(contours):
    """
          This function seperate the array contour into two part. One part only contains x coordinate
          the other contains y coordinate
          :param
            --contours: the contour line
          :return
            x_coordinate: array of x coordinates
            y_coordinate: array of y coordinates
        """

    x_coordinate = []
    y_coordinate = []
    for cnt in contours:
        coordinate = cnt[0]
        x_coordinate.append(coordinate[1])
        y_coordinate.append(coordinate[0])

    return [x_coordinate, y_coordinate]


def show_line_with_diff_color(img, contours, color='r'):
    """This function is to hightlight to secific region of the line
            :param
                --contours: contour of the line
                --image: the image that want to motify
                --color: color of the secific region
            :return
                img: image with the highlight region in contour
    """

    # blank = np.zeros(img.shape, dtype=np.uint8)
    for cnt in contours:
        val = cnt
        img[val[1], val[0]] = 255
        # blank[val[1], val[0], 1] = 255
    # plt.imshow(img, cmap='gray')
    # plt.show()
    return img


def smoothing_line(global_line_contours, mul_range, smoothen_x, smoothen_y, local_rate):
    """ This function emphasizes on smoothing specific region of the random line

          :param
          --global_line_contours: contours[index]
          --local_line_contours: contours[index][start:end]
          --smoothen_x: only smoothing by the X coordinate
          --smoothen_y: only smoothing by the Y coodinate

         :return
            new_global_line: numpy contour has been smoothened
        """
    # do nothing to global line
    if local_rate == 0:
        return global_line_contours

    # --------- Unpack coordinate to separate array x=[x1, x2, x3,...], y = [y1, y2, y3, ...] -------
    local_line_x = []
    local_line_y = []
    # reason for reversed
    # mul_range may contain 2 range,[(0 -> point inside polygon), (point inside polygon -> end of cnt)]
    # cnt must be consecutive

    for r in reversed(mul_range):
        start, end = r
        x, y = extract_coordinate_from_contours(global_line_contours[start:end])
        local_line_x.extend(x)
        local_line_y.extend(y)

    # Smoothing only for local line
    new_local_line_x, new_local_line_y = local_line_x, local_line_y
    if smoothen_y is True:
        new_local_line_y = gaussian_filter1d(local_line_y, local_rate)
    if smoothen_x is True:
        new_local_line_x = gaussian_filter1d(local_line_x, local_rate)

    # ----- pack them again after gaussian [[(x1,y1)], [(x2,y2)], ....]]
    new_local_line = [[list(a)] for a in zip(new_local_line_y, new_local_line_x)]
    new_local_line = np.asarray(new_local_line)
    start_local_line = 0
    end_local_line = 0
    for r in reversed(mul_range):
        start_global_line, end_global_line = r # global_line

        # local line
        start_local_line = end_local_line
        distance = abs(start_global_line - end_global_line)
        end_local_line = start_local_line + distance

        # blend the new local line into the global line
        global_line_contours[start_global_line:end_global_line] = new_local_line[start_local_line:end_local_line]

    return global_line_contours


def convert_color_img(img, color):
    """
    Convert color of character of binary image [0, 255]
    :param img: cv2 binary image
    :param color: 'r'/'b'/'g': convert to red/blue/green
    :return: numpy color image
    """
    cv_rgb_img = cv2.cvtColor(img.astype(np.uint8), cv2.COLOR_GRAY2RGB)
    np_rgb_color = np.array(cv_rgb_img)
    noChannel = []
    if color == 'r':
        noChannel.append(0)
    elif color == 'g':
        noChannel.append(1)
    elif color == 'b':
        noChannel.append(2)
    else:
        noChanne = [0, 1, 2]
    for color_index in noChannel:
        np_rgb_color[np_rgb_color[:, :, color_index] == 0, color_index] = 255
    return np_rgb_color


def get_data_json_file(path, content):
    Path(path).touch(exist_ok=True)  # create file if not exist
    if Path(path).stat().st_size == 0:
        with open(path, 'w') as f:
            f.write(json.dumps(content))
    else:
        with open(path, 'r') as f:
            content = json.loads(f.read())

    return content


def update_data_json_file(path, keys, values):
    with open(path, 'r') as f:
        content = json.loads(f.read())

    # length of keys and value is equal
    for i in range(len(keys)):
        content[keys[i]] = values[i]

    with open(path, 'w') as f:
        f.write(json.dumps(content))


def list_contours(contours):
    """ This function help union all the points in contours into one list
          :param
          --contours: all contours

          :return
             list contains all points in contours
    """
    list = []
    max_len = 0
    for cnt in contours:
        for p in cnt:
            list.append(p)
    return list


def convert_img_to_base64(img):
    """ This function help union all the points in contours into one list
          :param
          --img: numpy image

          :return
             image in base64 form
    """
    img_base64 = "data:image/png;base64," + base64.b64encode(cv2.imencode('.png', img)[1]).decode()
    return img_base64


def padding_and_hold_ratio(cv_img):
    h, w = cv_img.shape[:2]
    if h < w:
        diff = w - h
        top_pad = diff // 2
        bot_pad = diff - top_pad
        padded_img = cv2.copyMakeBorder(cv_img, top_pad, bot_pad, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    else:
        diff = h - w
        left_pad = diff // 2
        right_pad = diff - left_pad
        padded_img = cv2.copyMakeBorder(cv_img, 0, 0, left_pad, right_pad, borderType=cv2.BORDER_CONSTANT,
                                        value=(0, 0, 0))
    return padded_img


def concat_org_and_norm_imgs(org_img, norm_img):
    o_h, _ = org_img.shape
    n_h, _ = norm_img.shape

    delta_h = max(o_h, n_h) - min(o_h, n_h)
    if o_h < n_h:
        org_img = cv2.copyMakeBorder(org_img, top=delta_h // 2, bottom=(delta_h - (delta_h // 2)), left=0, right=0,
                                     borderType=cv2.BORDER_CONSTANT,
                                     value=255)

    else:
        norm_img = cv2.copyMakeBorder(norm_img, top=delta_h // 2, bottom=(delta_h - (delta_h // 2)), left=0, right=0,
                                      borderType=cv2.BORDER_CONSTANT,
                                      value=255)

    return cv2.hconcat([org_img, norm_img])


def concat_images_with_diff_size(img, ratio):
    h, w = img.shape
    max_size = [int(ratio[-1] * h), int(w * ratio[-1])]
    imgs = []

    for r in ratio:
        shape_for_img = [int(h * r), int(w * r)]
        ratio_img = cv2.resize(img, shape_for_img, interpolation=cv2.INTER_AREA)
        ratio_img = padding_to_specific_size(ratio_img, max_size, 255)
        imgs.append(ratio_img)

    return cv2.hconcat(imgs)


def padding_to_specific_size(img, specific_size, v):
    """
        Adding padding to image to turn it to original size
             :param img: target image
             :param specific_size: tuple of size image want to transfer, and it must greater than img.shape 
	"""
    height_img, width_img = img.shape
    height_org, width_org = specific_size
    delta_height = abs(height_img - height_org)
    delta_width = abs(width_img - width_org)

    pad_img = cv2.copyMakeBorder(img, top=int(delta_height / 2), bottom=delta_height - int(delta_height / 2), \
                                 left=int(delta_width / 2), right=delta_width - int(delta_width / 2), \
                                 borderType=cv2.BORDER_CONSTANT,
                                 value=v)
    return pad_img


def create_threshold_image(img, threshold, normalize_obj, concat_path, f_smooth_path):
    # ---------------------------Handle Image------------------------------
    # 3 mains step normalize -> pix2pix -> normalize
    # size of image has some small change, preprocess_img just threshold and adjust to center
    # keep track of this size_ratio_with_org_img for later concat image
    first_normalize_img = normalize_obj.preprocess_img(img, threshold, "first")
    size_ratio_with_org_img = first_normalize_img.shape

    # pix2pix model to smoothen img and read image in tensor form in pytorch
    # create size [1, 1, height, width]
    first_normalize_img = np.expand_dims(first_normalize_img, axis=2)
    tensor_normalized_img = torch.unsqueeze(pix2pix.eval_augmentation(image=first_normalize_img)["image"], dim=0).to(
        "cuda") # image has been resized to 512x512

    y_fake = pix2pix.gen(tensor_normalized_img) * 0.5 + 0.5  # normalize image
    y_fake = torch.reshape(y_fake, (y_fake.shape[2], y_fake.shape[3]))
    y_fake = y_fake.cpu().detach().numpy() * 255

    # threshold hold and adjust, size of image just a little small 512
    second_normalize_img = normalize_obj.preprocess_img(y_fake.astype(np.uint8), threshold, "second")

    # create concat image
    # original image and first_normalize image
    img_ratio_with_org_img = cv2.resize(second_normalize_img, size_ratio_with_org_img, interpolation=cv2.INTER_AREA)
    concat_org_first_image = concat_org_and_norm_imgs(img, img_ratio_with_org_img)

    cv2.imwrite(concat_path, concat_org_first_image)
    cv2.imwrite(f_smooth_path, second_normalize_img)

    return normalize_obj, concat_org_first_image, second_normalize_img

