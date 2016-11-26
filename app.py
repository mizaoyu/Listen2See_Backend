import os
from flask import Flask
from www.test import test
from www.upload import upload

app = Flask(__name__)
app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(upload, url_prefix='/upload')
app.debug = True

if __name__ == '__main__':
	app.run(host='0.0.0.0')