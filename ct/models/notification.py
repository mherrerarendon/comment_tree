from ct import db
from ct.models.user import User
from ct.models.comment import Comment

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
    # seen bool
    user = db.relationship('User')
    comment = db.relationship('Comment')

    def to_dict(self):
        pass

    @staticmethod
    def clear_old_notifications():
        pass

    @staticmethod
    def get_comment_notifications(user_id):
        notifications = Notification.query.filter_by(user_id=user_id)
        comments = [n.comment for n in notifications]
        unique_threads = set([c.parent_id for c in comments])
        notifications_by_thread = {}
        for unique_thread in unique_threads:
            thread_comments = [c.to_dict() for c in comments if c.parent_id == unique_thread]
            notifications_by_thread[unique_thread] = thread_comments
        return notifications_by_thread

    @staticmethod
    def create_comment_notifications(comment):
        parent_comment = Comment.query.filter_by(id=comment.parent_id).first()
        user_id_list = parent_comment.get_user_ids_in_thread()
        user_id_list.remove(comment.user_id) # We don't want to add a notification for the user that made the comment.
        for user_id in user_id_list:
            n = Notification(user_id=user_id, comment_id=comment.id)
            db.session.add(n)
        db.session.commit()
