from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms import (
    BooleanField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Length
from wtforms.widgets import CheckboxInput, ListWidget

from ... import db
from ...models import Group, Permission

empty_option = [("", "-------")]


class RegisterNewUserForm(FlaskForm):
    fullname = StringField("Fullname", validators=[DataRequired()])
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=4, max=25)]
    )
    group = SelectField("Group", validators=[])
    is_active = BooleanField("Is Active", default=True)
    is_staff = BooleanField("Is Staff", default=False)
    is_superuser = BooleanField("Is Super user", default=False)
    submit = SubmitField("Register")

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        db_groups = db.session.execute(select(Group)).scalars()
        self.group.choices = empty_option + [
            (str(gp.group_id), str(gp.name)) for gp in db_groups
        ]


class AssignUserPermissionsForm(FlaskForm):
    permissions = SelectMultipleField(
        "Permissions",
        widget=ListWidget(prefix_label=True),
        option_widget=CheckboxInput(),
    )
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_permissions = db.session.execute(select(Permission)).scalars()
        self.permissions.choices = [
            (str(p.permission_id), f"{p.name}: {p.description}") for p in db_permissions
        ]
