from flask import Blueprint

bp = Blueprint("staff", __name__, template_folder="templates")

from .routes import *  # noqa F403
