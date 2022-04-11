import os
from detectors.DB import *
import easyocr
import numpy as np
import cv2
from PIL import Image
import io
import uuid
import json
import numpy as np
import copy
from collections import defaultdict
import time



def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Easy_OCR
reader = easyocr.Reader(['ch_tra'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_JSON_detect(d,box):
    region = {
        "shape_attributes": {
          "name": "polygon",
          "all_points_x": [
            float(box[0][0]),
            float(box[1][0]),
            float(box[2][0]),
            float(box[3][0])
          ],
          "all_points_y": [
            float(box[0][1]),
            float(box[1][1]),
            float(box[2][1]),
            float(box[3][1])
          ]
        },
        "region_attributes": {
          "name": d
        }
      }
    return region

def to_JSON(regions,img_name,size):


    res = {
        img_name: {
            "filename": img_name,
            "size": size,
            "regions": regions,
            "file_attributes": {}
          }
        }

    return res

def detect_symbol(filename):
    detect = None
    output = reader.readtext(filename)
    if(output != []):
        if(output[0][1] != ''):
            detect = output[0][1]

    return detect


def get_box_img(box, image):
    img = Image.open(io.BytesIO(image))
    width, height = img.size
    img = np.array(img)
    b = np.array(box, dtype=np.int16)
    xmin = np.min(b[:, 0])
    ymin = np.min(b[:, 1])
    xmax = np.max(b[:, 0])
    ymax = np.max(b[:, 1])
    crop_img = img[ymin:ymax, xmin:xmax, :].copy()

    return crop_img, xmin, ymin, xmax, ymax, height, width

def save_annotation_and_label(image_folder):
    """
    Auto annotate Han-Nom characters and label them follow images_folder
    contain all images
    """
    for image_file in os.listdir(image_folder):
        start = time.time()
        print("Processing at image: {}".format(image_file))
        file_path = os.path.join(image_folder, image_file + '/' + image_file +'.png')
        img = Image.open(file_path)
        img = image_to_byte_array(img)
        try:
            bboxes = detect_single_image(img)['bbox']
        except RuntimeError:
            pass
        image_file_json = image_file + '.json'
        detected_boxes = []
        height, width = None, None
        for box in bboxes:
            img_box_crop, x_min, y_min, x_max, y_max, height, width  = get_box_img(box, img)
            label_detect = detect_symbol(img_box_crop)
            current_box = {
                'id': str(uuid.uuid4()),
                'label': label_detect,
                'x_min': x_min.item(),
                'y_min': y_min.item(),
                'x_max': x_max.item(),
                'y_max': y_max.item()
            }
            detected_boxes.append(current_box)

        page = {
            "_id": str(uuid.uuid4()),
            "image_file": image_file,
            "height": height,
            "width": width,
            "bboxes": detected_boxes,
        }
        with open(os.path.join(image_folder, image_file+'/'+image_file_json), 'w') as json_file:
            json.dump(page, json_file)
        end = time.time()
        print("Finish on image: {}, number of characters detect: {}".format(image_file, len(detected_boxes)))
        print("Executation time: {}".format(end - start))
    
def save_annotation_and_label_file(image_folder, image_file):
    """
    Auto annotate Han-Nom characters and label them follow image_file in images_folder
    """
    file_path = os.path.join(image_folder, image_file + '/' + image_file +'.png')
    img = Image.open(file_path)
    img = image_to_byte_array(img)
    bboxes = detect_single_image(img)['bbox']
    image_file_json = image_file + '.json'
    detected_boxes = []
    height, width = None, None
    for box in bboxes:
        img_box_crop, x_min, y_min, x_max, y_max, height, width  = get_box_img(box, img)
        label_detect = detect_symbol(img_box_crop)
        current_box = {
            'id': str(uuid.uuid4()),
            'label': label_detect,
            'x_min': x_min.item(),
            'y_min': y_min.item(),
            'x_max': x_max.item(),
            'y_max': y_max.item()
        }
        detected_boxes.append(current_box)

    page = {
        "_id": str(uuid.uuid4()),
        "image_file": image_file,
        "height": height,
        "width": width,
        "bboxes": detected_boxes,
    }
    with open(os.path.join(image_folder, image_file+'/'+image_file_json), 'w') as json_file:
        json.dump(page, json_file)
    print("Finish on image: {}, number of characters detect: {}".format(image_file, len(detected_boxes)))

if __name__ == '__main__':
    IMAGE_FOLDER = './static/uploads/tt4/'
    save_annotation_and_label(IMAGE_FOLDER)
    # save_annotation_and_label_file(IMAGE_FOLDER, '01702_mk22')