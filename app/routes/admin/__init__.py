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
from sqlalchemy import not_, or_, select

from ... import bcrypt, consts, db, utils
from ...decorators import permission_required, superuser_required
from ...models import Permission, User, UserPermission
from .forms import AssignUserPermissionForm, RegisterNewUserForm

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


@bp.route("/assgin-user-permission/<string:user_id>", methods=["GET", "POST"])
@superuser_required
def assign_user_permission(user_id: str):
    form = AssignUserPermissionForm()

    user = db.session.get(User, ident=user_id)

    if not user:
        flash(f"User with id: {user_id} does not exist.", "warning")
        return redirect(url_for("admin.panel"))

    user_permissions = [
        row[0]
        for row in db.session.execute(
            select(Permission)
            .join(UserPermission)
            .filter(UserPermission.user_id == user_id)
        ).all()
    ]

    unassigned_permissions = db.session.execute(
        select(
            Permission,
        ).filter(
            not_(
                Permission.permission_id.in_(
                    set({user_perm.permission_id for user_perm in user_permissions})
                )
            )
        )
    ).scalars()

    permission_choices = [
        (str(perm.permission_id), perm.name) for perm in unassigned_permissions
    ]
    print(permission_choices)
    form.permission.choices = permission_choices

    if form.validate_on_submit():
        permission_id = form.permission.data

        db_permission = db.session.get(Permission, ident=permission_id)

        if not db_permission:
            flash("Permission with this id is not found", "warning")
            return redirect(url_for("admin.assign_user_permission", user_id=user_id))

        if db.session.get(UserPermission, ident=(user_id, permission_id)):
            flash(
                f"Permission <b>{db_permission.name}</b> is already assigned to <b>{user.fullname}</b>",
                "info",
            )
            return redirect(url_for("admin.assign_user_permission", user_id=user_id))

        user_permission = UserPermission(
            user_id=user_id,
            permission_id=permission_id,
            assigned_by_id=current_user.get_id(),
        )

        try:
            db.session.add(user_permission)
            flash(
                f"Permission <b>{db_permission.name}</b> assigned successfully for <b>{user.fullname}</b>.",
                "info",
            )
            db.session.commit()
            return redirect(url_for("admin.assign_user_permission", user_id=user_id))
        except Exception as e:
            db.session.rollback()
            app.logger.error(str(e))
            flash("Something went wrong, Please try again later.", "danger")

    return render_template(
        "admin/assign_user_permission.html",
        form=form,
        user=user,
        user_permissions=user_permissions,
        title="Assign Permissions",
    )


@bp.route("/user-details/<string:user_id>")
@superuser_required
def user_details(user_id: str):
    user = db.session.get(User, ident=user_id)

    if not user:
        flash(f"User with id: {user_id} does not exist.", "warning")
        return redirect(url_for("admin.panel"))

    user_permissions = db.session.execute(
        select(
            Permission,
            UserPermission,
        )
        .select_from(Permission)
        .join(UserPermission)
        .filter(UserPermission.user_id == user_id)
    ).all()

    return render_template(
        "admin/user_details.html", user=user, user_permissions=user_permissions
    )


@bp.route(
    "/delete-user-permission/<string:user_id>/permission/<string:permission_id>",
    methods=["GET", "POST"],
)
@superuser_required
def delete_user_permission(user_id: str, permission_id: str):
    user = db.session.get(User, ident=user_id)

    if not user:
        flash(f"User with id: {user_id} does not exist.", "warning")
        return redirect(url_for("admin.panel"))

    permission = db.session.get(Permission, ident=permission_id)

    if not permission:
        flash(f"Permission with id: {permission_id} does not exist.", "warning")
        return redirect(url_for("admin.panel"))

    user_permission = db.session.get(UserPermission, ident=(user_id, permission_id))

    if not user_permission:
        flash(
            f"Permission <b>{permission.name}</b> is not assigned to <b>{user.fullname}</b>",
            "warning",
        )
        return redirect(url_for("admin.panel"))

    try:
        db.session.delete(user_permission)
        flash(
            f"Permission <b>{permission.name}</b> removed from  <b>{user.fullname}</b>",
            "info",
        )
        db.session.commit()
        return redirect(url_for("admin.user_details", user_id=user.user_id))
    except Exception as e:
        db.session.rollback()
        app.logger.error(str(e))
        flash("Something went wrong, Please try again later.", "danger")

    return redirect(url_for("admin.panel"))
