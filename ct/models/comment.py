from ct import db
import datetime

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    time_stamp = db.Column(db.DateTime, unique=False, nullable=False, default=datetime.datetime.utcnow)
    thread = db.relationship('Comment', lazy=True)
    

    def __repr__(self):
        return f'<user: {self.username} content: {self.content}>'

    def to_dict(self, recursive=False):
        d = {
            'id': self.id,
            'parent_id': self.parent_id,
            'username': self.username, 
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
