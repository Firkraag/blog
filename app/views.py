from app import app, db, lm
from flask import render_template, redirect, url_for, flash, g, request
from .oauth import OAuthSignIn
from flask.ext.login import login_user, logout_user, current_user, login_required
from .models import User, Blog
from .forms import WriteForm
from datetime import datetime
from markdown import Markdown
import os
import subprocess

md = Markdown()
@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@app.route('/index')
def index():
    blogs = [
        {'title':   'example1',
         'content': 'fake1'
        },
        {'title':   'example2',
         'content': 'fake2'
        }
    ]
    return render_template('index.html', blogs = blogs)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login')
def login():
    if not g.user.is_anonymous:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', title = "Sign In")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember = True)
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/user/<name>')
def user(name):
#    blogs = [
#        {
#            'title': 'first blog',
#            'timestamp': 20160330,
#            'author':
#            {
#                'nickname': 'SmilingWang'
#            }
#        },
#        {
#            'title': 'Second blog',
#            'timestamp': 20160330,
#            'author':
#            {
#                'nickname': 'SmilingWang'
#            }
#        }
#    ]
    user = User.query.filter_by(nickname = name).first()
    blogs = user.blogs.all()
    return render_template('user.html', blogs = blogs)

@app.route('/blog/<id>')
def blog(id):
#    with open('/home/windheart/ft.py') as f:
#        content = f.read()
#    blog = {
#            'title': 'first blog',
#            'timestamp': 20160330,
#            'author':
#            {
#                'nickname': 'SmilingWang'
#            },
#            'content': content
#        }
    blog = Blog.query.get(id)
    content = md.convert(blog.content)
#    name = 'blog_' + str(blog.id) 
#    with open(name, 'w') as f:
#        f.write(blog.content.encode('utf-8'))
#    content = subprocess.check_output("app/Markdown.pl %s" % name, shell = True).decode('utf-8')
#    print content
#    with open(name, 'w') as f:
#        f.write(blog.content)
#        content = os.system("app/Markdown.pl %s" % name)
    return render_template('blog.html', blog = blog, content = content)

@app.route('/write', methods = ['GET', 'POST'])
@login_required
def write():
    form = WriteForm()
    if form.validate_on_submit():
        blog = Blog(content = form.content.data, title = form.title.data, timestamp = datetime.utcnow(), author = current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Your have written a new blog')
        return redirect(url_for('index'))
    else:
        return render_template('write.html', form = form)
