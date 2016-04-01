from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length

class LoginForm(Form):
    openid = StringField('openid', validators = [DataRequired()])
    remember_me = BooleanField('remember_me', default = False)

class WriteForm(Form):
    title = StringField('title', validators = [DataRequired(), Length(max = 140)])
    content = TextAreaField('content', validators = [DataRequired()])

    def __init__(self,  *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
#        self.original_nickname = original_nickname
#
#    def validate(self):
#        if not Form.validate(self):
#            return False
#        if self.nickname.data == self.original_nickname:
#            return True
#        if self.nickname.data != User.make_valid_nickname(self.nickname.data):
#            self.nickname.errors.append(gettext("This nickname has invalid characters. Please use letters, numbers, dots and underscores only."))
#            return False
#        user = User.query.filter_by(nickname = self.nickname.data).first()
#        if user != None:
#            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
#            return False
#        return True
