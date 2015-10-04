from flask import (Flask, flash, render_template, jsonify, request,
	redirect, url_for, get_flashed_messages, abort)
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.login import (LoginManager, current_user, login_user, 
	logout_user, login_required)
from flask_restful import Api, fields, marshal_with, reqparse, Resource
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import desc
from flask_wtf.csrf import CsrfProtect
import json

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'the secret key, shhhh!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
api = Api(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
csrf = CsrfProtect(app)
login_manager.init_app(app)

from models import *
from forms import LoginForm, SignUpForm
@app.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None and user.verify_password(form.password.data):
			login_user(user, form.remember_me.data)
			return redirect(request.args.get('next') or url_for('.read'))
		flash('Invalid credentials', 'danger')
	elif form.errors:
		flash('Invalid credentials', 'danger')
	get_flashed_messages()		
	return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
	logout_user()
	flash('You have been logged out.')
	return redirect(url_for('.read'))

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
	form = SignUpForm()
	if form.validate_on_submit():
		username = User.query.filter_by(username=form.username.data).first()
		email = User.query.filter_by(email=form.email.data).first()
		if username != None:
			flash('Username already registered', 'danger')
			get_flashed_messages()	
			return render_template('signup.html', form=form)
		if email != None:
			flash('Email already registered', 'danger')
			get_flashed_messages()	
			return render_template('signup.html', form=form)
		new_user = User(email=form.email.data,
						username=form.username.data,
						password=form.password.data
						)
		db.session.add(new_user)
		db.session.commit()
		login_user(new_user, True)
		flash('Sign up successful', 'success')
		get_flashed_messages()
		return redirect(url_for('.read'))
	elif form.errors:
		for error in form.errors:
			flash(form.errors[error][0], 'danger')
	get_flashed_messages()	
	return render_template('signup.html', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/read/', methods=['GET', 'POST'])
def read():
	# Not sure why, but flashed messages won't
	# display in template unless invoke below method
	get_flashed_messages()
	return render_template('read.html')

@app.route('/read/<int:post_id>')
def read_post(post_id):
	post = Post.query.filter_by(id=post_id).first()
	if post==None:
		flash("Post doesn't exist", 'danger')
		return redirect( url_for('.read') )
	return render_template('readpost.html', post_id=post.id)

@app.route('/write/', methods=['GET', 'POST'])
@login_required
def write():
	return render_template('write.html')

@app.route('/edit/<int:post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
	post = Post.query.filter_by(id=post_id).first()
	if post.author_id != current_user.id:
		flash('Can only edit your posts', 'warning')
		return redirect( url_for('.read') )
	return render_template('edit.html', post_id=post_id)		

@app.route('/profile/')
@login_required
def profile():
	return render_template('profile.html')

postslist_parser = reqparse.RequestParser()
postslist_parser.add_argument('title')
postslist_parser.add_argument('tag')
postslist_parser.add_argument('content')
postslist_parser.add_argument('page_num')

singlepost_parser = reqparse.RequestParser()
singlepost_parser.add_argument('title')
singlepost_parser.add_argument('tag')
singlepost_parser.add_argument('content')

likepost_parser = reqparse.RequestParser()
likepost_parser.add_argument('post_id')

userprofile_parser = reqparse.RequestParser()
userprofile_parser.add_argument('oldemail')
userprofile_parser.add_argument('newname')
userprofile_parser.add_argument('newemail')

class AllPosts(Resource):
	def get(self):
		args = postslist_parser.parse_args()
		page_num = args['page_num']

		if page_num != None:
			page = int(page_num)
		else:
			page=1

		results = Post.query.order_by(desc(Post.id)).paginate(page, 15)
		pages=results.iter_pages(left_edge=2, 
								 left_current=2,
								 right_current=4,
								 right_edge=2)
		pages=[p for p in pages]

		posts = []
		for post in results.items:
			if current_user.is_anonymous:
				like_status = 0
			elif current_user.is_authenticated:
				like_status = post in current_user.liked_posts.all()
			posts.append(
				{
				"id": post.id,
				"slug": post.slug,
				"title": post.title,
				"content": post.content,
				"created": post.created,
				"like_status": like_status,
				"author": post.author.username,
				})
		return jsonify(posts=posts,
					   current_page=results.page, 
					   has_prev=results.has_prev,
					   has_next=results.has_next,
					   pages=pages)

	def post(self):
		args = postslist_parser.parse_args()
		slug = args['title'].replace(' ', '-')
		post = Post(title=args['title'], 
					slug=slug,
					content=args['content'],
					author_id=current_user.id)
		db.session.add(post)
		db.session.commit()
		return 'Successfully created new post!'

class SinglePost(Resource):
    def get(self, post_id):
    	result = Post.query.filter_by(id=post_id).first()
    	if result == None:
    		return "Post doesn't exist", 404
        post = [{
        	'post_id': result.id,
        	'author': result.author.username,
        	'title': result.title,
        	'content': result.content,
        	'created': result.created
        }]
        return jsonify(post=post)

    def put(self, post_id):
    	args = singlepost_parser.parse_args()
    	post = Post.query.filter_by(id=post_id).first()
    	if post == None:
    		return "Post doesn't exist", 404
    	post.title = args['title']
    	post.content = args['content']
    	db.session.commit()
    	return 'Post updated', 201

    def delete(self, post_id):
    	post = Post.query.filter_by(id=post_id).first()
    	db.session.delete(post)
    	db.session.commit()
        return 'Success: post deleted', 201

class LikePost(Resource):
	def post(self):
		
		args = likepost_parser.parse_args()
		post_id = int(args['post_id'])

		if current_user.is_anonymous:
			return {'like_status': 1, 
					'post_id': post_id,
					'message': 'Sign up to save your liked posts!'}

		post = Post.query.filter_by(id=post_id).first()
		if post == None:
			return "Post doesn't exist", 404

		user = User.query.filter_by(id=current_user.id).first()
		
		if post in user.liked_posts.all():
			user.liked_posts.remove(post)
			db.session.commit()
			return {'like_status': 0, 
					'post_id': post.id,
					'message': 'Post unliked'}
		else:
			user.liked_posts.append(post)
			db.session.commit()
			return {'like_status': 1, 
					'post_id': post.id,
					'message': 'Post liked'}
	def put(self):
		return 'This is the time'

class UserProfile(Resource):
	def get(self):
		user_info = {'username': current_user.username,
					'email': current_user.email,
					'created': current_user.created}
		liked_posts = [] 
		for post in current_user.liked_posts.all():
			liked_posts.append({'id': post.id,
								'title': post.title,
								})
		user_posts = []
		for post in current_user.posts.all():
			user_posts.append({'id': post.id,
							   'title': post.title,
								})
		return jsonify(user_info=user_info,
					   liked_posts=liked_posts,
					   user_posts=user_posts)

	def put(self):
		args = userprofile_parser.parse_args()
		oldemail = args['oldemail']
		newname = args['newname']
		newemail = args['newemail']

		user = User.query.filter_by(email=oldemail).first()
		if user == None:
			return "Can't find user", 404
		user.email = newemail
		user.username = newname
		db.session.commit()
		return 'from the put request'

api.add_resource(AllPosts, '/posts')
api.add_resource(SinglePost, '/posts/<int:post_id>')
api.add_resource(LikePost, '/like')
api.add_resource(UserProfile, '/user')

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0')