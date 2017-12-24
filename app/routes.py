from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask import render_template, flash, redirect, request, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User 
from datetime import datetime
from app.forms import EditProfile



@app.route('/')
@app.route('/index')
@login_required
#Testing the user / posts
def index():
	user = {'username': 'leeho'}
	posts = [
		{
			'author' : {'username': 'Rohin'},
			'body' : 'Great day in Los Angeles!'
		},
		{
			'author' : {'username': 'Joshua'},
			'body' : 'I know, right?!'
		}
	]

	return render_template('index.html', title='Home', posts=posts)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	if current_user.is_authenticated: #If user is already authenticated, return to index
		return redirect(url_for('index'))
	form = RegistrationForm() #Calls registration form
	if form.validate_on_submit(): #Checks to see if it is validated
		user = User(username=form.username.data, email=form.email.data) #Creates user
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
	posts = [
		{'author': user, 'body': 'Test post 1'},
		{'author': user, 'body': 'Test post 2'}
	]
	return render_template('user.html', user=user, posts=posts)

#Logout user
@app.route('/logout')
def logout(): 
	logout_user() #Built into flask_login, logout function
	return redirect(url_for('index')) #Redirects to index after

#Edit Profile
@app.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
	form = EditProfileForm(current_user.username)
	if form.validate_on_submit():
		current_user.username = form.username.data
		current_user.about_me = form.about_me.data
		db.session.commit()
		flash('Settings have been updated.')
		return redirect(url_for('edit_profile'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.about_me.data = current_user.about_me
	return render_template('edit_profile.html', title='Settings', form=form)

#Get the time for the last time the user was seen
@app.before_request
def before_request():
	if current_user.is_authenticated:
		current_user.last_seen = datetime.utcnow()
		db.session.commit()




