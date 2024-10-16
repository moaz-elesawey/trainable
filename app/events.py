import uuid

from flask_login import current_user
from sqlalchemy import event, insert

from . import utils
from .models import (
    Assessment,
    AssessmentQuestion,
    AuditLog,
    Choice,
    Course,
    CourseAssessment,
    CourseLesson,
    Lesson,
    Question,
    User,
    UserAssessment,
    UserAssessmentQuestion,
    UserCourse,
    UserPermission,
)


def get_target_id_str(target) -> str:
    target_id = target.get_id()
    target_id_str = None

    if isinstance(target_id, uuid.UUID):
        target_id_str = str(target_id)
    elif isinstance(target_id, tuple):
        target_id_str = ":".join([str(id_) for id_ in target_id])

    return target_id_str


def after_insert_listener(mapper, connection, target):
    """Hook to run after each insert statement."""
    _mapper = mapper

    if current_user is not None:
        return

    connection.execute(
        insert(AuditLog).values(
            user_id=current_user.user_id,
            object_id=get_target_id_str(target),
            table_name=target.__tablename__,
            flag=utils.INSERT_FLAG,
            changed_data="{}",
        )
    )


def after_update_listener(mapper, connection, target):
    """Hook to run after each update statement."""
    _mapper = mapper

    if current_user is not None:
        return

    connection.execute(
        insert(AuditLog).values(
            user_id=current_user.user_id,
            object_id=get_target_id_str(target),
            table_name=target.__tablename__,
            flag=utils.UPDATE_FLAG,
            changed_data=str({"change": {}}),
        )
    )


# register events
def register_sa_events() -> None:
    """Register SQLAlchemy Events"""

    event.listen(UserPermission, "after_insert", after_insert_listener)
    event.listen(Course, "after_insert", after_insert_listener)
    event.listen(CourseLesson, "after_insert", after_insert_listener)
    event.listen(UserCourse, "after_insert", after_insert_listener)
    event.listen(CourseAssessment, "after_insert", after_insert_listener)
    event.listen(Assessment, "after_insert", after_insert_listener)
    event.listen(UserAssessment, "after_insert", after_insert_listener)
    event.listen(Lesson, "after_insert", after_insert_listener)
    event.listen(CourseLesson, "after_insert", after_insert_listener)
    event.listen(UserAssessmentQuestion, "after_insert", after_insert_listener)
    event.listen(AssessmentQuestion, "after_insert", after_insert_listener)
    event.listen(Question, "after_insert", after_insert_listener)
    event.listen(Choice, "after_insert", after_insert_listener)

    # Register Update Events
    event.listen(User, "after_update", after_update_listener)
    event.listen(User, "after_insert", after_insert_listener)
