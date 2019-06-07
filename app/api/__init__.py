from flask import Blueprint

api = Blueprint('api', __name__)

from app.api import students, errors, auth,email,projects