from flask_wtf import FlaskForm
from sqlalchemy import not_, select
from wtforms import (
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Length

from ... import db
from ...models import Course, Lesson, User

empty_option = [("", "-------")]


class NewCourseForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(min=1, max=255)])
    summary = TextAreaField("Summary")
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class AssignUserCourseForm(FlaskForm):
    user = SelectField("User", validators=[])
    course = SelectField("Course", validators=[])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_courses = db.session.execute(select(Course).select_from(Course)).scalars()
        db_users = db.session.execute(
            select(User)
            .filter(User.is_active)
            .filter(not_(User.is_superuser))
            .select_from(User)
        ).scalars()

        self.course.choices = empty_option + [
            (str(c.course_id), c.name) for c in db_courses
        ]
        self.user.choices = empty_option + [
            (str(u.user_id), u.fullname) for u in db_users
        ]


class NewLessonForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(min=1, max=255)])
    content = TextAreaField("Content")
    submit = SubmitField("Submit")


class AssignCourseLessonForm(FlaskForm):
    lesson = SelectField("Lesson", validators=[])
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_lessons = db.session.execute(select(Lesson).select_from(Lesson)).scalars()
        self.lesson.choices = empty_option + [
            (str(lesson.get_id()), lesson.name) for lesson in db_lessons
        ]
