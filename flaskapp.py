#!./flask/Scripts/python
from flask import Flask, jsonify, abort, request, redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename
#from imageio import imread

import s3
import rdb_store as rdb

UPLOAD_FOLDER = 'D:/share'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template('index.html')


@app.route('/api/v1.0/file_upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    if 'file' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
    file = request.files['file']
    if file.filename == '':
        resp = jsonify({'message' : 'No file selected for uploading'})
        resp.status_code = 400
        return resp
    if file and allowed_file(file.filename):
        url=s3.upload_file_stream(file)
        rdb.set_s3_files(file.filename, url)       
        #file.save(os.path.join(UPLOAD_FOLDER, filename))
        resp = jsonify({'message' : 'File successfully uploaded'})
        resp.status_code = 201
        return resp
    else:
        resp = jsonify({'message' : 'Allowed file types are  png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp

@app.route('/api/v1.0/test_rdb_connect', methods=['GET'])
def test_rdb_connect():
    result =rdb.test_connect()
    return result  

@app.route('/api/v1.0/get_images_list', methods=['GET'])
def get_images_list():
    result =rdb.get_s3_files()
    return result  

@app.route('/api/v1.0/get_random_image', methods=['GET'])
def get_random_image():
    url =rdb.get_single_s3_file()
    return redirect(url)    
    ##image = imread(url)

@app.route('/api/v1.0/get_image_by_name', methods=['POST'])
def get_image_by_name():
    file_name=request.form['fname']
    if file_name == '':
        resp = jsonify({'message' : 'enter file name please'})
        resp.status_code = 400
        return resp
    url =rdb.get_single_s3_file(file_name)
    return redirect(url)  

@app.route('/api/v1.0/get_instanse_path', methods=['GET'])
def get_instanse_path():
    return app.instance_path   

if __name__ == '__main__':
    app.run(debug=True)
