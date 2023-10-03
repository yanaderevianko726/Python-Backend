
import cv2
import os
import json
import shutil
import base64
import numpy as np
import face_recognition

from flask import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

host_name = 'localhost'
port_number = 5000

known_path = os.path.join(os.getcwd(), "C:\\Users\\Public\\Pictures\\known_faces\\")
unknown_path = os.path.join(os.getcwd(), "C:\\Users\\Public\\Pictures\\unknown_faces\\")
    

@app.route('/')
def index():
    return render_template("index.html")

took_photo = 'images/sample_photo.jpeg'
took_file = 'images/file1.txt'
dir_img = "C:\\Users\\Public\\Pictures\\"

@app.route('/take_photo', methods=['POST'])
def take_photo():

    data = request.get_json()

    b64_string = data['b64string']
    img_name = data['imgname']

    txt1 = open(took_file, 'w')
    txt1.write(b64_string)
    txt1.close()

    file1 = open(took_file, 'rb')
    encoded_data = file1.read()
    file1.close()
    
    decoded_data = base64.b64decode((encoded_data))

    jpeg_path = f'{dir_img}{img_name}.jpeg'
    isExisting = os.path.exists(jpeg_path)

    if isExisting:
        img_file = open(jpeg_path, 'wb')
        img_file.write(decoded_data)
        img_file.close()
    else:
        dest = shutil.copyfile(took_photo, jpeg_path)

        img_file = open(jpeg_path, 'wb')
        img_file.write(decoded_data)
        img_file.close()

    os.remove(f'{took_file}')

    resp = jsonify({
        "status": 200
    })

    return resp

@app.route('/new_user', methods=['POST'])
def new_user():

    data = request.get_json()

    staff_name = data['username']
    gender = data['gender']
    birthday = data['birthday']
    imgname = data['imgname']

    img_path = f'{dir_img}{imgname}.jpeg'

    user_data = {
        'staff_name' : staff_name,
        'birthday' : birthday,
        'image_path': img_path,
        'gender': gender
    }

    tmp_users = []
    tmp_users.append(user_data)
    
    with open(f'user_data.json', 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)            
        d_users = data['users']        
        
        for i, d_user in enumerate(d_users):
            tmp_users.append(d_user)

        json_file.close()
    
    users_json = {
        'users' : tmp_users
    }

    with open(f'user_data.json', 'w', encoding='utf-8') as f:
        f.write(json.dumps(users_json))
        f.close()

        resp = jsonify({
            "status": 200
        })

        return resp


@app.route("/login_user", methods=['GET'])
def login_user():

    user_name = request.args.get("user_name")    
    password = request.args.get("password")    
            
    return ''


if __name__ == '__main__':

    app.run(debug=True)
