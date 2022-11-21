from flask import Blueprint

education = Blueprint('education', __name__,  template_folder="../templates")

from . import view