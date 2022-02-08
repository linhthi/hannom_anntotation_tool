import cv2
import numpy as np
import matplotlib.pyplot as plt
from tool import convert_color_img

class Normalize:
    def __init__(self):
        self.contours = None
        self.result_img_shape = None
        self.no_of_contour = None
        self.hierarchy = None
        self.previous_cnt = None

    def set_attributes(self, cnt, shape, hierarchy):
        self.contours = list(cnt)
        self.result_img_shape = shape
        self.hierarchy = hierarchy
        self.original_contours = list(cnt)
        self.previous_cnt = list(cnt)

    def get_attributes(self):
        return self.contours, self.result_img_shape, self.hierarchy,\
               self.original_contours, self.previous_cnt

    def update(self, prev, index_cnt,new_cnt_of_int):
        if prev is False:
            self.previous_cnt = self.contours.copy()
            self.contours[index_cnt] = new_cnt_of_int
        else:
            self.contours = self.previous_cnt


    def shift_image(self,img, x, y):
        """
            Pad into image to center of character is center of image
            :param img: cv2 binary image
            :param x: x_center_of_image - x_center_of_character
            :param y: y_center_of_image - y_center_of_character
            :return: Padded image that center of character lies on center of image
            """
        x_abs = int(round(abs(x), 0))
        y_abs = int(round(abs(y), 0))
        if x < 0 and y < 0:
            pad_img = cv2.copyMakeBorder(img, top=y_abs, bottom=0, left=x_abs, right=0, borderType=cv2.BORDER_CONSTANT,
                                         value=0)
        elif x < 0 and y > 0:
            pad_img = cv2.copyMakeBorder(img, top=y_abs, bottom=0, left=0, right=x_abs, borderType=cv2.BORDER_CONSTANT,
                                         value=0)
        elif x > 0 and y < 0:
            pad_img = cv2.copyMakeBorder(img, top=0, bottom=y_abs, left=x_abs, right=0, borderType=cv2.BORDER_CONSTANT,
                                         value=0)
        else:
            pad_img = cv2.copyMakeBorder(img, top=0, bottom=y_abs, left=0, right=x_abs, borderType=cv2.BORDER_CONSTANT,
                                         value=0)
        return pad_img

    def padding_and_hold_ratio(self,cv_img):
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

    def list_contours(self,contours):
        list = []
        max_len = 0
        for cnt in contours:
            for p in cnt:
                list.append(p)
        return list


    def filter_much_small_contour(self, bin_img, contours, hierarchy=None, min_area=70):
        """
        Remove hole on character, hole outside character, lines that have the zero area
        """
        mask = np.ones(bin_img.shape[:2], dtype="uint8")
        inv_mask = np.ones(bin_img.shape[:2], dtype="uint8")
        total_mask = np.ones(bin_img.shape[:2], dtype="uint8")
        new_contours = []
        for index, contour in enumerate(contours):
            if int(cv2.contourArea(contour)) == 0:
                # lines are created some points(area = 0)
                for point in contour:
                    bin_img[point[0][1], point[0][0]] = 0
            elif 0 < cv2.contourArea(contour) < min_area:
                # hole in character
                if hierarchy[0][index][3] != -1:
                    cv2.drawContours(inv_mask, [contour], -1, 0, -1)
                    # plt.imshow(inv_mask, cmap='gray')
                    # plt.show()
                # hole out in character
                else:
                    cv2.drawContours(mask, [contour], -1, 0, -1)
            else:
                new_contours.append(contour)
        bin_img = cv2.bitwise_and(bin_img, bin_img, mask=cv2.resize(mask, bin_img.shape))
        bin_img = cv2.bitwise_or(bin_img, 1 - inv_mask, mask=cv2.resize(total_mask, bin_img.shape))
        return bin_img, self.list_contours(new_contours)


    def crop_char(self,thresh, contours):
        """
        Crop image based on contours, find the most top, bot, left, right points
        :param thresh: binary image
        :param contours: list of contours
        :return: crop of original image that contains character
        """
        xmax = max(i[0][0] for i in contours)
        xmin = min([i[0][0] for i in contours])
        ymax = max(i[0][1] for i in contours)
        ymin = min([i[0][1] for i in contours])
        image = thresh[max(0, ymin - 2):ymax, max(0, xmin - 2):xmax]
        return image


    def find_center(self,list2, mask):
        # scipy.ndimage.measurements.center_of_mass¶
        """
        Find center of the character(mask)
        :param list2: list of contours
        :param mask: mask indicates the position of character
        :return: center of character
        """
        # cnts = cv2.drawContours(mask, list2, -1, (0, 255, 0), 1)

        kpCnt = len(list2)

        x = 0
        y = 0

        for kp in list2:
            x = x + kp[0][0]
            y = y + kp[0][1]

        return x / kpCnt, y / kpCnt  # x_center, y_center

    def normalize_mask(self,thresh):
        """
        Get character image and shift center of character to center of image(a part of image can be disappeared)
        :param thresh: binary image
        :return: image that contain image, and center of image is center of character
        """
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        thresh, contours = self.filter_much_small_contour(thresh, contours, hierarchy)
        thresh = self.crop_char(thresh, contours)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        x_center, y_center = self.find_center(self.list_contours(contours), thresh)
        shifted_img = self.shift_image(thresh, thresh.shape[1] / 2 - x_center, thresh.shape[0] / 2 - y_center)

        # plt.imshow(cv2.circle(cv2.cvtColor(thresh, cv2.COLOR_GRAY2RGB), (int(x_center), int(y_center)), 10, (255, 0, 0), 1), cmap='gray')
        return self.padding_and_hold_ratio(shifted_img)

    def convert_color_img(self,img, color):
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

    def padding_to_original_size(self,img, original_size):
        """
          Adding padding to image to turn it to original size
          :param img: target image
          :param original_size: tuple of size image want to transfer
        """
        height_img, width_img = img.shape
        height_org, width_org = original_size
        delta_height = abs(height_img - height_org)
        delta_width = abs(width_img - width_org)

        pad_img = cv2.copyMakeBorder(img, top=int(delta_height / 2), bottom=delta_height - int(delta_height / 2), \
                                     left=int(delta_width / 2), right=delta_width - int(delta_width / 2), \
                                     borderType=cv2.BORDER_CONSTANT,
                                     value=0)
        return pad_img

    def preprocess_img(self,cv_img, threshold=110):
        """
        Combine the above functions to crop character area
        cv_img: cv bgr img
        threshold: threshold to convert bgr to binary image
        """

        ret, bin_print_img = cv2.threshold(cv_img, threshold, 1, cv2.THRESH_BINARY_INV)
        normalized_print_img = self.normalize_mask(bin_print_img)
        normalized_print_img = self.padding_to_original_size(normalized_print_img, cv_img.shape)
        # normalized_print_img is image of filled contour
        contours, hierarchy = cv2.findContours(normalized_print_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        self.set_attributes(contours, normalized_print_img.shape, hierarchy)
        #print("len(contours)",len(contours))
        return 255 - normalized_print_img*255

    def convert_to_original_image(self):
        blank = np.zeros(self.result_img_shape, dtype=np.uint8)
        blank = cv2.drawContours(blank, self.contours, -1, 255, -1)
        return 255 - blank

