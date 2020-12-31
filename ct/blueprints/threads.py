from flask import Blueprint, send_from_directory, current_app, request, jsonify, Response

from ct.models.thread import Thread
from ct.models.comment import Comment
from ct import db

bp = Blueprint('threads', __name__, url_prefix='/threads')

@bp.route('/thread', methods=('POST',))
def create_thread():
    thread = Thread()
    db.session.add(thread)
    db.session.commit()
    return jsonify({'thread_id': thread.id}), 201

@bp.route('/thread/<thread_id>', methods=('GET',))
def get_thread(thread_id):
    payload = {}
    thread = Thread.query.filter_by(id=thread_id).first()
    if thread:
        payload['thread_id'] = thread_id
        
        # TODO: order by date
        comments = Comment.query.filter_by(thread_id=thread_id)
        payload['comments'] = [{'username': comment.username, 'content': comment.content} for comment in comments]
        return jsonify(payload), 200
    else:
        return 'not found', 404

@bp.route('/thread/<thread_id>/comment', methods=('POST',))
def add_comment_to_thread(thread_id):
    req_payload = request.get_json()
    thread = Thread.query.filter_by(id=thread_id).first()
    if thread:
        comment = Comment(username=req_payload['username'], content=req_payload['content'])
        thread.comments.append(comment)
        db.session.commit()
        return jsonify({'comment_id': comment.id}), 201 
    else:
        return 'not found', 404