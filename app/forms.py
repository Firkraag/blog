from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(Form):
    openid = StringField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class WriteForm(Form):
    title = StringField('title', validators = [DataRequired(), Length(max = 140)])
    content = TextAreaField('content', validators = [DataRequired()])
    summary = TextAreaField('summary', validators = [DataRequired()])

    def __init__(self,  *args, **kwargs):
        Form.__init__(self, *args, **kwargs)

class CommentForm(Form):
    nickname = StringField('nickname', validators = [DataRequired(), Length(max = 64, min = 1)])
    url = StringField('url', validators = [Length(max = 140)])
    email = StringField('email', validators = [DataRequired(), Email(), Length(max = 140, min = 1)])
    content = TextAreaField('content', validators = [DataRequired()])

    def __init__(self,  *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
