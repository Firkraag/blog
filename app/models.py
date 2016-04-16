from flask.ext.login import UserMixin
from app import db
from hashlib import md5

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    social_id = db.Column(db.String(64), nullable = False, unique = True)
    nickname = db.Column(db.String(64), nullable = False)
    email = db.Column(db.String(64), nullable = True)
    admin = db.Column(db.Boolean(), nullable = False)
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

    def avatar(self, size): 
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.email.encode('utf-8')).hexdigest(), size)

    def __repr__(self):
        return '<User %r>' % (self.nickname)

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    summary = db.Column(db.Text, nullable = False)
    html_content = db.Column(db.Text, nullable = False)
    title = db.Column(db.String(140), nullable = False) 
    timestamp = db.Column(db.DateTime, nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='blog', lazy = 'dynamic')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text, nullable = False)
    html_content = db.Column(db.Text, nullable = False)
    author_nickname = db.Column(db.String(64), nullable = False)
    author_email = db.Column(db.String(140), nullable = False) 
    timestamp = db.Column(db.DateTime, nullable = False)
    author_url = db.Column(db.String(140), nullable = True)
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))

    def avatar(self, size): 
        return 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(self.author_email.encode('utf-8')).hexdigest(), size)
