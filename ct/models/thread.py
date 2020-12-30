from ct import db

class Thread(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<ID: {self.id}>'