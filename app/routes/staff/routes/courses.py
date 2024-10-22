from flask import (
    current_app as app,
)
from flask import (
    flash,
    redirect,
    render_template,
    url_for,
)
from flask_login import current_user
from sqlalchemy import not_, select

from .... import consts, db
from ....decorators import permission_required
from ....models import Course, CourseLesson, Lesson, User, UserCourse
from .. import bp
from ..forms import (
    AssignCourseLessonForm,
    AssignCourseUserForm,
    AssignUserCourseForm,
    NewCourseForm,
    NewLessonForm,
)


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
            flash(f"Couse with name <b>{name}</b> already exist.", "warning")
            return redirect(url_for("staff.add_new_course"))

        course = Course(
            name=name,
            summary=summary,
            content=content,
        )

        try:
            db.session.add(course)
            db.session.commit()
            flash(f"Course <b>{name}</b> has added successfully.", "success")
            return redirect(url_for("staff.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something wen wrong, Please try again later.", "danger")
    return render_template("staff/add_new_course.html", form=form, title="New Course")


@bp.route("assign-user-course/<string:user_id>", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_COURSE)
def assign_user_course(user_id: str):
    """Assign User Course"""
    form = AssignUserCourseForm()

    user = db.session.get(User, ident=user_id)

    if not user:
        flash("User does not exist.", "warning")
        return redirect(url_for("staff.assign_user_course", user_id=user_id))

    user_courses = [
        row[0]
        for row in db.session.execute(
            select(Course).join(UserCourse).filter(UserCourse.user_id == user_id)
        ).all()
    ]

    unassigned_courses = db.session.execute(
        select(
            Course,
        ).filter(
            not_(
                Course.course_id.in_(
                    set({user_course.course_id for user_course in user_courses})
                )
            )
        )
    ).scalars()

    form.course.choices = [
        (str(course.course_id), course.name) for course in unassigned_courses
    ]

    if form.validate_on_submit():
        course_id = form.course.data

        if not db.session.get(Course, course_id):
            flash(f"Course with id: {course_id} is not found.", "warning")
            return redirect(url_for("staff.assign_user_course", user_id=user_id))

        if db.session.get(UserCourse, (user_id, course_id)):
            flash("This course is already assigned to this user.", "warning")
            return redirect(url_for("staff.assign_user_course", user_id=user_id))

        user_course = UserCourse(
            user_id=user_id, course_id=course_id, assigned_by_id=current_user.get_id()
        )
        try:
            db.session.add(user_course)
            db.session.commit()
            flash("Course assigned successfully for the user.", "success")
            return redirect(url_for("staff.assign_course_user", course_id=course_id))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something went wrong, Please try again later.", "danger")

    return render_template(
        "staff/assign_user_course.html", form=form, user=user, title="Assign Course"
    )


@bp.route("assign-course-user/<string:course_id>", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_COURSE)
def assign_course_user(course_id: str):
    """Assign Course User"""
    form = AssignCourseUserForm()

    course = db.session.get(Course, ident=course_id)

    if not course:
        flash("Course does not exist.", "warning")
        return redirect(url_for("staff.assign_course_user", course_id=course_id))

    user_courses = [
        row[0]
        for row in db.session.execute(
            select(User)
            .join(UserCourse, onclause=(User.user_id == UserCourse.user_id))
            .filter(UserCourse.course_id == course_id)
        ).all()
    ]

    unassigned_users = db.session.execute(
        select(
            User,
        )
        .filter(
            not_(
                User.user_id.in_(
                    set({user_course.user_id for user_course in user_courses})
                )
            )
        )
        .filter(not_(User.is_superuser))
    ).scalars()

    form.user.choices = [
        (str(user.user_id), user.fullname) for user in unassigned_users
    ]

    if form.validate_on_submit():
        user_id = form.user.data

        if not db.session.get(User, user_id):
            flash(f"User with id: {user_id} is not found.", "warning")
            return redirect(url_for("staff.assign_course_user", course_id=course_id))

        if db.session.get(UserCourse, (user_id, course_id)):
            flash("This course is already assigned to this user.", "warning")
            return redirect(url_for("staff.assign_course_user", course_id=course_id))

        user_course = UserCourse(
            user_id=user_id, course_id=course_id, assigned_by_id=current_user.get_id()
        )
        try:
            db.session.add(user_course)
            db.session.commit()
            flash("Course assigned successfully for the user.", "success")
            return redirect(url_for("staff.assign_course_user", course_id=course_id))
        except Exception as e:
            db.session.rollback()
            app.logger.error(e)
            flash("Something went wrong, Please try again later.", "danger")

    return render_template(
        "staff/assign_course_user.html", form=form, course=course, title="Assign Course"
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
            return redirect(url_for("staff.assign_course_lesson", course_id=course_id))

        if not db.session.get(Lesson, lesson_id):
            flash(f"Lesson with id: {lesson_id} is not found.", "warning")
            return redirect(url_for("staff.assign_course_lesson", course_id=course_id))

        if db.session.get(CourseLesson, (course_id, lesson_id)):
            flash("This lesson is already assigned to this course.", "warning")
            return redirect(url_for("staff.assign_course_lesson", course_id=course_id))

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
