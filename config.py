import os

ROOT_DIR = os.path.dirname(__file__)

class BaseConfig(object):
	"Base Configuration"
	SECRET_KEY = 'this should be more secret than this'

	@staticmethod
	def init_app(app):
		pass

class DevelopmentConfig(BaseConfig):
	"Development Configuration"
	DEBUG = True
	TESTING = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'

class StagingConfig(BaseConfig):
	"Staging Configuration"
	pass

class ProductionConfig(BaseConfig):
	"Production Configuration"
	pass	