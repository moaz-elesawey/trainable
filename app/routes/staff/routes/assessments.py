from flask import (
    render_template,
)

from .... import consts
from ....decorators import permission_required
from .. import bp


@bp.route("add-new-assessment", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_CREATE_ASSESSMENT)
def add_new_assessment():
    """Add New Assessment"""
    return render_template("staff/add_new_assessment.html", title="New Assessment")


@bp.route("assign-user-assessment", methods=["GET", "POST"])
@permission_required(consts.PermissionEnum.CAN_ASSIGN_USER_ASSESSMENT)
def assign_user_assessment():
    """Assign User Assessment"""
    return render_template(
        "staff/assign_user_assessment.html", title="Assign Assessment"
    )
