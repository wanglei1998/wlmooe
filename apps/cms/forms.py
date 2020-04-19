from wtforms import StringField,IntegerField
from wtforms.validators import Email,InputRequired,Length,EqualTo
from ..forms import BaseForm
from wtforms.validators import Regexp, EqualTo, ValidationError, InputRequired
from utils import zlcache
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


class ResetpwdForm(BaseForm):
    oldpwd = StringField(validators=[Length(6,20,message='请输入正确格式的旧密码')])
    newpwd = StringField(validators=[Length(6, 20,message='请输入正确格式的新密码')])
    newpwd2 = StringField(validators=[EqualTo('newpwd',message='确认密码必须和新密码相同')])


class ResetEmailForm(BaseForm):
    email = StringField(validators=[Email(message='请输入正确格式的邮箱')])
    captcha = StringField(validators=[Length(min=6,max=6,message='请输入正确长度的邮箱')])

    def validate_captcha(self,field):
        captcha = field.data
        email = self.email.data
        captcha_cache = zlcache.get(email)
        if not captcha_cache or captcha.lower()!=captcha_cache.lower():
            raise ValidationError('邮箱验证码错误！')

    def validate_email(self,field):
        email = field.data
        teacher = g.teacher
        if teacher.email == email:
            raise ValidationError('不能修改为原邮箱！')


