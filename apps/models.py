from exts import db
from datetime import datetime

class Banner(db.Model):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey("teacher.id"),nullable=False)

    author = db.relationship("Teacher", backref='banners')


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    click = db.Column(db.Integer,default=0)
    classification = db.Column(db.String(20),default="未进行分类")
    highlight = db.Column(db.Integer,default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)
    board_id = db.Column(db.Integer, db.ForeignKey("board.id"), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("teacher.id"), nullable=False)

    board = db.relationship("Board", backref="courses")
    author = db.relationship("Teacher", backref='courses')
    students = db.relationship("Student_Course",back_populates="course")

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    author_id = db.Column(db.String(100), db.ForeignKey("student.id"), nullable=False)

    course = db.relationship("Course", backref='comments')
    author = db.relationship("Student", backref='comments')


class Student_Course(db.Model):
    __tablename__ = 'student_course'
    student_id = db.Column(db.String(100),db.ForeignKey('student.id'),primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)
    star = db.Column(db.Integer,nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    student = db.relationship("Student",back_populates="courses")
    course = db.relationship("Course",back_populates="students")

