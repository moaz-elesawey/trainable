from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import UUID, DataRequired, Length

from ... import db
from ...models import Course, Lesson, User

empty_option = [("", "-------")]


class NewCourseForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(min=1, max=255)])
    summary = TextAreaField("Summary")
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class AssignUserCourseForm(FlaskForm):
    course = SelectField("Course", validators=[UUID(message="Valid user ID required")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_courses = db.session.execute(select(Course).select_from(Course)).scalars()
        self.course.choices = empty_option + [
            (str(course.course_id), course.name) for course in db_courses
        ]


class AssignCourseUserForm(FlaskForm):
    user = SelectField("User", validators=[UUID(message="Valid course ID required")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_users = db.session.execute(select(User).select_from(User)).scalars()
        self.user.choices = empty_option + [
            (str(user.user_id), user.fullname) for user in db_users
        ]


class NewLessonForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(min=1, max=255)])
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class AssignCourseLessonForm(FlaskForm):
    lesson = SelectField("Lesson", validators=[UUID(message="Select valid lesson")])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_lessons = db.session.execute(select(Lesson).select_from(Lesson)).scalars()
        self.lesson.choices = empty_option + [
            (str(lesson.get_id()), lesson.name) for lesson in db_lessons
        ]
