import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	POSTS_PER_PAGE = 20
	SECRET_KEY = os.environ.get('SECRET_KEY') or '5\x82\xdf4\xfb\x01eK\xcf\xcc-\x99b\x87\x8en\x07V\xfe{\xf9\xae\x18\xd4'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
	'sqlite:///' + os.path.join(basedir, 'app.db')
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	MAIL_SERVER = os.environ.get('MAIL_SERVER')
	MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
	MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
	MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
	MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
	ADMINS = ['leeholim@uchicago.edu', 'rohin@uchicago.edu']