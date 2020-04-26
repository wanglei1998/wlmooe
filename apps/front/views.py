from flask import Blueprint,views,request,render_template,session,abort,g
from flask_paginate import Pagination,get_page_parameter
from sqlalchemy import func
from exts import db
from utils import restful
import config
from .forms import SignupForm,SigninForm,AddCommentForm,AddStarForm
from .models import Student
from ..models import Banner,Board,Course,Comment,Student_Course
from .decorators import login_required
from ..knn.knn import knn

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
        query_obj = db.session.query(Course).order_by(Course.create_time.desc()).filter(Course.highlight==1)
    elif sort == 3:
        # 按照点击量排序
        query_obj = Course.query.order_by(Course.click.desc())
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


@bp.route('/c/<course_id>/')
def course_detail(course_id):
    course = Course.query.get(course_id)
    if not course:
        abort(404)
    else:
        course.click = course.click+1
        db.session.commit()
        click = course.click
        sumStudent = Student_Course.query.filter(Student_Course.course_id==course.id).count()
        sumStar = Student_Course.query.filter(Student_Course.course_id==course.id).all()
        sum = 0
        for star_demo in sumStar:
            sum += star_demo.star
        aveStar = 0;
        if(sumStudent != 0):
            aveStar = sum/sumStudent
        classification = knn.courseclassTest([click,aveStar])
        print(classification[0])
        course.classification = classification[0]
        db.session.commit()
        return render_template('front/front_cdetail.html',course=course)


@bp.route('/acomment/',methods=['POST'])
@login_required
def add_comment():
    form = AddCommentForm(request.form)
    if form.validate():
        content = form.content.data
        course_id = form.course_id.data
        course = Course.query.get(course_id)
        if course:
            comment = Comment(content=content)
            comment.course = course
            comment.author = g.student
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这门课程！')
    else:
        return restful.params_error(form.get_error())

@bp.route('/astar/',methods=['POST'])
@login_required
def add_star():
    form = AddStarForm(request.form)
    if form.validate():
        index = form.index.data
        course_id = form.course_id.data
        student_id = g.student.id
        course = Course.query.get(course_id)
        if course:
            #filter 加表名 用==  支持 order_by等复杂操作  filter_by 不加表名字 用==，简单用法
            student_course = db.session.query(Student_Course).filter_by(student_id=student_id, course_id=course_id).first()
            if student_course:
                print(student_course.student_id+" "+student_course.course_id)
                student_course.star = index
                db.session.commit()
            else:
                print("新加入")
                student_course_model = Student_Course(student_id=student_id, course_id=course_id,star=index)
                db.session.add(student_course_model)
                db.session.commit()
            #分类更新
            click = course.click
            sumStudent = Student_Course.query.filter(Student_Course.course_id == course.id).count()
            sumStar = Student_Course.query.filter(Student_Course.course_id == course.id).all()
            sum = 0
            for star_demo in sumStar:
                sum += star_demo.star
            aveStar = 0;
            if (sumStudent != 0):
                aveStar = sum / sumStudent
            classification = knn.courseclassTest([click, aveStar])
            print(classification[0])
            course.classification = classification[0]
            db.session.commit()
            return restful.success()
        else:
            return restful.params_error('没有这门课程！')
    else:
        return restful.params_error(form.get_error())

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

