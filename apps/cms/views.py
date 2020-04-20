from flask import Blueprint, views, render_template, request, session, redirect, url_for, g, jsonify
from flask_mail import Message
from exts import db,mail
from  utils import restful,zlcache
import config,string,random
from .forms import SigninForm, SignupForm, ResetpwdForm, ResetEmailForm,AddBannerForm, UpdateBannerForm, AddBoardForm,UpdateBoardForm, AddCourseForm
from .models import Teacher
from .decorators import login_required
from ..models import Banner,Board,Course,Comment

bp = Blueprint("cms", __name__, url_prefix='/cms')


@bp.route('/')
@login_required
def index():
    return render_template('cms/cms_index.html')


@bp.route('/logout/')
@login_required
def logout():
    del session[config.TEACHER_ID]
    return redirect(url_for('cms.signin'))


@bp.route('/profile/')
@login_required
def profile():
    return render_template('cms/cms_profile.html')


@bp.route('/email_captcha/')
def email_captcha():
    email = request.args.get('email')
    if not email:
        return restful.params_error('请传递邮箱参数！')
    source = list(string.ascii_letters)
    # source.extend(["0","1","2","3","4","5","6","7","8","9"])等价于下面的
    source.extend(map(lambda x: str(x), range(0, 10)))
    captcha = "".join(random.sample(source, 6))
    print('***************************************')
    print(captcha)
    print('***************************************')
    message = Message('卧龙MOOE邮箱验证码', recipients=[email], body='您的验证码是：%s' % captcha)
    try:
        mail.send(message)
    except:
        return restful.sever_error()
    zlcache.set(email, captcha)
    return restful.success()


@bp.route('banners')
@login_required
def banners():
    banners = Banner.query.order_by(Banner.priority.desc()).all()
    return render_template('cms/cms_banners.html', banners=banners)


@bp.route('/abanner/', methods=['POST'])
@login_required
def abanner():
    form = AddBannerForm(request.form)
    if form.validate():
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner(name=name, image_url=image_url, link_url=link_url, priority=priority)
        db.session.add(banner)
        db.session.commit()
        return restful.success()


@bp.route('/ubanner/', methods=['POST'])
@login_required
def ubanner():
    form = UpdateBannerForm(request.form)
    if form.validate():
        banner_id = form.banner_id.data
        name = form.name.data
        image_url = form.image_url.data
        link_url = form.link_url.data
        priority = form.priority.data
        banner = Banner.query.get(banner_id)
        if banner:
            banner.name = name
            banner.image_url = image_url
            banner.link_url = link_url
            banner.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个轮播图！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dbanner/', methods=['POST'])
@login_required
def dbanner():
    banner_id = request.form.get('banner_id')
    if not banner_id:
        return restful.params_error(message='请传入轮播图id！')

    banner = Banner.query.get(banner_id)
    if not banner:
        return restful.params_error(message='没有这个轮播图！')

    db.session.delete(banner)
    db.session.commit()
    return restful.success()



@bp.route('/boards/')
@login_required
def boards():
    board_models = Board.query.all()
    context = {
        'boards': board_models
    }
    return render_template('cms/cms_boards.html', **context)


@bp.route('/aboard/', methods=['POST'])
@login_required
def aboard():
    form = AddBoardForm(request.form)
    if form.validate():
        name = form.name.data
        name = form.name.data
        board = Board(name=name)
        db.session.add(board)
        db.session.commit()
        return restful.success()
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/uboard/', methods=['POST'])
@login_required
def uboard():
    form = UpdateBoardForm(request.form)
    if form.validate():
        board_id = form.board_id.data
        name = form.name.data
        board = Board.query.get(board_id)
        if board:
            board.name = name
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message='没有这个板块！')
    else:
        return restful.params_error(message=form.get_error())


@bp.route('/dboard/', methods=['POST'])
@login_required
def dboard():
    board_id = request.form.get("board_id")
    if not board_id:
        return restful.params_error('请传入板块id！')

    board = Board.query.get(board_id)
    if not board:
        return restful.params_error(message='没有这个板块！')

    db.session.delete(board)
    db.session.commit()
    return restful.success()


@bp.route('/courses/')
@login_required
def courses():
    return render_template('cms/cms_courses.html')

@bp.route('/acourse/',methods=['GET','POST'])
@login_required
def acourse():
    if request.method == 'GET':
        boards = Board.query.all()
        return render_template('cms/cms_acourse.html',boards=boards)
    else:
        form = AddCourseForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            board = Board.query.get(board_id)
            if not board:
                return restful.params_error(message='没有这个板块！')
            course = Course(title=title,content=content)
            course.board = board
            course.author = g.teacher
            db.session.add(course)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(message=form.get_error())


@bp.route('/comments/')
@login_required
def comments():
    return render_template('cms/cms_comments.html')


@bp.route('/teacher/')
@login_required
def teacher():
    return render_template('cms/cms_teacher.html')


@bp.route('/student/')
@login_required
def student():
    return render_template('cms/cms_student.html')




class SignupView(views.MethodView):
    def get(self, message=None):
        return render_template('cms/cms_signup.html', message=message)

    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            teacher = Teacher(email=email, username=username, password=password)
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


class ResetPwdView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetpwd.html')

    def post(self):
        form = ResetpwdForm(request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            teacher = g.teacher
            if teacher.check_password(oldpwd):
                teacher.password = newpwd
                db.session.commit()
                return restful.success()
            else:
                return restful.params_error("旧密码错误")
        else:
            message = form.get_error()
            return restful.params_error(message)


class ResetEmailView(views.MethodView):
    decorators = [login_required]

    def get(self):
        return render_template('cms/cms_resetemail.html')

    def post(self):
        form = ResetEmailForm(request.form)
        if form.validate():
            email = form.email.data
            g.teacher.email = email
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error(form.get_error())


bp.add_url_rule('/signin/', view_func=SigninView.as_view('signin'))
bp.add_url_rule('/signup/', view_func=SignupView.as_view('signup'))
bp.add_url_rule('/resetpwd/', view_func=ResetPwdView.as_view('resetpwd'))
bp.add_url_rule('/resetemail/', view_func=ResetEmailView.as_view('resetemail'))
