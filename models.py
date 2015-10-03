from app import db, login_manager
from datetime import datetime
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash 

class Post(db.Model):
    __tablename__ = 'post'    
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True)
    title = db.Column(db.String(120), unique=True)
    content = db.Column(db.Text)
    created = db.Column(db.Integer, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # tags = 

    # def __init__(self, slug, title, content, author_id):
    #     self.slug = slug
    #     self.title = title
    #     self.content = content
    #     self.author_id = author_id

    def __repr__(self):
        return '<Post %r>' % self.title

    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py, random
        seed()
        for i in range(100):
            title=forgery_py.lorem_ipsum.sentence()
            p = Post(
                title=title,
                slug=title.replace(' ', '-'),
                content=forgery_py.lorem_ipsum.paragraph(),
                author_id=random.choice(range(1, 11))
                )
            db.session.add(p)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

user_liked_posts = db.Table('user_liked_posts',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('post_id', db.Integer, db.ForeignKey('post.id'))
    )

class User(UserMixin, db.Model):
    __tablename__ = 'user'    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), unique=True)
    created = db.Column(db.Integer, default=datetime.utcnow)
    posts = db.relationship('Post', backref='author',
                                lazy='dynamic')
    liked_posts = db.relationship('Post',
        secondary=user_liked_posts,
        backref=db.backref('user', lazy='dynamic'),
        lazy='dynamic')

    # def __init__(self, username, email):
    #     self.username = username
    #     self.email = email

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User %r>' % self.username

    def generate_fake(count=10):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py
        seed()
        for i in range(10):
            u = User(email=forgery_py.internet.email_address(),
                username=forgery_py.internet.user_name(True),
                password=forgery_py.lorem_ipsum.word())
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()