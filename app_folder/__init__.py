from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
login_manager=LoginManager(app)
mail=Mail(app)
bootstrap = Bootstrap(app)
login_manager.login_view='login'

from app_folder import routes, models





# db = SQLAlchemy()
# login_manager=LoginManager()
# mail=Mail()
# bootstrap = Bootstrap()

# login_manager.login_view='login'


# def create_app(test_config=None):
#     app = Flask(__name__,instance_relative_config=False)

#     if test_config is None:
#         #not testing
#         app.config.from_object(Config)
#     else:
#         app.config.from_mapping(test_config)
    
#     db.init_app(app)
#     login_manager.init_app(app)
#     login_manager.login_view='login'
#     mail.init_app(app)
#     bootstrap.init_app(app)

#     with app.app_context():
#         from . import routes
#         from . import models
#         db.create_all()
#     return app