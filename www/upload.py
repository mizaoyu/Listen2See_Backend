import os
import requests
from flask import Blueprint, request, redirect, url_for
from flask import current_app as app
from flask_socketio import send, emit

upload = Blueprint('upload', __name__)

@upload.route('/audio', methods=['GET', 'POST'])
def audio():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_AUDIO_FOLDER'], filename))
			output = os.popen('./www/getVoiceDocument.sh')
			print(output.read())
			headers = {"Content-type": "application/x-www-form-urlencoded","Content-Length": "0", "Ocp-Apim-Subscription-Key": "c24b0bb50e8944fd941e9fceeffc602f"}
			url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
			r = requests.post(url, headers=headers)
			print(r.text)
			return 'success'
	return '''
	<!doctype html>
	<title>Upload new File</title>
	<h1>Upload new File</h1>
	<form action="" method=post enctype=multipart/form-data>
	<p><input type=file name=file>
	<input type=submit value=Upload>
	</form>
	'''

@upload.route('/text', methods=['GET', 'POST'])
def text():
	if request.method == 'POST':
		data = request.data
		if data:
			return data


