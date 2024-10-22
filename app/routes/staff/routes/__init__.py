from flask import render_template, request
from flask_login import current_user
from sqlalchemy import not_, select

from .... import db
from ....decorators import staff_user_required
from ....models import Course, User
from .. import bp


@bp.route("/panel")
@staff_user_required
def panel():
    """Staff Panel"""
    q_user = request.args.get("q_user", "")
    q_course = request.args.get("q_course", "")

    courses = db.session.execute(
        select(Course).filter(Course.name.icontains(q_course))
    ).scalars()

    users = db.session.execute(
        select(User)
        .filter(User.fullname.icontains(q_user))
        .filter(not_(User.is_superuser))
        .filter(User.group_id == current_user.group_id)
    ).scalars()

    return render_template(
        "staff/panel.html",
        courses=courses,
        users=users,
        q_user=q_user,
        q_course=q_course,
        title="Panel",
    )


from .assessments import *  # noqa F403
from .courses import *  # noqa F403
