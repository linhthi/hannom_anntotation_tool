# import pymongo
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory
# from pymongo import message
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from torchvision.utils import save_image, make_grid

#from flask_jwt_extended import JWTManager, jwt_required, create_access_token
#from pymongo import MongoClient
#from bson.objectid import ObjectId
# from flask_jwt_extended import JWTManager, jwt_required, create_access_token
# from pymongo import MongoClient
# from bson.objectid import ObjectId
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
from tool import *
from normalize import Normalize
from collections import defaultdict
import json


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
#db = client["a"]
#fs = gridfs.GridFS(db)

# collection
#user = db["User"]
#book = db['Book']
#box_img = db['Box']
# # Making a Connection with MongoClient
# client = MongoClient("mongodb://localhost:27017/")

# # database
# db = client["a"]
# fs = gridfs.GridFS(db)

# # collection
# user = db["User"]
# book = db['Book']
# box_img = db['Box']

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)

#jwt = JWTManager(app)
# jwt = JWTManager(app)


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


# Example for using jwt 
# @app.route("/dashboard")
# @jwt_required()
# def dasboard():
#     return jsonify(message="Welcome! to the Dashboard!")


# @app.route("/api/user/signup", methods=["POST"])
# def signup():
#     email = request.json["email"]
#     test = user.find_one({"email": email})
#     if test:
#         return jsonify(message="User Already Exist"), 409
#     else:
#         first_name = request.json["first_name"]
#         last_name = request.json["last_name"]
#         password = request.json["password"]
#         user_info = dict(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
#         user.insert_one(user_info)
#         return jsonify(message="User added sucessfully"), 201


# @app.route("/api/user/signin", methods=["POST"])
# def signin():
#     if request.is_json:
#         email = request.json["email"]
#         password = request.json["password"]
#     else:
#         email = request.form["email"]
#         password = request.form["password"]

#     test = user.find_one({"email": email})
#     if check_password_hash(test['password'], password):
#         access_token = create_access_token(identity=email)
#         return jsonify(message="Login Succeeded!", 
#         access_token=access_token,
#         email=email,
#         name=test['first_name'] + " " + test['last_name']
#         ), 201
#     else:
#         return jsonify(message="Bad Email or Password"), 401


# @app.route('/api/user/logout/')
# def logout():
#     if 'email' in session:
#         sessions.pop('email', None)
#     return jsonify({'message': 'You successfully logged'})


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



# @app.route('/api/images/upload_old', methods=['GET', 'POST'])
# def upload_old():
#     file = request.files['inputFile']
#     user_id = request.form['user_id']
#     title = request.form['title']
    
#     contents = file.read()
#     book_id = str(uuid.uuid4())

#     book_info = dict(user_id=user_id,book_id=book_id, title=title, filename=file.filename, annotation=None)
#     book.insert_one(book_info)

#     fs.put(contents, filename=file.filename)
#     file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
#     return jsonify({'message': 'Upload file successful'}), 201


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


# @app.route('/api/images/uploads_old/<file_path>', methods=['GET'])
# def get_img_old(file_path):
#     """Get image preview, return image"""
#     if (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file_path))):
#         print("File has existed")

#     return send_from_directory(app.config['UPLOAD_FOLDER'], file_path, as_attachment=True)


@app.route('/api/images/uploads/<image_file>', methods=['GET'])
def get_img(image_file):
    """Get image preview, return image"""
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    if (os.path.exists(os.path.join(file_path, f'{image_file}.png'))):
        print("File has existed")
    return send_from_directory(file_path, f'{image_file}.png', as_attachment=True)

@app.route('/api/images/auto/<image_file>', methods=['POST'])
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
        characters_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{image_file}/characters')
        if os.path.isdir(characters_path) == False:
            os.mkdir(characters_path)
            characters_path = os.path.join(characters_path, f'img_{current_box["id"]}')
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


