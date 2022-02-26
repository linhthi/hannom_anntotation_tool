# import pymongo
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory
# from pymongo import message
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
#from flask_jwt_extended import JWTManager, jwt_required, create_access_token
#from pymongo import MongoClient
#from bson.objectid import ObjectId
import os
#import gridfs
from detectors.DB import *
import easyocr
import numpy as np
import cv2
from PIL import Image
import io
import uuid
import json
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory, redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename
import json
import cv2
from PIL import Image
import io
import matplotlib.pyplot as plt
import numpy as np
import copy
from tool import is_inside_polygon,smoothing_line, is_inside_contour_and_get_local_line,convert_color_img,show_line_with_diff_color
from normalize import Normalize
import base64
from collections import defaultdict
import json
import mocban_pix2pix as model


basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
normalize_obj = Normalize()


def image_to_byte_array(image:Image):
  imgByteArr = io.BytesIO()
  image.save(imgByteArr, format=image.format)
  imgByteArr = imgByteArr.getvalue()
  return imgByteArr


# Making a Connection with MongoClient
#client = MongoClient("mongodb://localhost:27017/")

# 
base
#db = client["a"]
#fs = gridfs.GridFS(db)

# collection
#user = db["User"]
#book = db['Book']
#box_img = db['Box']

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)
#jwt = JWTManager(app)

# JWT Config
#app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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



# @app.route('/api/images', methods=['GET'])
# def getAllBook():
#     books = book.find()
#     books_ = []
#     for item in books:
#         temp = {
#             "book_id": item.get("book_id"),
#             "user_id": item.get("user_id"),
#             "name": item.get("filename"),
#             "width": item.get("width"),
#             "height": item.get("height")
#         }
#         books_.append(temp)
#     print(books_)
#     return jsonify(message="successful", results=books_), 200





