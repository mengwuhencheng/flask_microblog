import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from flask_openid import OpenID
from config import basedir
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate
from flask_moment import Moment

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
moment = Moment

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    # register Blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

# app = Flask(__name__)
#bootstarp = Bootstrap(app)
# app.config.from_object('config')
#mail = Mail(app)
#db = SQLAlchemy(app)
# lm = LoginManager()
# lm.init_app(app)
# lm.login_view = 'login'
# oid = OpenID(app, os.path.join(basedir, 'tmp'))
# migrate = Migrate(app,db)

# from app import views, models
