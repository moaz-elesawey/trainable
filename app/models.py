import uuid
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    PrimaryKeyConstraint,
    String,
    Text,
)
from sqlalchemy.dialects import postgresql as pg
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import db, login_manager


@login_manager.user_loader
def load_user(user_id: uuid.UUID) -> "User":
    return db.session.get_one(User, ident=user_id)


class Group(db.Model):
    __tablename__ = "groups"

    group_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    abbreviation: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(Text(), nullable=True, default="N/A")

    def get_id(self) -> uuid.UUID:
        return self.group_id

    def __repr__(self) -> str:
        return f"Group<{self.name!r}>"


class User(db.Model, UserMixin):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    fullname: Mapped[str] = mapped_column(String(255), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_staff: Mapped[bool] = mapped_column(default=False)
    is_superuser: Mapped[bool] = mapped_column(default=False)

    registered_at: Mapped[datetime] = mapped_column(default=datetime.now)
    registered_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    last_login: Mapped[datetime] = mapped_column(
        default=datetime.now, onupdate=datetime.now
    )

    group_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("groups.group_id"), nullable=True
    )
    group: Mapped["Group"] = relationship(foreign_keys="User.group_id")

    courses: Mapped[list["UserCourse"]] = relationship(
        foreign_keys="UserCourse.user_id"
    )
    assessments: Mapped[list["UserAssessment"]] = relationship(
        foreign_keys="UserAssessment.user_id"
    )
    permissions: Mapped[list["UserPermission"]] = relationship(
        foreign_keys="UserPermission.user_id"
    )

    profile: Mapped["Profile"] = relationship(foreign_keys="Profile.user_id")

    def get_id(self) -> uuid.UUID:
        return self.user_id

    def __repr__(self) -> str:
        return f"User<{self.username!r}>"


class Profile(db.Model):
    __tablename__ = "profiles"

    profile_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    title: Mapped[str] = mapped_column(String(255))

    age: Mapped[int] = mapped_column(Integer())

    years_of_experience: Mapped[int] = mapped_column(Integer())

    profile_picture: Mapped[str] = mapped_column(String(255))

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    def get_id(self) -> uuid.UUID:
        return self.profile_id

    def __repr__(self) -> str:
        return f"Profile<{self.title!r}>"


class Permission(db.Model):
    __tablename__ = "permissions"

    permission_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    flag: Mapped[int] = mapped_column(Integer(), nullable=False, unique=True)
    codename: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    description: Mapped[str] = mapped_column(Text(), nullable=True, default="N/A")

    def get_id(self) -> uuid.UUID:
        return self.permission_id

    def __repr__(self) -> str:
        return f"Permission<{self.codename!r}, {self.flag}>"


class UserPermission(db.Model):
    __tablename__ = "user_permissions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("permissions.permission_id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("user_id", "permission_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.user_id, self.permission_id)


class GroupPermission(db.Model):
    __tablename__ = "group_permissions"

    group_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("groups.group_id"), nullable=False
    )
    permission_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("permissions.permission_id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("group_id", "permission_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.group_id, self.permission_id)


