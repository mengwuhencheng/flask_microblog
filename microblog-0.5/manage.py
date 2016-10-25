#!python2.7_env/bin/python
import os
from app import create_app, db
from flask_script import Manager,Shell
from flask_migrate import Migrate, MigrateCommand
from app.models import User, Role, Permission, Post
app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
Migrate = Migrate(app,db)

def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('db',MigrateCommand)
manager.add_command("shell", Shell(make_context=make_shell_context))
if __name__ == '__main__':
    manager.run()
