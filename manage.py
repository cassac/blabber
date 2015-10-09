import os
from app import create_app, db
from app.models import *
from flask.ext.script import Manager, Shell
from config import DevelopmentConfig

app = create_app(DevelopmentConfig)

manager = Manager(app)

def make_shell_context():
	return dict(app=app, db=db, Post=Post, User=User)

manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
	manager.run()