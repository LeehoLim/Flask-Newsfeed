from datetime import datetime
from app import app, db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


followers = db.Table('followers', 
					db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
					db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
			)


class User(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key=True) #Unique ID per user
	username = db.Column(db.String(64), index=True, unique=True) #Username stored as string
	fname = db.Column(db.String(64), index=True)
	lname = db.Column(db.String(64), index=True)
	email = db.Column(db.String(128), index=True, unique=True) #Email stored as string
	password_hash = db.Column(db.String(256)) #Password stored as hash (SHA256)
	posts = db.relationship('Post', backref='author', lazy='dynamic') #Maintains relationship of user's post w/ user
	about_me = db.Column(db.String(256))
	last_seen = db.Column(db.DateTime, default=datetime.utcnow)
	followed = db.relationship(
		'User', secondary=followers,
		primaryjoin=(followers.c.follower_id == id),
		secondaryjoin=(followers.c.followed_id == id),
		backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
	

	#Shows posts of users that you follow
	def followed_posts(self): #Adds posts of people that YOU specifically follow
		followed = Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(
			followers.c.follower_id == self.id)
		own = Post.query.filter_by(user_id=self.id)
		out = followed.union(own).order_by(Post.timestamp.desc())
		return out


	#Adds user to list
	def follow(self,user): #Follows user if user is not already following
		if not self.is_following(user):
			self.followed.append(user)

	#Removes user from list
	def unfollow(self, user): #Unfollows user if user is not following
		if self.is_following(user):
			self.followed.remove(user)

	#Checks to see if the user is following another user (returns Bool)
	def is_following(self, user):
		return self.followed.filter(followers.c.followed_id == user.id).count() > 0

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




#Receives user ID
@login.user_loader
def load_user(id):
	return User.query.get(int(id)) #Returns the user ID in the form of INT datatype


class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True) #Post ID as INT
	body = db.Column(db.String(256)) #Post message (up to 256 char)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow) #Posted timestamp
	user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #Post to associate relationship with User ID

	def __repr__(self):
		return '<Post {}>'.format(self.body)
