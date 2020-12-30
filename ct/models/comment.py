from ct import db

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f'<user: {self.username} content: {self.content}>'