import os
from flask import Flask
from flask_socketio import SocketIO
from www.test import test
from www.upload import upload
from flask.ext.cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app, resources={r"/update/getspeak": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
app.register_blueprint(test, url_prefix='/test')
app.register_blueprint(upload, url_prefix='/upload')
app.debug = True
app.config.from_pyfile('config.py')
socketio = SocketIO(app)

@socketio.on('test')
def handle_test_message(message):
    print('received message: ' + message['data'])
    socketio.emit('testresponse', {'data': 'success'})

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0')