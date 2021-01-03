from ct import db
from ct.models.comment import Comment
from ct.models.notification import Notification
from ct.blueprints.utils import get_query_arg
from flask import Blueprint, send_from_directory, current_app, request, jsonify, Response

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('POST',))
def create_thread():
    req_payload = request.get_json()
    comment = Comment(username=req_payload['username'], content=req_payload['content'])
    db.session.add(comment)
    db.session.commit()
    return jsonify(comment.to_dict()), 201

@bp.route('/thread/<thread_id>', methods=('GET',))
def get_thread(thread_id):
    arg_defaults = {'recursive': False}
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    if parent_comment:
        payload = {'comment': parent_comment.to_dict()}
        recurse_threads = get_query_arg(request.args, 'recursive', arg_defaults)
        payload['thread'] = parent_comment.get_thread(recurse_threads)
        return jsonify(payload), 200
    else:
        return 'not found', 404

@bp.route('/thread/<thread_id>/comment', methods=('POST',))
def append_comment_to_thread(thread_id):
    arg_defaults = {'notify': False}
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    if parent_comment:
        with_notification = get_query_arg(request.args, 'notify', arg_defaults)
        comment = do_add_comment_to_thread(parent_comment, request.get_json())
        if with_notification:
            Notification.create_comment_notifications(comment)
        return jsonify(comment.to_dict()), 201 
    else:
        return 'not found', 404

def do_add_comment_to_thread(parent_comment, req_payload):
    comment = Comment(username=req_payload['username'], content=req_payload['content'])
    parent_comment.add_comment_to_thread(comment)
    return comment

# TODO: editable db path in configuration (memory for tests and filesystem for server)