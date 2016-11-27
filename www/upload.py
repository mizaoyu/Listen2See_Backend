import os
import requests
from flask import Blueprint, request, redirect, url_for, jsonify
from flask import current_app as app
from flask_socketio import send, emit
import wave
import urllib, urllib3
import base64
from io import BytesIO
import re
import speech_recognition as sr
from flask.ext.cors import CORS, cross_origin



upload = Blueprint('upload', __name__)
r = sr.Recognizer()
speaker = ''
text = ''

# def get_token():  
# 	apiKey = "Y9Kw05g3OOfYAYcyg1S4qvcL"  
# 	secretKey = "c65dd0e07c6b8a4223a9e7403073d2cb"  

# 	auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" + apiKey + "&client_secret=" + secretKey;  

# 	res = urllib3.urlopen(auth_url)  
# 	json_data = res.read()  
# 	return json.loads(json_data)['access_token']  

# def dump_res(buf):  
# 	print(buf) 


# ## post audio to server  
# def use_cloud(token):  
# 	fp = wave.open('./public/audio/daoshort.wav', 'rb')  
# 	nf = fp.getnframes()  
# 	f_len = nf * 2  
# 	audio_data = fp.readframes(nf)  

# 	cuid = "wfnuser"
# 	srv_url = 'http://vop.baidu.com/server_api' + '?cuid=' + cuid + '&token=' + token  
# 	http_header = [  
# 		'Content-Type: audio/pcm; rate=1600',  
# 		'Content-Length: %d' % f_len  
# 	]  

# 	c = pycurl.Curl()  
# 	c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode  
# 	#c.setopt(c.RETURNTRANSFER, 1)  
# 	c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict  
# 	c.setopt(c.POST, 1)  
# 	c.setopt(c.CONNECTTIMEOUT, 30)  
# 	c.setopt(c.TIMEOUT, 30)  
# 	c.setopt(c.WRITEFUNCTION, dump_res)  
# 	c.setopt(c.POSTFIELDS, audio_data)  
# 	c.setopt(c.POSTFIELDSIZE, f_len)  
# 	c.perform() #pycurl.perform() has no return val

