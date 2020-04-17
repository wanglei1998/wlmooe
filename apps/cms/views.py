from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from exts import db
import config
from .forms import SigninForm,SignupForm
from .models import Teacher
from .decorators import login_required

bp = Blueprint("cms", __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')

@bp.route('/logout/')
@login_required
def logout():
    del session[config.TEACHER_ID]
    return redirect(url_for('cms.login'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')

class SignupView(views.MethodView):
    def get(self,message=None):
        return render_template('cms/cms_signup.html',message=message)

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            teacher = Teacher(email=email,username=username,password=password)
            db.session.add(teacher)
            db.session.commit()
            return redirect(url_for('cms.signin'))
        else:
            message = form.get_error()
            print(message)
            return self.get(message=message)



class SigninView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_signin.html', message=message)

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            # filter_by 可以直接用属性名不用类名.属性名，但是不支持大于小于，不支持_and和 _or
            teacher = Teacher.query.filter_by(email=email).first()
            if teacher and teacher.check_password(password):
                session[config.TEACHER_ID] = teacher.id
                if remember:
                    # true默认31天
                    session.permanent = True
                return redirect(url_for('cms.index'))
            else:
                return self.get(message='邮箱或密码错误')
        else:
            message = form.get_error()
            print(message)
            return self.get(message=message)

bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
