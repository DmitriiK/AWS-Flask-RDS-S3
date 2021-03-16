#!./flask/Scripts/python
from flask import Flask, jsonify, abort, request, redirect, render_template
import os
import urllib.request
from werkzeug.utils import secure_filename

import rdb_store as rdb

UPLOAD_FOLDER = 'D:/share'
ALLOWED_EXTENSIONS = set([ 'png', 'jpg', 'jpeg', 'gif'])
app = Flask(__name__)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('index.html')


@app.route('/file_upload', methods=['POST'])
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
		filename = secure_filename(file.filename)
		file.save(os.path.join(UPLOAD_FOLDER, filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are  png, jpg, jpeg, gif'})
		resp.status_code = 400
		return resp

@app.route('/test_rdb_connect', methods=['GET'])
def test_rdb_connect():
    result =rdb.test_connect()
    return result  

@app.route('/get_images_list', methods=['GET'])
def get_images_list():
    result =rdb.get_s3_files()
    return result    

if __name__ == '__main__':
    app.run(debug=True)