@app.route('/api/images/crop/<image_file>', methods=['GET'])
def crop_characters(image_file):
    # Read image
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], image_file)
    image_file_path = os.path.join(folder_path, image_file +'.png')
    img = Image.open(image_file_path)
    # img = image_to_byte_array(img)   

    # Read anntations from json
    image_file_json = os.path.join(folder_path, image_file +'.json')
    with open(image_file_json, 'r') as f:
        data = f.read()
    page_annotation = json.loads(data)
    bboxes = page_annotation["bboxes"] 

    # Crop all characters in image
    for box in bboxes:
        x_min, y_min, x_max, y_max = box['x_min'], box['y_min'], box['x_max'], box['y_max']
        print(x_min, y_min, x_max, y_max)
        img_box_crop = img.crop((x_min, y_min, x_max, y_max))

        # img_box_crop = cv2.resize(img_box_crop, (224, 224), interpolation = cv2.INTER_AREA)
        # img_box_crop = img_box_crop.resize((224, 224))
        characters_path = os.path.join(folder_path, f'characters/img_{box["id"]}')
        if os.path.isdir(characters_path) == False:
            os.mkdir(characters_path)   
        print(characters_path)
        img_box_crop.save(os.path.join(characters_path, f'img_{box["id"]}.png'))

    return jsonify({'message: crop successfull'})




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
@app.route('/smooth/<img_folder>/<target_img_name>', methods=['POST', 'GET'])
def show_img(target_img_name, img_folder):

    #path to specific file
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{img_folder}/characters/{target_img_name}')
    file_path = os.path.join(folder_path, f'{target_img_name}.png') #cropped image or original image
    json_path = os.path.join(folder_path, f'{target_img_name}.json') #json file
    f_smooth_path = os.path.join(folder_path, f'{target_img_name}_smooth.png') #smooth image
    concat_org_norm_path = os.path.join(folder_path, f'{target_img_name}_concat.png') #concat of original and normalize image

    img = cv2.imread(file_path,0) #cropped image or original image
    property_of_image = get_data_json_file(json_path, {"has_threshold":False, "size": img.shape, "no_cnts":-1, "threshold":127})
    global normalize_obj #empty obj


    if request.method == 'GET':
        print("-----------------GET-------------------")
        try:
           mocban_data = {}
           if property_of_image["has_threshold"]:
                    #load data to normalize_obj
                    all_contours = []
                    for i in range(property_of_image["no_cnts"]):
                        all_contours.append(np.array(property_of_image[f'cnt_{i}']))

                    normalize_obj.set_attributes(all_contours, property_of_image['size'], np.array(property_of_image['hierarchy']))

                    #update it to global normalize obj for later gaussian
                    concat_img = cv2.imread(concat_org_norm_path,0)
                    final_img = cv2.imread(f_smooth_path,0)
                    threshold_container = "none"
           else:
                    #---------------------------Threshold------------------------------
                    #update the value after threshold
                    normalize_obj, concat_img, final_img = create_threshold_image(img, 127, normalize_obj,
                                                                                         json_path,
                                                                                         concat_org_norm_path,
                                                                                         f_smooth_path)
                    threshold_container = "block"
           mocban_data = { 'filename': target_img_name,
                   'final_img': convert_img_to_base64(final_img),
                   'concat_org_f_img': convert_img_to_base64(concat_img),
                   'img_folder': img_folder,
                   'threshold_value': 127,
                   'threshold_container': threshold_container,
                   'has_threshold': property_of_image["has_threshold"]
                 }
        except Exception as e:
            print("Error at the GET request threshold: ", e)
        finally:
            return render_template('via.html', mocban_data=mocban_data)


    if request.method == 'POST':
        print("-----------------POST-------------------")
        try:
            request_data = request.get_json()
            threshold = int(request_data["threshold"])
            concat_img = cv2.imread(concat_org_norm_path,0)
            normalize_obj, concat_img, final_img = create_threshold_image(img, threshold, normalize_obj,
                                                                                          json_path,
                                                                                          concat_org_norm_path,
                                                                                          f_smooth_path)
            mocban_data = {
                     'final_img':convert_img_to_base64(final_img),
                     'concat_org_f_img':convert_img_to_base64(concat_img),
            }
        except Exception as e:
            print("Error at the POST request threshold: ", e)
        finally:
            return mocban_data

            
    
    
    

