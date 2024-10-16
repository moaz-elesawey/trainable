from flask import (
    Blueprint,
    request,
    redirect,
    url_for,
    render_template,
    flash,
    current_app as app,
)
from flask_login import current_user
from sqlalchemy import select
from ... import db
from ... import consts
from ...decorators import staff_user_required, permission_required
from .forms import (
    NewCourseForm,
    AssignUserCourseForm,
    NewLessonForm,
    AssignCourseLessonForm,
)
from ...models import Course, User, UserCourse, Lesson, CourseLesson


bp = Blueprint("staff", __name__, template_folder="templates")


@bp.route("/panel")
@staff_user_required
def panel():
    """Staff Panel"""
    q = request.args.get("q", "")
    courses = db.session.execute(
        select(Course).filter(Course.name.icontains(q))
    ).scalars()
    return render_template("staff/panel.html", courses=courses, q=q, title="Panel")


@bp.route("add-new-course", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_CREATE_COURSE)
def add_new_course():
    """Add New Course"""
    form = NewCourseForm()

    if form.validate_on_submit():
        name = form.name.data
        summary = form.summary.data
        content = form.content.data

        if db.session.execute(
            select(Course).filter(Course.name == name)
        ).scalar_one_or_none():
            flash(f"Couse with name {name} already exist.", "warning")
            return redirect(url_for("staff.add_new_course"))

        course = Course(
            name=name,
            summary=summary,
            content=content,
        )

        try:
            db.session.add(course)
            db.session.commit()
            flash(f"Course with title {name} has added successfully.", "success")
            return redirect(url_for("staff.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something wen wrong, Please try again later.", "danger")
    return render_template("staff/add_new_course.html", form=form, title="New Course")


@bp.route("assign-user-course", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_COURSE)
def assign_user_course():
    """Assign User Course"""
    form = AssignUserCourseForm()

    if form.validate_on_submit():
        user_id = form.user.data
        course_id = form.course.data

        if not db.session.get(Course, course_id):
            flash(f"Course with id: {course_id} is not found.", "warning")
            return redirect(url_for("staff.assign_user_course"))

        if not db.session.get(User, user_id):
            flash(f"User with id: {user_id} is not found.", "warning")
            return redirect(url_for("staff.assign_user_course"))

        if db.session.get(UserCourse, (user_id, course_id)):
            flash("This course is already assigned to this user.", "warning")
            return redirect(url_for("staff.assign_user_course"))

        user_course = UserCourse(
            user_id=user_id, course_id=course_id, assigned_by_id=current_user.get_id()
        )
        try:
            db.session.add(user_course)
            db.session.commit()
            flash("Course assigned successfully for the user.", "success")
            return redirect(url_for("staff.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something went wrong, Please try again later.", "danger"), 500

    return render_template(
        "staff/assign_user_course.html", form=form, title="Assign Course"
    )


@bp.route("add-new-assessment", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_CREATE_ASSESSMENT)
def add_new_assessment():
    """Add New Assessment"""
    return render_template("staff/add_new_assessment.html", title="New Assessment")


@bp.route("assign-user-assessment", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_ASSESSMENT)
def assign_user_assessment():
    """Assign User Assessment"""
    return render_template(
        "staff/assign_user_assessment.html", title="Assign Assessment"
    )


@bp.route("add-new-lesson", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_CREATE_COURSE)
def add_new_lesson():
    """Add New Lesson"""
    form = NewLessonForm()

    if form.validate_on_submit():
        name = form.name.data
        content = form.content.data
        index = 1

        lesson = Lesson(
            name=name,
            index=index,
            content=content,
        )

        try:
            db.session.add(lesson)
            db.session.commit()
            flash(f"Lesson with title: {name} added successfully", "success")
            return redirect(url_for("staff.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something went wrong, Please try agian later", "danger")

    return render_template("staff/add_new_lesson.html", form=form, title="New Lesson")


@bp.route("assign-course-lesson/<string:course_id>", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_CREATE_COURSE)
def assign_course_lesson(course_id: str):
    """Assign Course Lesson"""
    form = AssignCourseLessonForm()

    if form.validate_on_submit():
        lesson_id = form.lesson.data

        if not db.session.get(Course, course_id):
            flash(f"Course with id: {course_id} is not found.", "warning")
            return redirect(url_for("staff.assign_course_lesson"))

        if not db.session.get(Lesson, lesson_id):
            flash(f"Lesson with id: {lesson_id} is not found.", "warning")
            return redirect(url_for("staff.assign_course_lesson"))

        if db.session.get(CourseLesson, (course_id, lesson_id)):
            flash("This lesson is already assigned to this course.", "warning")
            return redirect(url_for("staff.assign_course_lesson"))

        course_lesson = CourseLesson(
            course_id=course_id,
            lesson_id=lesson_id,
            assigned_by_id=current_user.get_id(),
        )
        # course_lessons_count = db.session.execute(
        #     select(func.count())
        #     .select_from(CourseLesson)
        #     .filter(CourseLesson.course_id == course_id)
        # ).scalar_one_or_none()

        try:
            db.session.add(course_lesson)
            db.session.commit()
            flash("Lesson assigned successfully for the course", "success")
            return redirect(url_for("staff.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something went wrong, Please try again later.", "danger"), 500

    return render_template(
        "staff/assign_course_lesson.html", form=form, title="Assign Lesson"
    )
