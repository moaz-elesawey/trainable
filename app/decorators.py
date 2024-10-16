from flask import flash, redirect, url_for
from flask_login import current_user
from functools import wraps
from sqlalchemy import select
from .models import Permission, UserPermission
from . import db


def superuser_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login to access this page.", "warning")
            return redirect(url_for("auth.login"))

        if not current_user.is_superuser:
            flash("Page you attempt to visit does not exist", "warning")
            return redirect(url_for("base.home"))
        return f(*args, **kwargs)

    return wrapped_function


def staff_user_required(f):
    @wraps(f)
    def wrapped_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash("You need to login to access this page.", "warning")
            return redirect(url_for("auth.login"))

        if not current_user.is_staff:
            flash("Page you attempt to visit does not exist", "warning")
            return redirect(url_for("base.home"))
        return f(*args, **kwargs)

    return wrapped_function


def permission_required(permission_codename: str):
    def permission_required_func(f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash("You need to login to access this page.", "warning")
                return redirect(url_for("auth.login"))

            if current_user.is_superuser:
                return f(*args, **kwargs)

            permission = db.session.execute(
                select(Permission).filter(Permission.codename == permission_codename)
            ).scalar_one_or_none()

            if not permission:
                flash("Page you attempt to visit does not exist", "warning")
                return redirect(url_for("base.home"))

            user_permission = db.session.get(
                UserPermission, ident=(current_user.user_id, permission.permission_id)
            )

            if not user_permission:
                flash("Page you attempt to visit does not exist", "warning")
                return redirect(url_for("base.home"))
            return f(*args, **kwargs)

        return wrapped_function

    return permission_required_func
