from ct import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    thread = db.relationship('Comment', lazy=True)

    def __repr__(self):
        return f'<user: {self.username} content: {self.content}>'