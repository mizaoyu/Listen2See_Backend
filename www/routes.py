from flask import Blueprint

test = Blueprint('test', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def test():
	return 'Test!'
