# blabber
Blog App - User registration and authentication. Post, edit, delete and favorite posts.

Built with Python/Flask, Bootstrap, jQuery

Usage instructions:

1) Install virtualenv, libraries and activate environment
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
```
2) Create database
```
from app import *
db.create_all()
```

3) Create fictitious users and posts
```
from app import *
User.generate_fake()
Post.generate_fake()
```

4) Run app
```
python app.py
```

