#!python2.7_env/bin/python
from app import app
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

manager = Manager(app)
#Migrate =Migrate(app,db)
manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()
