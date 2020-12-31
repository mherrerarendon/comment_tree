from flask import Blueprint, send_from_directory, current_app, request, jsonify, Response

# from ct.models.thread import Thread
from ct.models.comment import Comment
from ct import db

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('POST',))
def create_thread():
    req_payload = request.get_json()
    comment = Comment(username=req_payload['username'], content=req_payload['content'])
    db.session.add(comment)
    db.session.commit()
    # old
    # thread = Thread(id=1)
    # db.session.add(thread)
    # db.session.commit()
    return jsonify({'thread_id': comment.id}), 201

@bp.route('/thread/<thread_id>', methods=('GET',))
def get_thread(thread_id):
    payload = {}
    parent_comment = Comment.query.filter_by(id=thread_id).first()
    if parent_comment:
        payload['thread_id'] = thread_id
        payload['comments'] = [{'username': parent_comment.username, 'content': parent_comment.content}]
        
        # TODO: order by date
        comments = Comment.query.filter_by(parent_id=thread_id)
        payload['comments'].extend([{'username': comment.username, 'content': comment.content} for comment in comments])
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

@bp.route('/thread/<thread_id>/comment/<comment_id>', methods=('POST',))
def branch_comment(thread_id, comment_id):
    pass
