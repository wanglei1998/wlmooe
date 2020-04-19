from flask import Blueprint,views,request,render_template,session
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy import func
from exts import db
from utils import restful
import config
from .forms import SignupForm,SigninForm
from .models import Student
from ..models import Banner,Board,Course,Comment


bp = Blueprint("front", __name__)

@bp.route('/')
def index():
    board_id = request.args.get('bd',type=int,default=None)
    page = request.args.get(get_page_parameter(),type=int,default=1)
    sort = request.args.get("st",type=int,default=1)
    banners = Banner.query.order_by(Banner.priority.desc()).limit(4)
    boards = Board.query.all()
    start = (page-1)*config.PER_PAGE
    end = start + config.PER_PAGE
    pasts = None
    total = 0

    query_obj = None
    if sort == 1:
        query_obj = Course.query.order_by(Course.create_time.desc())
    elif sort == 2:
        # 按照加精的时间倒叙排序
        query_obj = db.session.query(Course).outerjoin(HighlightPostModel).order_by(HighlightPostModel.create_time.desc(),Course.create_time.desc())
    elif sort == 3:
        # 按照点赞的数量排序
        query_obj = Course.query.order_by(Course.create_time.desc())
    elif sort == 4:
        # 按照评论的数量排序
        query_obj = db.session.query(Course).outerjoin(Comment).group_by(Course.id).order_by(func.count(Comment.id).desc(),Course.create_time.desc())

    if board_id:
        query_obj = query_obj.filter(Course.board_id==board_id)
        courses = query_obj.slice(start,end)
        total = query_obj.count()
    else:
        courses = query_obj.slice(start,end)
        total = query_obj.count()
    pagination = Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context = {
        'banners': banners,
        'boards': boards,
        'courses': courses,
        'pagination': pagination,
        'current_board': board_id,
        'current_sort': sort
    }
    return render_template('front/front_index.html',**context)



class SignupView(views.MethodView):
    def get(self):
        return render_template('front/front_signup.html')
    def post(self):
        form = SignupForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            username = form.username.data
            password = form.password1.data
            student = Student(telephone=telephone, username=username, password=password)
            db.session.add(student)
            db.session.commit()
            return restful.success()
        else:
            print(form.get_error())
            return restful.params_error(message=form.get_error())

class SigninView(views.MethodView):
    def get(self):
        return render_template('front/front_signin.html')

    def post(self):
        form = SigninForm(request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            remember = form.remeber.data
            student = Student.query.filter_by(telephone=telephone).first()
            if student and student.check_password(password):
                session[config.STUDENT_ID] = student.id
                if remember:
                    session.permanent = True
                return restful.success()
            else:
                return restful.params_error(message='手机号或密码错误！')
        else:
            return restful.params_error(message=form.get_error())



bp.add_url_rule('/signup/',view_func=SignupView.as_view('signup'))
bp.add_url_rule('/signin/',view_func=SigninView.as_view('signin'))

