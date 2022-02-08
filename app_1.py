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


basedir = os.path.abspath(os.path.dirname(__file__))
uploads_path = os.path.join(basedir, 'uploads')

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['UPLOAD_FOLDER_CHARACTER'] = 'static/characters'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
normalize_obj = Normalize()

@app.route('/home')
def home():
    return "Hello World"


#### Linh
@app.route('/api/images/uploads/<file_path>', methods=['GET'])
def get_img(file_path):
    """Get image preview, return image"""
    if (os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], file_path))):
        print("File has existed")

    return send_from_directory(app.config['UPLOAD_FOLDER'], file_path, as_attachment=True)


### Lam
@app.route('/show_imgs/<target_img_name>')
def show_img(target_img_name):
    path = os.path.join(app.config['UPLOAD_FOLDER_CHARACTER'], target_img_name)
    img = cv2.imread(path,0)
    normalized_pred_img = normalize_obj.preprocess_img(img)
    img_base64 = "data:image/png;base64," + base64.b64encode(cv2.imencode('.png', normalized_pred_img)[1]).decode()
    mocban_data = {'filename':target_img_name,
                'img':img_base64
            }
    return render_template('via.html', mocban_data=mocban_data)

@app.route('/imgs/<img_name>')
def get_img_chacracter(img_name):
    return send_from_directory(app.config['UPLOAD_FOLDER_CHARACTER'],img_name, as_attachment=False )


""" Recieving the gaussian value and make the change on the local line
    params:
    --id_img: ID of target image
    --region_id: ID of specific region in image
    --highlight: whether just show image or make a change
"""
@app.route('/<highlight>/gaussian/<filename>/<id_img>/<region_id>', methods=['POST', 'GET'])
def upload_image(id_img,region_id, filename, highlight):
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
        path = os.path.join(app.config['UPLOAD_FOLDER_CHARACTER'], filename)
        all_contours,normalized_shape,_,_,_ = normalize_obj.get_attributes()
        highlight_contour = []

        for index_of_cnt in range(len(all_contours)):
            r, mul_range = is_inside_contour_and_get_local_line(all_points_x,
                                                                              all_points_y,
                                                                              all_contours[index_of_cnt],
                                                                              )
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
        return send_from_directory(app.config['UPLOAD_FOLDER_CHARACTER'], filename, as_attachment=False)

@app.route('/revertImage/<filename>/', methods=['POST', 'GET'])
def revert_image(filename):
    normalize_obj.update(True, None, None)
    path = os.path.join(app.config['UPLOAD_FOLDER_CHARACTER'], filename)
    result_img = normalize_obj.convert_to_original_image()
    cv2.imwrite(path, result_img)
    return send_from_directory(app.config['UPLOAD_FOLDER_CHARACTER'], filename, as_attachment=False)





if __name__ == '__main__':
    app.run(host="localhost", debug=True)