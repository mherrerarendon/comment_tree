from flask import Blueprint, send_from_directory, current_app, request, jsonify, Response

from ct.models.thread import Thread
from ct import db

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('GET', 'POST'))
def create_thread():
    if request.method == 'POST':
        thread = Thread()
        db.session.add(thread)
        db.session.commit()
        return jsonify({'thread_id': thread.id}), 201