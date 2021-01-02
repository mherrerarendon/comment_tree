from ct.models.comment import Comment
from ct import db
from flask import Blueprint, send_from_directory, current_app, request, jsonify, Response

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('POST',))
def create_thread():
    req_payload = request.get_json()
    comment = Comment(username=req_payload['username'], content=req_payload['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify({'thread_id': comment.id}), 201

@bp.route('/thread/<thread_id>', methods=('GET',))
def get_thread(thread_id):
    payload = {}
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    if parent_comment:
        payload['thread_id'] = thread_id
        payload['comment'] = parent_comment.to_dict()
        recurse_threads = False if 'recursive' not in request.args else request.args['recursive']
        payload['thread'] = parent_comment.get_thread(recurse_threads)
        return jsonify(payload), 200
    else:
        return 'not found', 404

@bp.route('/thread/<thread_id>/comment', methods=('POST',))
def append_comment_to_thread(thread_id):
    req_payload = request.get_json()
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    if parent_comment:
        comment = Comment(username=req_payload['username'], content=req_payload['content'])
        parent_comment.thread.append(comment)
        db.session.commit()
        return jsonify({'comment_id': comment.id}), 201 
    else:
        return 'not found', 404

# TODO: editable db path in configuration (memory for tests and filesystem for server)