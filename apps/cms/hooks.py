from .views import bp
import config
from flask import session,g
from .models import Teacher

@bp.before_request
def before_request():
    if config.TEACHER_ID in session:
        user_id = session.get(config.TEACHER_ID)
        teacher = Teacher.query.get(user_id)
        if teacher:
            g.teacher = teacher