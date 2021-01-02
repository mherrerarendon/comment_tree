from ct.models.comment import Comment
from ct import db
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
        comment = do_add_comment_to_thread(parent_comment, request.get_json())
        if get_query_arg(request.args, 'notify', arg_defaults):
            add_notification_for_relevant_users(parent_comment)
        return jsonify(comment.to_dict()), 201 
    else:
        return 'not found', 404

def do_add_comment_to_thread(parent_comment, req_payload):
    comment = Comment(username=req_payload['username'], content=req_payload['content'])
    parent_comment.thread.append(comment)
    db.session.commit()
    return comment

def add_notification_for_relevant_users(parent_comment, comment):
    relevant_users = [parent_comment.username].extend([c.username for c in parent_comment.thread])
    relevant_users = set(relevant_users)
    for user in relevant_users:
        add_notification(user, comment)
    return relevant_users

def add_notification(user, comment):
    print(f'Notifying {user} about new comment')

# TODO: editable db path in configuration (memory for tests and filesystem for server)