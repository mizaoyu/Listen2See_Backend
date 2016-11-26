from flask import Flask, Blueprint
import test

test = Blueprint('test', __name__)

@test.route('/', methods=['GET', 'POST'])
def get_info():
	return 'Test!'
