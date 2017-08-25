from lib import db

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<Entry id={id} name={name!r}>'.format(
            id=self.id, name=self.namme)

def init():
    db.create_all()
