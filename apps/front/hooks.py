from .views import bp
import config
from flask import session,g,render_template
from .models import Student

@bp.before_request
def my_before_request():
    if config.STUDENT_ID in session:
        student_id = session.get(config.STUDENT_ID)
        student = Student.query.get(student_id)
        if student:
            g.student = student