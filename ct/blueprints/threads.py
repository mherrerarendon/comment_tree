from ct import db
from ct.models.comment import Comment
from ct.models.notification import Notification
from ct.models.user import User
from ct.blueprints.utils import get_query_arg
from flask import Blueprint, request, jsonify, Response

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('POST',))
def create_thread():
    req_payload = request.get_json()
    user = User.query.filter_by(username=req_payload['username']).first()
    comment = Comment(user=user, content=req_payload['content'])
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
    req_payload = request.get_json()
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    user = User.query.filter_by(username=req_payload['username']).first()
    if parent_comment and user:
        with_notification = get_query_arg(request.args, 'notify', arg_defaults)
        comment = do_add_comment_to_thread(parent_comment, user, req_payload)
        if with_notification:
            Notification.create_comment_notifications(comment)
        return jsonify(comment.to_dict()), 201 
    else:
        return 'not found', 404

def do_add_comment_to_thread(parent_comment, user, req_payload):
    comment = Comment(user=user, content=req_payload['content'])
    parent_comment.add_comment_to_thread(comment)
    return comment
