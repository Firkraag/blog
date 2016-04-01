from flask.ext.login import UserMixin
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    social_id = db.Column(db.String(64), nullable = False, unique = True)
    nickname = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(64), nullable = True)
    blogs = db.relationship('Blog', backref = 'author', lazy = 'dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    def get_id(self):
        try:
            return unicode(self.id)
        except NameError:
            return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text)
    title = db.Column(db.String(140), nullable = False) 
    timestamp = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

