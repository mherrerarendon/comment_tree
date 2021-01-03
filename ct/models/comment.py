from ct import db
from ct.models.user import User
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    time_stamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    thread = db.relationship('Comment', lazy=True)
    user = db.relationship('User')

    def __repr__(self):
        return f'<user: {self.user.username} content: {self.content}>'

    def to_dict(self, recursive=False):
        d = {
            'id': self.id,
            'parent_id': self.parent_id,
            'username': self.user.username, 
            'content': self.content,
            'time_stamp': self.time_stamp
        }
        if recursive:
            d['thread'] = self.get_thread()
        return d

    def get_thread(self, recursive=False):
        comments = self.thread
        if len(comments) > 0:
            comments.sort(key=lambda c : c.time_stamp)
            return [comment.to_dict(recursive) for comment in comments]
        else:
            return []

    def get_user_ids_in_thread(self):
        user_ids = [self.user_id]
        user_ids.extend([c.user_id for c in self.thread])
        return set(user_ids)

    def add_comment_to_thread(self, comment):
        self.thread.append(comment)
        db.session.commit()  
