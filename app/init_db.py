from flask import Flask
from sqlalchemy import select, or_

from . import db, bcrypt
from .consts import PERMISSIONS
from .models import User, Group, Permission


def init_db_data(app: Flask) -> None:
    """Initialize database data."""

    # Get The Superusers Group Data
    name = app.config.get("SUPERUSER_GROUP_NAME")
    abbreviation = app.config.get("SUPERUSER_GROUP_ABBREVIATION")

    with app.app_context():
        stmt = select(Group).filter(
            or_(Group.name == name, Group.abbreviation == abbreviation)
        )
        group = db.session.execute(stmt).scalar_one_or_none()

        if not group:
            group = Group(
                name=name,
                abbreviation=abbreviation,
                description="Super Users Highest Level Group.",
            )
            db.session.add(group)
            db.session.commit()
            db.session.refresh(group)

    # Get The Superuser User Data.
    username = app.config.get("FIRST_SUPERUSER")
    password = app.config.get("FIRST_SUPERUSER_PASSWORD")

    with app.app_context():
        stmt = select(User).filter(User.username == username)
        user = db.session.execute(stmt).scalar_one_or_none()

        if not user:
            user = User(
                username=username,
                fullname="Admin User",
                password_hash=bcrypt.generate_password_hash(password).decode("UTF-8"),
                group_id=group.group_id,
                is_active=True,
                is_staff=True,
                is_superuser=True,
            )
            db.session.add(user)
            db.session.commit()

    with app.app_context():
        db_permissions = []
        for permission in PERMISSIONS:
            if not db.session.execute(
                select(Permission).filter(Permission.codename == permission["codename"])
            ).scalar_one_or_none():
                db_permission = Permission(
                    name=permission["name"],
                    codename=permission["codename"],
                    flag=permission["flag"],
                    description=permission["description"],
                )

                db_permissions.append(db_permission)

            db.session.add_all(db_permissions)
            db.session.commit()
