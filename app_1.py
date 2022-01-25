import pymongo
from flask import Flask, jsonify, request, session, sessions, flash, send_file, url_for, send_from_directory
from pymongo import message
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
import gridfs
from detectors.DB import *
import easyocr
import numpy as np
import cv2
from PIL import Image
import io
import uuid


# Making a Connection with MongoClient
client = MongoClient("mongodb://localhost:27017/")

# database
db = client["a"]
fs = gridfs.GridFS(db)

# collection
user = db["User"]
book = db['Book']
box_img = db['Box']

basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)
jwt = JWTManager(app)

# JWT Config
app.config["JWT_SECRET_KEY"] = "this-is-secret-key"
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
@app.route("/dashboard")
@jwt_required()
def dasboard():
    return jsonify(message="Welcome! to the Dashboard!")


@app.route("api/user/signup", methods=["POST"])
def signup():
    email = request.json["email"]
    test = user.find_one({"email": email})
    if test:
        return jsonify(message="User Already Exist"), 409
    else:
        first_name = request.json["first_name"]
        last_name = request.json["last_name"]
        password = request.json["password"]
        user_info = dict(first_name=first_name, last_name=last_name, email=email, password=generate_password_hash(password))
        user.insert_one(user_info)
        return jsonify(message="User added sucessfully"), 201


@app.route("/api/user/signin", methods=["POST"])
def signin():
    if request.is_json:
        email = request.json["email"]
        password = request.json["password"]
    else:
        email = request.form["email"]
        password = request.form["password"]

    test = user.find_one({"email": email})
    if check_password_hash(test['password'], password):
        access_token = create_access_token(identity=email)
        return jsonify(message="Login Succeeded!", 
        access_token=access_token,
        email=email,
        name=test['first_name'] + " " + test['last_name']
        ), 201
    else:
        return jsonify(message="Bad Email or Password"), 401


@app.route('/api/user/logout/')
def logout():
    if 'email' in session:
        sessions.pop('email', None)
    return jsonify({'message': 'You successfully logged'})


@app.route('/api/images', methods=['GET'])
def getAllBook():
    books = book.find()
    books_ = []
    for item in books:
        temp = {
            "book_id": item.get("book_id"),
            "user_id": item.get("user_id"),
            "name": item.get("filename"),
            "width": item.get("width"),
            "height": item.get("height")
        }
        books_.append(temp)
    print(books_)
    return jsonify(message="successful", results=books_), 200



@app.route('/api/images/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['inputFile']
    user_id = request.form['user_id']
    title = request.form['title']
    
    contents = file.read()
    book_id = str(uuid.uuid4())

    book_info = dict(user_id=user_id,book_id=book_id, title=title, filename=file.filename, annotation=None)
    book.insert_one(book_info)

    fs.put(contents, filename=file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return jsonify({'message': 'Upload file successful'}), 201

@app.route('/api/images/uploads/<file_path>', methods=['GET'])
def get_img(file_path):
    """Get image preview, return image"""
    if (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file_path))):
        print("File has existed")

    return send_from_directory(app.config['UPLOAD_FOLDER'], file_path, as_attachment=True)


@app.route('/api/images/annotate/<book_id>', methods=['GET', 'POST'])
def annotate(book_id):
    img_id = book_id
    img_file = book.find_one({"_id": ObjectId(str(img_id))})

    img_ = fs.find_one({'filename': img_file['filename']})
    img = img_.read()
    bbox = detect_single_image(img)['bbox']

    book.update_one({"_id": ObjectId(str(img_id))}, {"$set": {"boxes": bbox}})

    return jsonify({'message': 'Get annotion successful'}, {"bbox": bbox}), 200

@app.route('/api/images/autolabel/<img_id>', methods=['GET', 'POST'])
def autolabel(img_id):
    current_book = book.find_one({"_id": ObjectId(str(img_id))})
    img_file = current_book['filename']
    img_ = fs.find_one({'filename': img_file})
    img = img_.read()
    bboxes = detect_single_image(img)['bbox']
    detected_boxes = []
    for box in bboxes:
        print("Sample box: {}".format(box))
        img_box_crop, x_min, y_min, x_max, y_max, height, width  = get_box_img(box, img)
        label_detect = detect_symbol(img_box_crop)
        current_box = {
            'id': uuid.uuid4(),
            'label': label_detect,
            'x_min': x_min.item(),
            'y_min': y_min.item(),
            'x_max': x_max.item(),
            'y_max': y_max.item()
        }
        detected_boxes.append(current_box)
    
    book.update_one({"_id": ObjectId(str(img_id))}, {"$set": {"boxes": detected_boxes, "height": height, "width": width}})
    return jsonify({'message': 'Label successfull'})


if __name__ == '__main__':
    app.run(host="localhost", debug=True)