class Course(db.Model):
    __tablename__ = "courses"

    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String(255), nullable=False, unique=True, index=True
    )
    summary: Mapped[str] = mapped_column(Text(), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    users: Mapped[list["UserCourse"]] = relationship(
        foreign_keys="UserCourse.course_id"
    )
    lessons: Mapped[list["CourseLesson"]] = relationship(back_populates="course")
    assessment: Mapped["CourseAssessment"] = relationship()
    attachments: Mapped[list["Attachment"]] = relationship()

    def get_id(self) -> uuid.UUID:
        return self.course_id

    @property
    def enrolled_count(self):
        return len(self.users)

    def __repr__(self) -> str:
        return f"Course<{self.name!r}>"


class UserCourse(db.Model):
    __tablename__ = "user_courses"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    user: Mapped["User"] = relationship(
        foreign_keys="UserCourse.user_id", back_populates="courses"
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False
    )
    course: Mapped["Course"] = relationship(
        foreign_keys="UserCourse.course_id", back_populates="users"
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    is_completed: Mapped[bool] = mapped_column(Boolean(), nullable=True, default=False)
    completed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    __table_args__ = (PrimaryKeyConstraint("user_id", "course_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.user_id, self.course_id)


class Lesson(db.Model):
    __tablename__ = "lessons"

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    index: Mapped[int] = mapped_column(Integer(), nullable=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    courses: Mapped[list["CourseLesson"]] = relationship(back_populates="lesson")

    def get_id(self) -> uuid.UUID:
        return self.lesson_id

    def __repr__(self) -> str:
        return f"Lesson<{self.name!r}>"


class UserCourseLesson(db.Model):
    __tablename__ = "user_course_lessons"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False
    )
    lesson_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("lessons.lesson_id"), nullable=False
    )

    first_access_at: Mapped[datetime] = mapped_column(DateTime(), default=datetime.now)

    last_access_at: Mapped[datetime] = mapped_column(DateTime(), onupdate=datetime.now)

    is_accessed: Mapped[bool] = mapped_column(Boolean(), default=False)

    is_marked_completed: Mapped[bool] = mapped_column(Boolean(), default=False)

    is_marked_skiped: Mapped[bool] = mapped_column(Boolean(), default=False)

    mark_completed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    mark_skiped_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    opened_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    closed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    __table_args__ = (PrimaryKeyConstraint("user_id", "course_id", "lesson_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.user_id, self.course_id, self.lesson_id)

    def __repr__(self) -> str:
        return f"UserCourseLesson<{self.user_id}, {self.course_id}, {self.lesson_id}>"


class CourseLesson(db.Model):
    __tablename__ = "course_lessons"

    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False
    )

    lesson_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("lessons.lesson_id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    course: Mapped["Course"] = relationship(
        foreign_keys=[course_id], back_populates="lessons"
    )
    lesson: Mapped["Lesson"] = relationship(
        foreign_keys=[lesson_id], back_populates="courses"
    )

    # Index of lesson in the course
    # TODO: will serve a role in re arraning of lessons.
    index: Mapped[int] = mapped_column(Integer(), nullable=True, default=1)

    __table_args__ = (PrimaryKeyConstraint("course_id", "lesson_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.course_id, self.lesson_id)


class Attachment(db.Model):
    __tablename__ = "attachments"

    attachment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True
    )

    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False, unique=False)

    old_filename: Mapped[str] = mapped_column(Text(), nullable=False)

    new_filename: Mapped[str] = mapped_column(Text(), nullable=False)

    file_path: Mapped[str] = mapped_column(Text(), nullable=False)

    file_data: Mapped[bytes] = mapped_column(pg.BYTEA(), nullable=False)

    def get_id(self) -> uuid.UUID:
        return self.attachment_id

    def __repr__(self) -> str:
        return f"Attachment<{self.attachment_id}, {self.name}>"


class Assessment(db.Model):
    __tablename__ = "assessments"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(255), nullable=False)

    summary: Mapped[str] = mapped_column(Text(), nullable=True, default="N/A")

    duration_in_minutes: Mapped[int] = mapped_column(
        Integer(), nullable=True, default=30
    )

    questions: Mapped[list["AssessmentQuestion"]] = relationship()

    def get_id(self) -> uuid.UUID:
        return self.assessment_id

    def __repr__(self) -> str:
        return f"Assessment<{self.name}>"


class CourseAssessment(db.Model):
    __tablename__ = "course_assessments"

    course_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("courses.course_id"), nullable=False
    )

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("assessments.assessment_id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    __table_args__ = (PrimaryKeyConstraint("course_id", "assessment_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.course_id, self.assessment_id)


class UserAssessment(db.Model):
    __tablename__ = "user_assessments"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("assessments.assessment_id"), nullable=False
    )
    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)
    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    started_at: Mapped[datetime] = mapped_column(nullable=True)

    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    is_on_hold: Mapped[datetime] = mapped_column(default=False)

    is_started: Mapped[bool] = mapped_column(default=False)

    is_completed: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "assessment_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.user_id, self.assessment_id)


class Question(db.Model):
    __tablename__ = "questions"

    question_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    question: Mapped[str] = mapped_column(String(255), nullable=False)

    type: Mapped[str] = mapped_column(String(255), nullable=False)

    choices: Mapped[list["Choice"]] = relationship()

    def get_id(self) -> uuid.UUID:
        return self.question_id

    def __repr__(self) -> str:
        return f"Question<{self.name}>"


class Answer(db.Model):
    __tablename__ = "answers"

    answer_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    answer: Mapped[str] = mapped_column(Text(), nullable=False)

    question_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True),
        ForeignKey("questions.question_id"),
        nullable=False,
        unique=True,
        index=True,
    )

    def get_id(self) -> uuid.UUID:
        return self.answer_id


class AssessmentQuestion(db.Model):
    __tablename__ = "assessment_questions"

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("assessments.assessment_id"), nullable=False
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False
    )

    assigned_at: Mapped[datetime] = mapped_column(default=datetime.now)

    assigned_by_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    __table_args__ = (PrimaryKeyConstraint("assessment_id", "question_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.assessment_id, self.question_id)


class UserAssessmentQuestion(db.Model):
    __tablename__ = "user_assessment_questions"

    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    assessment_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("assessments.assessment_id"), nullable=False
    )

    question_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False
    )

    opened_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    closed_at: Mapped[datetime] = mapped_column(DateTime(), nullable=True)

    completed_at: Mapped[datetime] = mapped_column(nullable=True)

    skiped_at: Mapped[datetime] = mapped_column(nullable=True)

    is_completed: Mapped[bool] = mapped_column(default=False)

    is_skiped: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (PrimaryKeyConstraint("user_id", "assessment_id", "question_id"),)

    def get_id(self) -> tuple[uuid.UUID]:
        return (self.user_id, self.assessment_id, self.question_id)


class Choice(db.Model):
    __tablename__ = "choices"

    choice_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    choice: Mapped[str] = mapped_column(String(255), nullable=False)

    question_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("questions.question_id"), nullable=False
    )

    def get_id(self) -> uuid.UUID:
        return self.choice_id

    def __repr__(self) -> str:
        return f"Choice<{self.choice}>"


class Mail(db.Model):
    __tablename__ = "mails"

    mail_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    sender_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    recipients: Mapped[str] = mapped_column(Text(), nullable=False)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=False)

    def get_id(self) -> uuid.UUID:
        return self.mail_id

    def __repr__(self) -> str:
        return f"Mail<{self.subject!r}>"


class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    audit_log_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # Who
    user_id: Mapped[uuid.UUID] = mapped_column(
        pg.UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    # When
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now)
    # What
    object_id: Mapped[str] = mapped_column(String(255))
    flag: Mapped[int] = mapped_column(Integer(), nullable=False)
    # Where
    table_name: Mapped[str] = mapped_column(String(255), nullable=False)
    changed_data: Mapped[str] = mapped_column(Text(), nullable=True)
    # Why
    justification: Mapped[str] = mapped_column(Text(), nullable=True, default="N/A")
