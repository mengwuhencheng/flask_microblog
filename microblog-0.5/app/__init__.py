import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_openid import OpenID
from config import basedir
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_migrate import Migrate

app = Flask(__name__)
bootstarp = Bootstrap(app)
app.config.from_object('config')
mail = Mail(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'
oid = OpenID(app, os.path.join(basedir, 'tmp'))
migrate = Migrate(app,db)

from app import views, models

