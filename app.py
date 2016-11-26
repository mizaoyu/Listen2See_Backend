import os
from flask import Flask
from www.routes import test

app = Flask(__name__)
app.register_blueprint(test, url_prefix='/test')
app.debug = True

if __name__ == '__main__':
	app.run(host='0.0.0.0')