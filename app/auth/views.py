from flask import render_template
from . import auth
from .models import User


@auth.route('/')
def index():
    users = User.query.all()
    print('users:')
    print(users)
    return render_template('index.html')
