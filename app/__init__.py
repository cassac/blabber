import os
from flask import Flask
from flask.ext.moment import Moment 
from flask.ext.bootstrap import Bootstrap 
from flask.ext.sqlalchemy import SQLAlchemy 
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from flask_restful import Api

bootstrap = Bootstrap()
db = SQLAlchemy()
api = Api()
moment = Moment()
csrf = CsrfProtect()

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.session_protection = 'strong'
login_manager.login_message_category = 'info'

from main.views import AllPosts, SinglePost, LikePost, UserProfile

api.add_resource(AllPosts, '/posts')
api.add_resource(SinglePost, '/posts/<int:post_id>')
api.add_resource(LikePost, '/like')
api.add_resource(UserProfile, '/user')

def create_app(config_name):
	app = Flask(__name__)
	app.config.from_object(config_name)
	bootstrap.init_app(app)
	db.init_app(app)
	login_manager.init_app(app)
	api.init_app(app)
	moment.init_app(app)
	csrf.init_app(app)

	from .main import main as main_blueprint
	app.register_blueprint(main_blueprint)

	return app