from flask import Blueprint

test = Blueprint('test', __name__)

@test.route('/', methods=['GET', 'POST'])
def get_info():
	return 'Test!'
