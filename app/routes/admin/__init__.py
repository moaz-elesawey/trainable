from datetime import datetime

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask import (
    current_app as app,
)
from flask_login import current_user
from sqlalchemy import delete, or_, select

from ... import bcrypt, consts, db, utils
from ...decorators import permission_required, superuser_required
from ...models import User, UserPermission
from .forms import AssignUserPermissionsForm, RegisterNewUserForm

bp = Blueprint("admin", __name__, template_folder="templates")


@bp.route("register-user", methods=["GET", "POST"])
@superuser_required
def register_user():
    """Register a New User"""

    form = RegisterNewUserForm()

    if request.method == utils.POST:
        if form.validate_on_submit():
            fullname = form.fullname.data
            username = form.username.data
            password = app.config.get("DEFAULT_USER_PASSWORD", "P@ssw0rd")
            group_id = form.group.data
            is_active = form.is_active.data
            is_staff = form.is_staff.data
            is_superuser = form.is_superuser.data

            # check if user exists
            user = db.session.execute(
                select(User).filter(User.username == username)
            ).scalar_one_or_none()

            if user:
                flash(f"User with username: {username} already exists.", "warning")
                return redirect(url_for("admin.register_user"))

            password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
            user = User(
                fullname=fullname,
                username=username,
                password_hash=password_hash,
                group_id=group_id,
                is_active=is_active,
                is_staff=is_staff,
                is_superuser=is_superuser,
                registered_by_id=current_user.get_id(),
                last_login=datetime.now(),
            )

            try:
                db.session.add(user)
                db.session.commit()
                db.session.refresh(user)
                flash(f"User registered successufully for <b>{fullname}</b>", "success")
                return redirect(url_for("admin.panel"))
            except Exception:
                flash("Something went wrong, Please try again later.", "danger")
                db.session.rollback()

    return render_template("admin/register_user.html", form=form, title="Register User")


@bp.route("/panel", methods=["GET"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_COURSE)
def panel():
    """Admin Panel"""

    q_user = request.args.get("q_user", "")

    users = db.session.execute(
        select(
            User.user_id,
            User.fullname,
            User.is_active,
            User.is_staff,
            User.is_superuser,
        )
        .select_from(User)
        .filter(or_(User.username.icontains(q_user), User.fullname.icontains(q_user)))
    )

    return render_template(
        "admin/panel.html", users=users, q_user=q_user, title="Panel"
    )


@bp.route("/assgin-user-permissions/<string:user_id>", methods=["GET", "POST"])
@superuser_required
def assign_user_permissions(user_id: str):
    form = AssignUserPermissionsForm()

    user = db.session.get(User, ident=user_id)
    db.session.commit()

    if not user:
        flash(f"User with id: {user_id} does not exist.", "warning")
        return redirect(url_for("admin.panel"))

    db_permissions = []

    if request.method == utils.GET:
        form.permissions.data = [str(p.permission_id) for p in user.permissions]

    if form.validate_on_submit():
        permissions = form.permissions.data

        for permission_id in permissions:
            db_permissions.append(
                UserPermission(
                    user_id=user_id,
                    permission_id=permission_id,
                    assigned_by_id=current_user.get_id(),
                )
            )

        try:
            db.session.execute(
                delete(UserPermission).where(UserPermission.user_id == user.user_id)
            )
            db.session.add_all(db_permissions)
            flash(
                f"Permissions assigned successfully for <b>{user.fullname}</b>.",
                "info",
            )
            db.session.commit()
            return redirect(url_for("admin.panel"))
        except Exception as e:
            db.session.rollback()
            app.logger.error(str(e))
            flash("Something went wrong, Please try again later.", "danger")

    return render_template(
        "admin/assign_user_permissions.html",
        form=form,
        user=user,
        title="Assign Permissions",
    )
