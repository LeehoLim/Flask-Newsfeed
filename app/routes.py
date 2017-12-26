from app import app, db
from app.forms import LoginForm, RegistrationForm, PostForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from datetime import datetime
from app.forms import EditProfile


#Get the time for the last time the user was seen
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()


@app.route('/', methods=['GET', 'POST'])

@app.route('/index', methods=['GET', 'POST'])
@login_required
#Index page
def index():
	form = PostForm()
	if form.validate_on_submit():
		post = Post(body=form.post.data, author=current_user)
		db.session.add(post)
		db.session.commit()
		flash('Successfully posted.')
		return redirect(url_for('index'))

	page = request.args.get('page', 1, type=int)
	posts = current_user.followed_posts().paginate(
		page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('index', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('index', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Home', form=form, posts=posts.items, next_url=next_url, prev_url=prev_url)

@app.route('/explore')
@login_required
def explore():
	page = request.args.get('page', 1, type=int)
	posts= Post.query.order_by(Post.timestamp.desc()).paginate(
		page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('explore', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('explore', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('index.html', title='Explore', posts=posts.items, next_url=next_url, prev_url=prev_url)	


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated: #If user is already authenticated, return to index
		return redirect(url_for('index'))
	form = RegistrationForm() #Calls registration form
	if form.validate_on_submit(): #Checks to see if it is validated
		user = User(username=form.username.data, email=form.email.data, fname=form.fname.data, lname=form.lname.data) #Creates user
		user.set_password(form.password.data) #Sets password
		db.session.add(user) #Adds user to db
		db.session.commit() #Commits user to db
		flash('Account successfully created. Please check email for further validation')
		return redirect(url_for('login')) #Redirects to login page
	return render_template('signup.html', title='Sign up', form=form)


#Login user
@app.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated: #If current user is valid, then accept user
		return redirect(url_for('index'))
	form = LoginForm() #Draws login form from the forms.py file, which includes uname, pword
	if form.validate_on_submit(): #If form is valid
		user = User.query.filter_by(username=form.username.data).first() #Store username into variable user
		#Filters by input data from form
		#Only calls the first data entry, because we will only want to check with MAX one.
		if user is None or (not user.check_password(form.password.data)): #if the user password doesn't exist or username doesn't exist, return error
			flash ('Incorrect username or password') #Error
			return redirect(url_for('login')) #Redirects back to login page
		login_user(user, remember=form.remember_me.data) #Else login the user
		next_page = request.args.get('next') 
		if (not next_page) or (not next_page.startswith('/')): #If URL does not have next argument / URL does not start with '/', redirect to index page
			next_page = url_for('index')
		return redirect(next_page) #If those conditions are not met, then it will just redirect
	return render_template('login.html', title='Sign in page', form=form) 

#User Profile
@app.route('/user/<username>')
@login_required
def user(username):
	user = User.query.filter_by(username=username).first_or_404()
	page = request.args.get('page', 1, type=int)
	posts = user.posts.order_by(Post.timestamp.desc()).paginate(
		page, app.config['POSTS_PER_PAGE'], False)
	next_url = url_for('user', page=posts.next_num) \
		if posts.has_next else None
	prev_url = url_for('user', page=posts.prev_num) \
		if posts.has_prev else None
	return render_template('user.html', user=user, posts=posts.items, next_url=next_url, prev_url=prev_url)

#Logout user
@app.route('/logout')
def logout(): 
	logout_user() #Built into flask_login, logout function
	return redirect(url_for('index')) #Redirects to index after

#Edit Profile
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfile(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.fname = form.fname.data
		current_user.lname = form.lname.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Settings have been updated.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.fname.data = current_user.fname
		form.lname.data = current_user.lname
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Settings', form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found.'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You cannot follow yourself!')
		return redirect(url_for('user', username=username))
	current_user.follow(user)
	db.session.commit()
	flash('You are following {}!'.format(username))
	return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
	user = User.query.filter_by(username=username).first()
	if user is None:
		flash('User {} not found.'.format(username))
		return redirect(url_for('index'))
	if user == current_user:
		flash('You cannot unfollow yourself!')
		return redirect(url_for('user', username=username))
	current_user.unfollow(user)
	db.session.commit()
	flash('You are not following {}.'.format(username))
	return redirect(url_for('user', username=username))


