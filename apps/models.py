from exts import db
from datetime import datetime


class Board(db.Model):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(20),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)


class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    name = db.Column(db.String(200),nullable=False)
    text = db.Column(db.Text,nullable=False)
    video = db.Column
    create_time = db.Column(db.DateTime,default=datetime.now)
    board_id = db.Column(db.Integer,db.ForeignKey("board.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("teacher.id"),nullable=False)

    board = db.relationship("Board",backref="courses")
    author = db.relationship("Teacher",backref='courses')


class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    course_id = db.Column(db.Integer,db.ForeignKey("course.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("teacher.id"), nullable=False)

    course = db.relationship("Course",backref='comments')
    author = db.relationship("Teacher",backref='comments')

