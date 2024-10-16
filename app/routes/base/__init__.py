from flask import Blueprint, render_template, url_for, redirect, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import select
from ... import db
from ...models import User, Course, UserCourse, CourseLesson


bp = Blueprint("base", __name__, template_folder="templates")


@bp.route("/health-check")
def health_check():
    return jsonify({"msg": "Ok"})


@bp.route("/")
@login_required
def home():
    # page = int(request.args.get("page", 1))

    stmt = (
        select(
            UserCourse,
        )
        .select_from(Course)
        .join(UserCourse, onclause=(Course.course_id == UserCourse.course_id))
        .join(User, onclause=(User.user_id == UserCourse.user_id))
        .filter(User.user_id == current_user.get_id())
        .distinct()
    )

    courses = db.session.execute(stmt).scalars().all()

    return render_template("base/home.html", courses=courses, title="Home")


@bp.route("/course/<string:course_id>")
@login_required
def course(course_id):
    if not db.session.get(UserCourse, ident=(current_user.user_id, course_id)):
        flash("Page you try to access is not found.", "warning")
        return redirect(url_for("base.home"))

    course = db.session.get(Course, ident=course_id)

    return render_template("base/course.html", course=course, title="Course")


@bp.route("/course/<string:course_id>/lesson/<string:lesson_id>")
def course_lesson(course_id: str, lesson_id: str):
    """Get Course Lesson"""

    if not db.session.get(UserCourse, ident=(current_user.user_id, course_id)):
        flash("Page you try to access not found.", "warning")
        return redirect(url_for("base.home"))

    course_lesson = db.session.get(CourseLesson, ident=(course_id, lesson_id))
    if not course_lesson:
        flash("Page you try to access not found.", "warning")
        return redirect(url_for("base.home"))

    return render_template(
        "base/course_lesson.html", course_lesson=course_lesson, title="Couse Lesson"
    )


@bp.route("/about")
@login_required
def about():
    return render_template("base/about.html")
