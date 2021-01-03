from ct import db
from ct.models.notification import Notification
from ct.blueprints.utils import get_query_arg
from flask import Blueprint, request, jsonify, Response

bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@bp.route('/user/<user_id>', methods=('GET',))
def get_notifications_for_user(user_id):
    notifications = Notification.get_comment_notifications(user_id)
    return jsonify(notifications), 200
