import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter1d

"""This comment is for two function below
        Two functions below will check whether the coordinate (px, py)
        is inside the polygon which is defined by set of two coordinates

        The algorithm is actually copy from via.html produced by the author
        Check it for more information

        :param 
            --all_points_x: holds the set of x coordinate of polygon
            --all_points_y: holds the set of y coordinate of polygon
            --px: current mouse down x coordinate
            --py: current mouse down y coordinate

        :return
            whether px,py in or out the contour 

    """
def is_left(x0,y0,x1,y1,x2,y2):
    return (((x1 - x0) * (y2 - y0)) - ((x2 - x0) * (y1 - y0)))

def is_inside_polygon(all_points_x, all_points_y, px, py):
    if len(all_points_x) == 0 or len(all_points_y) == 0:
        return 0
    wn = 0
    n = len(all_points_x)
    for i in range(n-1):
        is_left_value = is_left( all_points_x[i], all_points_y[i],
                                 all_points_x[i+1], all_points_y[i+1],
                                 px, py)
        if all_points_y[i] <= py:
            if all_points_y[i + 1] > py and is_left_value > 0:
                wn += 1
        else:
            if all_points_y[i+1]  <= py and is_left_value < 0:
                wn -= 1

    is_left_value  = is_left(all_points_x[n-1], all_points_y[n-1],
                               all_points_x[0], all_points_y[0],
                               px, py)
    if all_points_y[n - 1] <= py:
        if all_points_y[0] > py and is_left_value > 0:
            wn += 1
    else:
        if all_points_y[0] <= py and is_left_value < 0:
            wn -= 1

    if wn == 0:
        return 0
    else:
        return 1

def is_inside_contour_and_get_local_line(all_points_x, all_points_y, contours):
    """This function to find out which coordinates of contours are inside the polygon region
                :param
                    --contours: A specific contour of generated by contours[index]
                    --all_points_x: holds the set of x coordinate of polygon
                    --all_points_y: holds the set of y coordinate of polygon
                :return
                    True, False: in or out in the region
                    mul_range: if in, from where to where in contour
                """
    start_cnt = None
    end_cnt = None
    index = 0
    previous = 0
    mul_range = []
    new_line = False
    # len(list_contours(contours)))
    activate = True
    this_local_line_may_consist_two_range = 0
    #do not accept multiple
    for i, cnt in enumerate(list_contours(contours)):
        px, py = cnt
        if is_inside_polygon(all_points_x, all_points_y, px, py) == 1 :
            if new_line == False:
                new_line = True
                start_cnt = i
                end_cnt = i
            else:
                end_cnt = i

            if i == 0 or i == len(list_contours(contours)) - 1:
                this_local_line_may_consist_two_range += 1
        else:
            if new_line == True:
                new_line = False
                mul_range.append([start_cnt, end_cnt])
                start_cnt = None
                end_cnt = None

    if start_cnt is not None and end_cnt is not None:
        mul_range.append([start_cnt, end_cnt])


    if len(mul_range) == 0:
        return False, None
    else:
        #filter the range
        temp_mul_range = []
        if this_local_line_may_consist_two_range > 1:
            for i,r in enumerate(mul_range):
                if i == 0 or i == len(mul_range) -1 :
                    temp_mul_range.append(r)
            return True, temp_mul_range[::-1]
        else:
            temp_mul_range.append(mul_range[-1])
            return True, temp_mul_range


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
        val = cnt[0]
        img[val[1], val[0], 1] = 255
        # blank[val[1], val[0], 1] = 255
    # plt.imshow(img, cmap='gray')
    # plt.show()
    return img


def smoothing_line(global_line_contours, mul_range, visualize, smoothenByX, smoothenByY, local_rate,
                   img_shape, highlight):
    """ This function emphasizes on smoothing specific region of the random line

          :param
          --global_line_contours: contours points of the whole line
          --local_line_contours: contours points of the regional line
          --ranging: range of contours of local line in global line
          --rate: how much user want to smoothen
          --smoothenByX: only smoothing by the X coordinate
          --smoothenByY: only smoothing by the Y coodinate
          --highlight: just show the local line with different color

         :return
            result_img: numpy image has been smoothened
            new_global_line: numpy contour has been smoothened
        """

    local_line_x = []
    local_line_y = []
    for r in mul_range:
        start, end = r
        x, y = extract_coordinate_from_contours(global_line_contours[start:end])
        local_line_x.extend(x)
        local_line_y.extend(y)


    if highlight:
        print("highlight")

    else:
        # Smoothing only for local line
        global_line_x, global_line_y = extract_coordinate_from_contours(global_line_contours)
        new_local_line_y = gaussian_filter1d(local_line_y, local_rate)
        new_local_line_x = gaussian_filter1d(local_line_x, local_rate)

        new_local_line = [[list(a)] for a in zip(new_local_line_y, new_local_line_x)]
        new_local_line = np.asarray(new_local_line)
        start_local_line = 0
        end_local_line = 0
        for r in mul_range:
            start_global_line, end_global_line = r
            start_local_line = end_local_line
            distance = abs(start_global_line - end_global_line)
            end_local_line = start_local_line + distance
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
        noChanne = [0,1,2]
    for color_index in noChannel:
        np_rgb_color[np_rgb_color[:, :, color_index] == 0, color_index] = 255
    return np_rgb_color


def list_contours(contours):
    list = []
    max_len = 0
    for cnt in contours:
        for p in cnt:
            list.append(p)
    return list



