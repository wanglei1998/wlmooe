from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from wtforms.validators import Regexp, EqualTo, ValidationError, InputRequired
# from utils import zlcache
from wtforms import ValidationError
from flask import g


class SignupForm(BaseForm):
    username = StringField(validators=[Regexp(r".{2,20}", message='请输入正确格式的用户名！')])
    email = StringField(validators=[Email(message='请输入正确格式的邮箱'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message='请输入正确格式的密码！')])
    password1 = StringField(validators=[EqualTo("password", message='两次输入的密码不一致！')])

class SigninForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱'),InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6,20,message='请输入正确格式的密码')])
    remember = IntegerField()