@app.route('/thresh/<img_folder>/<target_img_name>/<int:threshold>')
def change_threshold(target_img_name, img_folder, threshold):
        if request.method == 'POST':
            request_data = request.get_json()
            threshold = int(request_data["threshold"])


""" Recieving the gaussian value and make the change on the local line
    params:
    --id_img: ID of target image
    --region_id: ID of specific region in image

"""
@app.route('/gaussian/<img_folder>/<target_img_name>/<id_img>/<region_id>', methods=['POST', 'GET'])
def character_effect(id_img,region_id, target_img_name, img_folder):
    effect = "gaussian" # may be change later
    global normalize_obj
    if request.method == 'GET':
        return	{
                    "local_rate": 0,
                    "only_x": "True",
                    "only_y": "True",
                }

    if request.method == 'POST':
      try:
        #initialize value
        request_data = request.get_json()
        local = None # level of smoothing
        only_x = None # smoothing by the horizonal orientation
        only_y = None # smoothing by the vertical orientation
        all_points_x = request_data['attr']['all_points_x'] # x-coordinate of polygon
        all_points_y = request_data['attr']['all_points_y'] # y-coordinate of polygon



        local = int(request_data['local_rate'])
        only_x = True if request_data['only_x'].lower() == "true" else False
        only_y = True if request_data['only_y'].lower() == "true" else False

        #correct
        folder_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{img_folder}/characters/{target_img_name}')
        f_smooth_path = os.path.join(folder_path, f'{target_img_name}_smooth.png') #smooth image 
        _,normalized_shape,_,all_contours,_ = normalize_obj.get_attributes()
        
        print(normalized_shape, all_contours)
        #cnt_points_of_polygon contains: - index of contour in all_contours
        #                                - range of points in the index contour 
        cnt_points_of_polygon = []

        for index_of_cnt in range(len(all_contours)):
            r, mul_range = is_inside_contour_and_get_local_line(all_points_x,
                                                                all_points_y,
                                                                all_contours[index_of_cnt])
            if r:
                cnt_points_of_polygon.append([index_of_cnt, mul_range])


	#if length of mul_range > 0 then it means the range in contour if combine of 2 region line1(0-> unknown) and (unknown -> end)
        #print("cnt_points_of_polygon",cnt_points_of_polygon)
        for hcnt in cnt_points_of_polygon:
            index, mul_range = hcnt
            global_contours = all_contours[index].copy()
            g_contours = smoothing_line(global_contours, mul_range, False,
                                                          only_x,only_y,
                                                          local,normalized_shape)
                                               

        normalize_obj.update(False, index,g_contours)
        result_image = normalize_obj.convert_to_original_image()
        cv2.imwrite(f_smooth_path, result_image)
        
      except Exception as e:
        print("Error at smoothening: ", e, "do nothing to image and return it")
      finally:
        return send_from_directory(folder_path,  f'{target_img_name}_smooth.png', as_attachment=False)



@app.route('/finishEdit/<img_folder>/<target_img_name>', methods=['POST', 'GET'])
def finish_edit(target_img_name, img_folder):

    #----------------------------------save smooth changes into normalization -------------------           
    normalize_obj.update(True, None, None)
    
    return "success finish update normalization"
    
@app.route('/doneEdit/<img_folder>/<target_img_name>')
def done_edit(target_img_name, img_folder):

    #----------------------------------update into the json -------------------                    
    #update for json file
    #numpy can not be saved in json file
    #so need to convert contours and hierarchy to list 
    folder_path = os.path.join(app.config['UPLOAD_FOLDER'], f'{img_folder}/characters/{target_img_name}')  
    json_path = os.path.join(folder_path, f'{target_img_name}.json') #json file
    
    _,normalized_shape,hierarchy,all_contours,_ = normalize_obj.get_attributes()
    
    update_data_json_file(json_path, ['size', 'has_threshold', 'no_cnts', 'hierarchy'], [normalized_shape, True, len(all_contours), hierarchy.tolist()])
    for i in range(len(all_contours)):
        update_data_json_file(json_path, [f'cnt_{i}'], [all_contours[i].tolist()])
        
    return "success save changes into json file"
    


if __name__ == '__main__':
    app.run(host="localhost", debug=True)
