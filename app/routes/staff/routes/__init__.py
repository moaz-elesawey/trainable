from flask import render_template, request
from sqlalchemy import select

from .... import db
from ....decorators import staff_user_required
from ....models import Course
from .. import bp


@bp.route("/panel")
@staff_user_required
def panel():
    """Staff Panel"""
    q = request.args.get("q", "")
    courses = db.session.execute(
        select(Course).filter(Course.name.icontains(q))
    ).scalars()
    return render_template("staff/panel.html", courses=courses, q=q, title="Panel")


from .assessments import *  # noqa F403
from .courses import *  # noqa F403
