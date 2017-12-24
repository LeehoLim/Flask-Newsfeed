from datetime import datetime
from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5

class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True) #Unique ID per user
	username = db.Column(db.String(64), index=True, unique=True) #Username stored as string
	email = db.Column(db.String(128), index=True, unique=True) #Email stored as string
	password_hash = db.Column(db.String(256)) #Password stored as hash (SHA256)
	posts = db.relationship('Post', backref='author', lazy='dynamic') #Maintains relationship of user's post w/ user
	about_me = db.Column(db.String(256))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)

	def __repr__(self):
		return '<User {}>'.format(self.username)

	#Method hashes password and stores password hash
	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	#Method compares password with hash to see if authenticated password
	def check_password(self, password):
		return check_password_hash(self.password_hash, password) 

	#Method creates an avatar of a given size!
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True) #Post ID as INT
	body = db.Column(db.String(256)) #Post message (up to 256 char)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #Posted timestamp
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Post to associate relationship with User ID

	def __repr__(self):
		return '<Post {}>'.format(self.body)


#Receives user ID
@login.user_loader
def load_user(id):
	return User.query.get(int(id)) #Returns the user ID in the form of INT datatype
