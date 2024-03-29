"""
The app.py file is the backbone of the application. It contains configuration settings for the
program
"""
import socket
from functools import wraps
from flask import Flask, render_template
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy


# Flask configurations
UPLOAD_FOLDER = 'BOMUploads'
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://csc2033_team36:Net8BondSaps@tharsus' \
                                        '.cyxylxr5iurl.eu-west-2.rds.amazonaws.com:3306/csc2033_team36'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'LongAndRandomSecretKey'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# initialise the database
db = SQLAlchemy(app)


def requires_roles(*roles):
    """
    This method guarantees that only inputted roles will be able to access flask view methods.
    :param roles: roles which are authorized to access a page.
    :return: logging.warning if current.user was not in roles.
    """
    def wrapper(role):
        @wraps(role)
        def wrapped(*args, **kwargs):
            if current_user.role not in roles:

                # Redirect the user to an unauthorised notice!
                return render_template('403.html')
            return role(*args, **kwargs)

        return wrapped

    return wrapper



@app.route('/')
def search():
    """
    The home page view
    """
    if current_user.is_authenticated:
        return render_template('index.html')
    else:
        return render_template('index.html')



# Error handling functionality
@app.errorhandler(400)
def handle_bad_request(error):
    return render_template('400.html'), 400


@app.errorhandler(403)
def page_forbidden(error):
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return render_template('405.html'), 405


@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@app.errorhandler(503)
def service_unavailable(error):
    return render_template('503.html'), 503


if __name__ == "__main__":
    my_host = "127.0.0.1"
    free_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    free_socket.bind((my_host, 0))
    free_socket.listen(5)
    free_port = free_socket.getsockname()[1]
    free_socket.close()

    # The login manager
    login_manager = LoginManager()
    login_manager.login_view = 'users.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    from users.views import users_blueprint
    from admin.views import admin_blueprint

    app.register_blueprint(users_blueprint)
    app.register_blueprint(admin_blueprint)

    app.run(host=my_host, port=free_port, debug=True)