@upload.route('/audio', methods=['GET', 'POST'])
def audio():
	if request.method == 'POST':
		file = request.files['file']
		if file:
			filename = file.filename
			file.save(os.path.join(app.config['UPLOAD_AUDIO_FOLDER'], filename))
			# output = os.popen('./www/getVoiceDocument.sh') # Todo: write a python client for bing speech & rewrite the popen into embeded code
			output = os.popen('python ./Cognitive-SpeakerRecognition-Python/Identification/IdentifyFile.py 77798739fb73418a8fb7315fb05e5442 ./public/audio/'+filename+' True 7bdceff1-e2d0-4b7f-9317-5d075296d571 413d94ab-9075-4b52-89e3-386bf82374a4 0a0660cc-9bdf-40cb-abeb-c25114931b18 cdac6b07-09ff-4aa8-aa6f-33cd14effe2a')
			tmpstr = output.read()
			print(tmpstr)
			regex = r"(?<=Identified Speaker = ).*"
			matches = re.findall(regex, tmpstr)
			documentId = matches[0]
			print(documentId)
			print(filename)
			WAV_FILE = os.path.join(app.config['UPLOAD_AUDIO_FOLDER'], filename)
			if (documentId == 'cdac6b07-09ff-4aa8-aa6f-33cd14effe2a'):
				speaker = "Peng"
			else:
				speaker = app.config['VOICE_DOCUMENTS'][documentId]
			print(speaker)
			with sr.WavFile(WAV_FILE) as source:
				for off in range(int(source.DURATION/10)):
					audio = r.record(source, duration=10)
					try:
						text = r.recognize_sphinx(audio)
						fo = open("foo.txt", "r+")
						fo.write(speaker+"\n"+text)
						fo.close()
						print("Audio says:::::::: \n" + text)
					except sr.UnknownValueError:
						print("Could not understand audio")

			# token = get_token()  
			# use_cloud(token)  
			# headers = {"Content-type": "application/x-www-form-urlencoded","Content-Length": "0", "Ocp-Apim-Subscription-Key": "c24b0bb50e8944fd941e9fceeffc602f"}
			# url = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"
			# r = requests.post(url, headers=headers)
			# print(r.text)

			# fp = wave.open('./public/audio/daoshort.wav')
			# nf = fp.getnframes()
			# f_len = nf * 2
			# audio_data = fp.readframes(nf)
			# http_header = [
			# 	'Content-type': 'audio/wav; codec="audio/pcm"; samplerate=16000',
			# 	'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzY29wZSI6Imh0dHBzOi8vc3BlZWNoLnBsYXRmb3JtLmJpbmcuY29tIiwic3Vic2NyaXB0aW9uLWlkIjoiNTI3MmFjNGRhZDRmNGIzZDlkZWZlNmU2ZTY5MDcxODgiLCJwcm9kdWN0LWlkIjoiQmluZy5TcGVlY2guUHJldmlldyIsImNvZ25pdGl2ZS1zZXJ2aWNlcy1lbmRwb2ludCI6Imh0dHBzOi8vYXBpLmNvZ25pdGl2ZS5taWNyb3NvZnQuY29tL2ludGVybmFsL3YxLjAvIiwiYXp1cmUtcmVzb3VyY2UtaWQiOiIiLCJpc3MiOiJ1cm46bXMuY29nbml0aXZlc2VydmljZXMiLCJhdWQiOiJ1cm46bXMuc3BlZWNoIiwiZXhwIjoxNDgwMTg0Mzc2fQ.jCCjH2ukJwAT_UfXTKPCqqgsut7fJQWqkh3PS-pd6F4' 
			# ]
			# http_url = 'https://speech.platform.bing.com/recognize?scenarios=smd&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5version=3.0&format=json'
			# c = pycurl.Curl()
			# c.setopt(pycurl.URL, str(srv_url)) #curl doesn't support unicode
			# #c.setopt(c.RETURNTRANSFER, 1)
			# c.setopt(c.HTTPHEADER, http_header)   #must be list, not dict
			# c.setopt(c.POST, 1)
			# c.setopt(c.CONNECTTIMEOUT, 30)
			# c.setopt(c.TIMEOUT, 30)
			# c.setopt(c.WRITEFUNCTION, dump_res)
			# c.setopt(c.POSTFIELDS, audio_data) 
			# c.setopt(c.POSTFIELDSIZE, f_len)
			# c.perform() #pycurl.perform() has no return val  
			# print(wave.open('./public/audio/daoshort.wav').read())
# "https://speech.platform.bing.com/recognize?scenarios=smd&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=your_locale&device.os=your_device_os&version=3.0&format=json&instanceid=your_instance_id&requestid=your_request_id" -H 'Authorization: Bearer your_access_token' -H 'Content-type: audio/wav; codec="audio/pcm"; samplerate=16000' --data-binary @your_wave_file
# 			nheaders = {"Content-type": "application/x-www-form-urlencoded","Content-Length": "0", "Ocp-Apim-Subscription-Key": "c24b0bb50e8944fd941e9fceeffc602f"}
# 			nurl = "https://speech.platform.bing.com/recognize?scenarios=smd&appid=D4D52672-91D7-4C74-8AD8-42B1D98141A5&locale=your_locale&device.os=your_device_os&version=3.0&format=json&instanceid=your_instance_id&requestid=your_request_id"
# 			nr = requests.post(nurl, nheaders=headers)
# 			print(nr.text)
			

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


@upload.route('/getspeak', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def getSpeak():
	result = list()
	fo = open("foo.txt", "r+")
	for line in fo.readlines():                          #依次读取每行  
		line = line.strip()                             #去掉每行头尾空白  
		if not len(line) or line.startswith('#'):       #判断是否是空行或注释行  
			continue                                    #是的话，跳过不处理  
		result.append(line) 
	fo.close()
	if request.method == 'GET':
		if(len(result)>=2):
			return jsonify({'error': 'false', 'speaker': result[0], 'text': result[1]})
		else:
			return jsonify({'error': 'true'})
		
@upload.route('/text', methods=['GET', 'POST'])
def text():
	if request.method == 'POST':
		data = request.data
		if data:
			return data


