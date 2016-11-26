from flask import Blueprint

upload = Blueprint('upload', __name__)

@upload.route('/audio', methods=['GET', 'POST'])
def audio():
	return 'Test!'

@upload.route('/text', methods=['GET', 'POST'])
def text():
	return 'Test!'