@app.route('/api/images/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['inputFile']
    # user_id = request.form['user_id']
    # title = request.form['title']
    
    # contents = file.read()
    # book_id = str(uuid.uuid4())

    # book_info = dict(user_id=user_id,book_id=book_id, title=title, filename=file.filename, annotation=None)
    # book.insert_one(book_info)

    # fs.put(contents, filename=file.filename)
    path = os.path.join(app.config['UPLOAD_FOLDER'], (file.filename).split('.')[0])
    if os.path.isdir(path) == False:
        os.mkdir(path)
    file.save(os.path.join(path, file.filename))
    return jsonify({'message': 'Upload file successful'}), 201


@app.route('/api/images/uploads/<image_file>', methods=['GET'])
def get_img(image_file):
    """Get image preview, return image"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    if (os.path.exists(os.path.join(file_path, f'{image_file}.png'))):
        print("File has existed")
    return send_from_directory(file_path, f'{image_file}.png', as_attachment=True)


@app.route('/api/images/auto/<image_file>', methods=['GET'])
def save_annotation_and_label(image_file):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file + '/' + image_file +'.png')
    img = Image.open(file_path)
    img = image_to_byte_array(img)
    bboxes = detect_single_image(img)['bbox']
    image_file_json = image_file + '.json'
    detected_boxes = []
    height, width = None, None
    for box in bboxes:
        print("Sample box: {}".format(box))
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
        img_box_crop = cv2.resize(img_box_crop, (512, 512), interpolation = cv2.INTER_AREA)
        characters_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{image_file}/characters/img_{current_box["id"]}')
        if os.path.isdir(characters_path) == False:
            os.mkdir(characters_path)
        cv2.imwrite(os.path.join(characters_path, f'img_{current_box["id"]}.png'), img_box_crop)

    page = {
        "_id": str(uuid.uuid4()),
        "image_file": image_file,
        "height": height,
        "width": width,
        "bboxes": detected_boxes,
    }
    with open(os.path.join(app.config['UPLOAD_FOLDER'], image_file+'/'+image_file_json), 'w') as json_file:
        json.dump(page, json_file)
    return jsonify({'message': 'Label successfull'})


# @app.route('/api/images/autolabel/<img_id>', methods=['GET', 'POST'])
# def autolabel(img_id):
#     current_book = book.find_one({"_id": ObjectId(str(img_id))})
#     img_file = current_book['filename']
#     img_ = fs.find_one({'filename': img_file})
#     img = img_.read()
#     bboxes = detect_single_image(img)['bbox']
#     detected_boxes = []
#     for box in bboxes:
#         print("Sample box: {}".format(box))
#         img_box_crop, x_min, y_min, x_max, y_max, height, width  = get_box_img(box, img)
#         label_detect = detect_symbol(img_box_crop)
#         current_box = {
#             'id': str(uuid.uuid4()),
#             'label': label_detect,
#             'x_min': x_min.item(),
#             'y_min': y_min.item(),
#             'x_max': x_max.item(),
#             'y_max': y_max.item()
#         }
#         detected_boxes.append(current_box)
#         img_box_crop = cv2.resize(img_box_crop, (512, 512), interpolation = cv2.INTER_AREA)
#         cv2.imwrite(f'static/characters/img_{current_box["id"]}.png', img_box_crop)
    
#     book.update_one({"_id": ObjectId(str(img_id))}, {"$set": {"boxes": detected_boxes, "height": height, "width": width}})
#     return jsonify({'message': 'Label successfull'})

@app.route('/api/image/getlabel/<image_file>', methods=['GET'])
def getlabel(image_file):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file + '/' + image_file +'.json')
    with open(file_path, 'r') as f:
        data = f.read()
    obj = json.loads(data)
    return jsonify(message="successful", data=obj), 200

# @app.get('/api/image/label/<imag_file>', methods=['POST'])
# def saveLabel(image_file):
#     data = request.json['data']
#     file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file + '/' + image_file + '.json')
#     with open(file_path, 'w') as f:
#         json.dump(data, f)

#     return jsonify(message="Save successfull", data=data), 200

@app.route('/api/images', methods=['GET'])
def getAllImages():
    images = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        d = os.path.join(app.config['UPLOAD_FOLDER'], file)
        if os.path.isdir(d):
            print(d)
            temp = {
            "id": file,
            "user_id": 1,
            "filename": file,
            }
            images.append(temp)
    return jsonify(message="successful", data=images), 200


### Lam
@app.route('/smooth/<img_folder>/<target_img_name>')
def show_img(target_img_name, img_folder):
    path = os.path.join(app.config['UPLOAD_FOLDER'], f'{img_folder}/characters/{target_img_name}')
    model.config['TEST_DIR'] = path
    model.val_dataset = model.MapDataset(root_dir=model.config['TEST_DIR'],augmentation=model.eval_augmentation)
    model.val_loader = model.DataLoader(model.val_dataset, batch_size=1, shuffle=False)

    model.test(model.gen, model.val_loader, path)
    file_path = os.path.join(path, f'{target_img_name}.png')
    img = cv2.imread(file_path,0)
    normalized_pred_img = normalize_obj.preprocess_img(img)
    img_base64 = "data:image/png;base64," + base64.b64encode(cv2.imencode('.png', normalized_pred_img)[1]).decode()
    mocban_data = {'filename':target_img_name,
                'img':img_base64,
                'img_folder': img_folder
            }
    return render_template('via.html', mocban_data=mocban_data)

@app.route('/imgs/<img_name>')
def get_img_chacracter(img_name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], img_name, as_attachment=False )


""" Recieving the gaussian value and make the change on the local line
    params:
    --id_img: ID of target image
    --region_id: ID of specific region in image
    --highlight: whether just show image or make a change
"""
@app.route('/<highlight>/gaussian/<img_folder>/<target_img_name>/<id_img>/<region_id>', methods=['POST', 'GET'])
def upload_image(id_img,region_id, target_img_name, highlight, img_folder):
    effect = "gaussian" # may be change later
    path = os.path.join(os.getcwd(), 'dataOfEffect.json')
    content = {
        id_img: {
            effect: [
                {
                    "local_rate": 0,
                    "only_x": "True",
                    "only_y": "True",
                }
            ]
        }
    }
    if request.method == 'GET':
        with open(path, 'r+') as jsonFile:
            #check if file is empty
            if os.path.getsize(path) == 0:

                jsonFile.write(str(json.dumps(content,indent=2)))
                return content[id_img][effect][0]
            else:
                all_data = json.loads(jsonFile.read())
                if id_img not in all_data:
                    all_data[id_img] = content[id_img]
                    #print("all_data: ", all_data)
                    jsonFile.seek(0)
                    json.dump(all_data, jsonFile, indent=2)
                    return jsonify(all_data[id_img][effect][int(region_id)])
                array_of_region_data = all_data[id_img][effect]

                if int(region_id) + 1 > len(all_data[id_img][effect]):
                    array_of_region_data.append({"local_rate": 0,
                                                 "only_x": "True",
                                                 "only_y": "True",
                                                 })
                    jsonFile.seek(0)
                    json.dump(all_data,jsonFile,indent=2)
            return jsonify(array_of_region_data[int(region_id)])

        return "Error reading file"

    if request.method == 'POST':

        #initialize value
        request_data = request.get_json()
        highlight = True if highlight.lower() == "true" else False
        local = None
        only_x = None
        only_y = None
        all_points_x = request_data['attr']['all_points_x']
        all_points_y = request_data['attr']['all_points_y']

        # with open(path, 'r+') as jsonFile:
        #     all_data = json.loads(jsonFile.read())
        #
        #     # only show the highlight line
        #     if not highlight:
        #         array_of_region_data = all_data[id_img][effect]
        #         data_of_region_id = array_of_region_data[int(region_id)]
        #
        #         # update data in json file
        #         data_of_region_id['local_rate'] = request_data['local_rate']
        #         data_of_region_id['only_x'] = request_data['only_x']
        #         data_of_region_id['only_y'] = request_data['only_y']
        #
        #     jsonFile.seek(0)
        #     json.dump(all_data, jsonFile, indent=2)
        #     jsonFile.truncate()

        #update in image
        # Testing new feature without reading from a file
        if not highlight:
            local = int(request_data['local_rate'])
            only_x = True if request_data['only_x'].lower() == "true" else False
            only_y = True if request_data['only_y'].lower() == "true" else False

        #correct
        path = os.path.join(app.config['UPLOAD_FOLDER'], f'{img_folder}/characters/{target_img_name}')
        _,normalized_shape,_,all_contours,_ = normalize_obj.get_attributes()
        highlight_contour = []

        for index_of_cnt in range(len(all_contours)):
            r, mul_range = is_inside_contour_and_get_local_line(all_points_x,
                                                                all_points_y,
                                                                all_contours[index_of_cnt])
            if r:
                highlight_contour.append([index_of_cnt, mul_range])



        print("highlight_contour",highlight_contour)
        for hcnt in highlight_contour:
            index, mul_range = hcnt
            global_contours = all_contours[index].copy()
            g_contours = smoothing_line(global_contours, mul_range, False,
                                                          only_x,only_y,
                                                          local,normalized_shape,highlight)

        if not highlight:
            normalize_obj.update(False, index,g_contours)

        result_image = normalize_obj.convert_to_original_image()
        cv2.imwrite(path, result_image)
        return send_from_directory(app.config['UPLOAD_FOLDER'],  f'{img_folder}/characters/{target_img_name}', as_attachment=False)



@app.route('/finishEdit/<filename>/', methods=['POST', 'GET'])
def finish_edit(filename):
    normalize_obj.update(True, None, None)
    path = os.path.join(app.config['CHARACTERS'], filename)
    result_img = normalize_obj.convert_to_original_image()
    cv2.imwrite(path, result_img)
    return send_from_directory(app.config['CHARACTERS'], filename, as_attachment=False)





if __name__ == '__main__':
    app.run(host="localhost", debug=True)
    

if __name__ == '__main__':
    app.run(host="localhost", debug=True)
