from lib import db

class User (db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))
    password = db.Column(db.String(20))

    def __repr__(self):
        return '<User id={id} name={name!r}>'.format(
            id=self.id, name=self.name)



class HyperLapse (db.Model):
    __tablename__ = 'hyperlapse'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    start_latlng1 = db.Column(db.Float)
    start_latlng2 = db.Column(db.Float)
    end_latlng1 = db.Column(db.Float)
    end_latlng2 = db.Column(db.Float)
    viewpoint_latlng1 = db.Column(db.Float)
    viewpoint_latlng2 = db.Column(db.Float)
    creator = db.Column(db.ForeignKey('user.name', onupdate='CASCADE', ondelete='CASCADE'))
    fav = db.Column(db.Integer)
    created_at = db.Column(db.DateTime,  default=db.func.now())

    def __repr__(self):
        return '<HyperLapse id={id} name={name}>'.format(
            id=self.id, name=self.name)

def init():
    db.create_all()
