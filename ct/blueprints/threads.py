from flask import Blueprint, send_from_directory, current_app

bp = Blueprint('thread', __name__, url_prefix='/thread')

@bp.route('/', methods=('GET', 'POST'))
def create_thread():
    pass