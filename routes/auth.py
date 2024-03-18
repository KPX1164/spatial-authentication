from flask import Blueprint

from controllers.authController import AuthController


class AuthBlueprint:
    auth_bp = Blueprint('auth_bp', __name__, url_prefix='/sign-in')
    auth_bp.route('/', methods=['POST'])(AuthController.auth)
    auth_bp.route('/sign-up', methods=['POST'])(AuthController.register)