from typing import Any
from datetime import datetime
from sqlalchemy import select, update
from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    current_app as app,
)
from flask_login import logout_user, login_user, login_required, current_user

from ... import db, bcrypt
from .forms import LoginForm, ChangePasswordForm
from ...models import User
from ... import utils


bp = Blueprint("auth", __name__, template_folder="templates")


@bp.route("/login", methods=["GET", "POST"])
def login() -> Any:
    """Login a user with username, and password"""

    form = LoginForm()

    if request.method == utils.GET:
        if current_user.is_authenticated:
            return redirect(url_for("base.home"))

    if request.method == utils.POST:
        form = LoginForm()

        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data

            stmt = select(User).filter(User.username == username)
            user = db.session.execute(stmt).scalar_one_or_none()

            if not user:
                flash(f"User with username: {username} cannot be found.", "warning")
                return redirect(url_for("auth.login"))

            if not user.is_active:
                flash("Your account is in active. Kindly contact the admin.", "warning")
                return redirect(url_for("auth.login"))

            if bcrypt.check_password_hash(user.password_hash, password):
                login_user(user=user, remember=form.remember.data)
                flash(
                    f"Logged in successfully as <b>{user.fullname if user.fullname else username}</b>",
                    "success",
                )
                try:
                    db.session.execute(
                        update(User)
                        .where(User.user_id == user.get_id())
                        .values(last_login=datetime.now())
                    )
                    db.session.commit()
                except Exception as e:
                    db.session.rollback()
                    app.logger.error(e)
                if user.is_superuser:
                    return redirect(url_for("admin.panel"))
                if user.is_staff:
                    return redirect(url_for("staff.panel"))

                return redirect(url_for("base.home"))
            else:
                flash("Please, check your password and try again later", "danger")
                return redirect(url_for("auth.login"))
        else:
            flash("Something went wrong, Kindly try again later.", "danger")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html", form=form)


@bp.route("/logout", methods=["GET"])
@login_required
def logout() -> Any:
    """Logout user and remove his/her session"""
    logout_user()
    return redirect(url_for("auth.login"))


@bp.route("/profile")
@login_required
def profile():
    """Profile Route"""
    return render_template("auth/profile.html", user=current_user)


@bp.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    """Change Password Route"""
    form = ChangePasswordForm()

    if form.validate_on_submit():
        old_password = form.old_password.data
        new_password = form.new_password.data
        new_password_confirm = form.new_password_confirm.data

        if not bcrypt.check_password_hash(current_user.password_hash, old_password):
            flash("Old password does not match your password.", "danger")
            return redirect(url_for("auth.profile"))

        if new_password != new_password_confirm:
            flash("New password does not match.", "warning")
            return redirect(url_for("auth.change_password"))

        try:
            db.session.execute(
                update(User).values(
                    password_hash=bcrypt.generate_password_hash(new_password).decode(
                        "utf-8"
                    )
                )
            )
            db.session.commit()
            flash("Password updated successfully. Login back here", "success")
            # return redirect(url_for('auth.profile'))
            logout_user()
            return redirect(url_for("auth.login"))
        except Exception:
            db.session.rollback()
            app.logger.error()
            flash("Something went wrong, Please try again later", "danger")

    return render_template("auth/change_password.html", form=form)
