from app import app, db, lm
from flask import render_template, redirect, url_for, flash, g, request, jsonify
from .oauth import OAuthSignIn
from flask.ext.login import login_user, logout_user, current_user, login_required#, jsonify
from .models import User, Blog, Comment
from .forms import WriteForm, CommentForm
from datetime import datetime
from markdown import Markdown
from hashlib import md5
import json

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
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('index.html', blogs = blogs)

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/login')
def login():
    if not g.user.is_anonymous:
        return redirect(url_for('manage'))
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
        user = User(social_id=social_id, nickname=username, email=email, admin = False)
        db.session.add(user)
        db.session.commit()
    login_user(user, remember = True)
    return redirect(url_for('manage'))
#    return redirect(request.args.get('next') or url_for('index'))

@app.route('/author/<name>')
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
    return render_template('author.html', blogs = blogs)

@app.route('/blog/<id>', methods = ['GET', 'POST'])
def blog(id):
    form = CommentForm()
    if form.validate_on_submit():
        nickname = request.form.get('nickname')
        url = request.form.get('url')
        email = request.form.get('email')
        content = request.form.get('content')
        html_content = md.convert(content)
        timestamp = datetime.utcnow()
        comment = Comment(author_nickname = nickname, author_url = url, author_email = email, content = content, html_content = html_content, timestamp = timestamp, blog_id = id)
        db.session.add(comment)
        db.session.commit()
    blog = Blog.query.get(id)
    comments = blog.comments.order_by(Comment.timestamp.desc()).all()
    return render_template('blog.html', blog = blog, form = form, comments = comments) 

@app.route('/manage/write', methods = ['GET', 'POST'])
@login_required
def write():
    form = WriteForm()
    if form.validate_on_submit():
        content = form.content.data
        html_content = md.convert(content)
        blog = Blog(content = form.content.data, summary = form.summary.data, html_content = html_content, title = form.title.data, timestamp = datetime.utcnow(), author = current_user)
        db.session.add(blog)
        db.session.commit()
        flash('Your have written a new blog')
        return redirect(url_for('index'))
    else:
        return render_template('write.html', form = form)

@app.route('/manage/edit/<id>', methods = ['GET', 'POST'])
@login_required
def edit(id):
    print "here"
    form = WriteForm()
    if form.validate_on_submit():
        blog = Blog.query.get(id)
        blog.content = form.content.data
        blog.html_content = md.convert(blog.content)
        blog.title = form.title.data
        blog.summary = form.summary.data
        db.session.commit()
        flash('Your have updated your blog')
        return redirect(url_for('index'))
    else:
        print "not validate"
        print id
        blog = Blog.query.get(id)
        print blog.content
        form.title.data = blog.title
        form.content.data = blog.content
        form.summary.data = blog.summary
        return render_template('write.html', form = form)

@app.route('/manage/')
@app.route('/manage/blogs')
@login_required
def manage():
    blogs = Blog.query.order_by(Blog.timestamp.desc()).all()
    return render_template('manage_blogs.html', blogs = blogs)

@app.route('/manage/comments')
@login_required
def manage_comments():
    return render_template('manage_comments.html')

@app.route('/admin/')
@login_required
def admin():
    return '/admin'

@app.route('/comment', methods = ['POST'])
def comment():
    form = CommentForm()
#    if form.validate_on_submit():
#    blog_id = request.form.get('blog_id')
#    blog_id = 2
#    nickname = request.form.get('nickname')
#    url = request.form.get('url')
#    email = request.form.get('email')
#    content = request.form.get('content')
#    blog_id = request.form.get('blog_id')
    blog_id = request.form['blog_id']
    print blog_id
    print request.form
    nickname = request.form['nickname']
    url = request.form['url']
    email = request.form['email']
    print email
    content = request.form['content']
    html_content = md.convert(content)
    timestamp = datetime.utcnow()
    comment = Comment(author_nickname = nickname, author_url = url, author_email = email, content = content, html_content = html_content, timestamp = timestamp, blog_id = blog_id)
    db.session.add(comment)
    db.session.commit()
    avatar = 'http://www.gravatar.com/avatar/%s?d=mm&s=%d' % (md5(email.encode('utf-8')).hexdigest(), 60) 
    print avatar
    return jsonify({
        'nickname':nickname,
        'url':url,
        'avatar':avatar,
        'content':html_content,
    })
#    else:
#        blog_id = request.form.get('blog_id')
#        blog_id = 2
#        blog = Blog.query.get(blog_id)
#        comments = blog.comments.all()
#        return render_template('blog.html', blog = blog, form = form, comments = comments) 

@app.route('/test')
def test():
    return json.dumps(
        {'abc': 1,
        'sfd': 2,
        'sdf': 3
        }
    )

@app.route('/foobar')
def foobar():
    return render_template('foobar.html')
