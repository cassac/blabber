# blabber
Blog App - User registration, authentication and API. Post, edit, delete and favorite posts.

Built with Python/Flask, Flask-RESTful, Bootstrap, jQuery

Usage instructions:

1) Install virtualenv, libraries and activate environment
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```
2) Create database
```
python manage.py shell
db.create_all()
```

3) Create fictitious users and posts
```
python manage.py shell
<<<<<<< HEAD
User.generate_fake()
Post.generate_fake()
=======
User().generate_fake()
Post().generate_fake()
>>>>>>> 251c0748dade9601b244f4b91abb532490764d81
```

4) Run app
```
python manage.py runserver
```

